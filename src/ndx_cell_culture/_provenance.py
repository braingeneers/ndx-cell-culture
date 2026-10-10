"""Complete subject provenance while preserving existing target ownership."""

from collections import deque

from hdmf.common import VectorData


def _references(value):
    if value is None:
        return []
    if isinstance(value, VectorData):
        return list(value.data)
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _check_names(values, owner_name, reserved=()):
    names = {}
    for value in values:
        if value.name in reserved:
            raise ValueError(
                f"Object name {value.name!r} is reserved under {owner_name}; use a distinct identifier-style name."
            )
        previous = names.get(value.name)
        if previous is not None and previous is not value:
            raise ValueError(
                f"Distinct objects named {value.name!r} would be stored under {owner_name}; "
                "reuse the same object or give the objects distinct names."
            )
        names[value.name] = value


def collect_subject_provenance(subject, culture, cell_lines, cell_cultures):
    """Return biological collections and validated, unowned application attachments."""
    # Import at call time: the public classes are generated during package import.
    from . import CellCulture, CellLine, ConstructApplication

    lines, cultures = [], []
    seen = set()
    applications = {}
    pending = deque(
        [culture] + _references(cell_lines) + _references(cell_cultures)
    )
    while pending:
        obj = pending.popleft()
        if obj is None or id(obj) in seen:
            continue
        if not isinstance(obj, (CellLine, CellCulture)):
            raise TypeError("Subject provenance references must target CellLine or CellCulture objects.")
        if obj.parent is not None and obj.parent is not subject:
            raise ValueError(
                f"{type(obj).__name__} {obj.name!r} is already owned by {obj.parent.name!r}; "
                "reuse its original subject or create an independent object for this subject."
            )
        seen.add(id(obj))
        if isinstance(obj, CellLine):
            lines.append(obj)
            pending.extend(_references(obj.parent_cell_line))
        else:
            cultures.append(obj)
            pending.extend(_references(obj.source_lines))
            pending.extend(_references(obj.parent_cultures))
        for variant in obj.genetic_variants.values():
            application = variant.related_application
            if application is None:
                continue
            if not isinstance(application, ConstructApplication):
                raise TypeError("GeneticVariant.related_application must target a ConstructApplication.")
            if application.parent is not None:
                if not isinstance(application.parent, (CellLine, CellCulture)):
                    raise ValueError(
                        f"ConstructApplication {application.name!r} must be owned by a CellLine or CellCulture; "
                        "attach it using that object's construct_applications collection."
                    )
                pending.append(application.parent)
            record = applications.setdefault(id(application), (application, {}))
            record[1][id(obj)] = obj

    _check_names(lines + cultures, "CellCultureSubject", reserved=("culture",))
    attachments = []
    additions = {}
    for application, referring_owners in applications.values():
        if application.parent is not None:
            continue
        if len(referring_owners) != 1:
            owners = ", ".join(repr(owner.name) for owner in referring_owners.values())
            raise ValueError(
                f"ConstructApplication {application.name!r} is referenced from multiple biological owners ({owners}); "
                "attach it explicitly to the appropriate CellLine or CellCulture construct_applications collection."
            )
        owner = next(iter(referring_owners.values()))
        attachments.append((owner, application))
        additions.setdefault(id(owner), []).append(application)
    for owner in lines + cultures:
        _check_names(list(owner.children) + additions.get(id(owner), []), repr(owner.name))
    return lines, cultures, attachments
