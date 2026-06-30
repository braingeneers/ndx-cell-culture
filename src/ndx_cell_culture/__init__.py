"""PyNWB bindings for the ndx-cell-culture extension."""

from pathlib import Path

from hdmf.common import VectorData
from hdmf.utils import docval, get_docval, popargs
from importlib_resources import files
from pynwb import get_class, load_namespaces

from .validation import RECOMMENDED_TERMS, RecommendedTermIssue, validate_recommended_terms


def _namespace_path() -> Path:
    package_root = files(__name__)
    installed_path = package_root / "spec" / "ndx-cell-culture.namespace.yaml"
    if installed_path.exists():
        return Path(str(installed_path))

    editable_path = Path(__file__).resolve().parents[2] / "spec" / "ndx-cell-culture.namespace.yaml"
    if editable_path.exists():
        return editable_path

    raise FileNotFoundError("Could not locate ndx-cell-culture.namespace.yaml")


load_namespaces(str(_namespace_path()))

CellCultureSubject = get_class("CellCultureSubject", "ndx-cell-culture")
CellCulture = get_class("CellCulture", "ndx-cell-culture")
CellLine = get_class("CellLine", "ndx-cell-culture")
GeneticVariant = get_class("GeneticVariant", "ndx-cell-culture")
ConstructApplication = get_class("ConstructApplication", "ndx-cell-culture")
CultureProtocol = get_class("CultureProtocol", "ndx-cell-culture")
CultureExperimentContext = get_class("CultureExperimentContext", "ndx-cell-culture")
ExperimentContext = get_class("ExperimentContext", "ndx-cell-culture")
Pharmacology = get_class("Pharmacology", "ndx-cell-culture")


def _as_reference_vector(name, description, value):
    if value is None or isinstance(value, VectorData):
        return value
    if isinstance(value, (list, tuple)):
        data = list(value)
    else:
        data = [value]
    if not data:
        return None
    return VectorData(name=name, description=description, data=data)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _same_container(left, right):
    if left is right:
        return True
    if left is None or right is None:
        return False
    for attr in ("object_id", "name"):
        left_value = getattr(left, attr, None)
        right_value = getattr(right, attr, None)
        if left_value and right_value and left_value == right_value:
            return True
    return False


def _dedupe_containers(values):
    deduped = []
    for value in _as_list(values):
        if not any(_same_container(value, existing) for existing in deduped):
            deduped.append(value)
    return deduped


_original_cell_line_init = CellLine.__init__
_cell_line_docval = []
for _arg in get_docval(_original_cell_line_init):
    _arg = dict(_arg)
    if _arg["name"] == "parent_cell_line":
        _arg["type"] = (CellLine, VectorData)
        _arg["doc"] = "Parent or source CellLine for a derived line."
    _cell_line_docval.append(_arg)


@docval(*_cell_line_docval)
def _cell_line_init(self, **kwargs):
    parent_cell_line = popargs("parent_cell_line", kwargs)
    parent_cell_line = _as_reference_vector(
        "parent_cell_line",
        "Parent or source CellLine for a derived line.",
        parent_cell_line,
    )
    if parent_cell_line is not None:
        kwargs["parent_cell_line"] = parent_cell_line
    _original_cell_line_init(self, **kwargs)


_original_cell_culture_init = CellCulture.__init__
_cell_culture_docval = []
for _arg in get_docval(_original_cell_culture_init):
    _arg = dict(_arg)
    if _arg["name"] == "source_lines":
        _arg["type"] = (CellLine, VectorData, list, tuple)
        _arg["doc"] = "Source CellLine or lines used to create this culture."
    elif _arg["name"] == "parent_cultures":
        _arg["type"] = (CellCulture, VectorData, list, tuple)
        _arg["doc"] = "Parent or input CellCulture objects used to derive this culture."
    _cell_culture_docval.append(_arg)


@docval(*_cell_culture_docval)
def _cell_culture_init(self, **kwargs):
    source_lines, parent_cultures = popargs("source_lines", "parent_cultures", kwargs)
    source_lines = _as_reference_vector(
        "source_lines",
        "Source CellLine or lines used to create this culture.",
        source_lines,
    )
    parent_cultures = _as_reference_vector(
        "parent_cultures",
        "Parent or input CellCulture objects used to derive this culture.",
        parent_cultures,
    )
    if source_lines is not None:
        kwargs["source_lines"] = source_lines
    if parent_cultures is not None:
        kwargs["parent_cultures"] = parent_cultures
    _original_cell_culture_init(self, **kwargs)


CellLine.__init__ = _cell_line_init
CellCulture.__init__ = _cell_culture_init


_PUBLIC_RELATED_CULTURES_CONTAINER = "related_cultures"
_GENERATED_SUBJECT_CULTURES_CONTAINER = "cell_cultures"
_original_cell_culture_subject_init = CellCultureSubject.__init__
_cell_culture_subject_docval = []
for _arg in get_docval(_original_cell_culture_subject_init):
    _cell_culture_subject_docval.append(_arg)
    if _arg["name"] == _GENERATED_SUBJECT_CULTURES_CONTAINER:
        _alias_arg = dict(_arg)
        _alias_arg["name"] = _PUBLIC_RELATED_CULTURES_CONTAINER
        _alias_arg["doc"] = "Related or parent CellCulture objects needed to interpret the subject culture provenance."
        _cell_culture_subject_docval.append(_alias_arg)


@docval(*_cell_culture_subject_docval)
def _cell_culture_subject_init(self, **kwargs):
    """Accept related/parent cultures using a subject-oriented public name."""

    culture, cell_cultures, related_cultures = popargs(
        "culture",
        _GENERATED_SUBJECT_CULTURES_CONTAINER,
        _PUBLIC_RELATED_CULTURES_CONTAINER,
        kwargs,
    )
    subject_cultures = []
    if getattr(culture, "name", None) == "culture":
        raise ValueError("CellCulture.name cannot be 'culture' when used as CellCultureSubject.culture; use a stable identifier-style name and store the biological identifier in culture_id.")
    for subject_culture in _dedupe_containers(_as_list(cell_cultures) + _as_list(related_cultures)):
        if not _same_container(subject_culture, culture):
            subject_cultures.append(subject_culture)
    if culture is not None and getattr(culture, "parent", None) is None:
        subject_cultures.insert(0, culture)
    kwargs["culture"] = culture
    if subject_cultures:
        kwargs[_GENERATED_SUBJECT_CULTURES_CONTAINER] = subject_cultures
    _original_cell_culture_subject_init(self, **kwargs)
    if culture is not None and culture.name not in self.cell_cultures:
        self.add_cell_cultures(culture)


def _get_related_cultures(self):
    return getattr(self, _GENERATED_SUBJECT_CULTURES_CONTAINER)


CellCultureSubject.__init__ = _cell_culture_subject_init
CellCultureSubject.related_cultures = property(_get_related_cultures)
CellCultureSubject.add_related_cultures = getattr(
    CellCultureSubject,
    "add_" + _GENERATED_SUBJECT_CULTURES_CONTAINER,
)
CellCultureSubject.create_related_cultures = getattr(
    CellCultureSubject,
    "create_" + _GENERATED_SUBJECT_CULTURES_CONTAINER,
)
CellCultureSubject.get_related_cultures = getattr(
    CellCultureSubject,
    "get_" + _GENERATED_SUBJECT_CULTURES_CONTAINER,
)


_PUBLIC_PHARMACOLOGY_CONTAINER = "pharmacologies"
_GENERATED_PHARMACOLOGY_CONTAINER = "pharmacology" + "s"
_original_culture_experiment_context_init = CultureExperimentContext.__init__
_culture_experiment_context_docval = []
for _arg in get_docval(_original_culture_experiment_context_init):
    _culture_experiment_context_docval.append(_arg)
    if _arg["name"] == _GENERATED_PHARMACOLOGY_CONTAINER:
        _alias_arg = dict(_arg)
        _alias_arg["name"] = _PUBLIC_PHARMACOLOGY_CONTAINER
        _alias_arg["doc"] = "Repeated Pharmacology records."
        _culture_experiment_context_docval.append(_alias_arg)


@docval(*_culture_experiment_context_docval)
def _culture_experiment_context_init(self, **kwargs):
    """Accept repeated Pharmacology records using the public plural spelling."""

    pharmacologies = popargs(_PUBLIC_PHARMACOLOGY_CONTAINER, kwargs)
    if pharmacologies is not None:
        generated_value = kwargs.get(_GENERATED_PHARMACOLOGY_CONTAINER)
        if generated_value:
            raise ValueError("Use pharmacologies for repeated Pharmacology records.")
        kwargs[_GENERATED_PHARMACOLOGY_CONTAINER] = pharmacologies
    _original_culture_experiment_context_init(self, **kwargs)


def _get_pharmacologies(self):
    return getattr(self, _GENERATED_PHARMACOLOGY_CONTAINER)


CultureExperimentContext.__init__ = _culture_experiment_context_init
CultureExperimentContext.pharmacologies = property(_get_pharmacologies)
CultureExperimentContext.add_pharmacologies = getattr(
    CultureExperimentContext,
    "add_" + _GENERATED_PHARMACOLOGY_CONTAINER,
)
CultureExperimentContext.create_pharmacologies = getattr(
    CultureExperimentContext,
    "create_" + _GENERATED_PHARMACOLOGY_CONTAINER,
)
CultureExperimentContext.get_pharmacologies = getattr(
    CultureExperimentContext,
    "get_" + _GENERATED_PHARMACOLOGY_CONTAINER,
)

__all__ = [
    "CellCultureSubject",
    "CellCulture",
    "CellLine",
    "GeneticVariant",
    "ConstructApplication",
    "CultureProtocol",
    "CultureExperimentContext",
    "ExperimentContext",
    "Pharmacology",
    "RECOMMENDED_TERMS",
    "RecommendedTermIssue",
    "validate_recommended_terms",
]
