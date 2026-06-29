"""PyNWB bindings for the ndx-cell-culture extension."""

from pathlib import Path

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
CellLineParentRelation = get_class("CellLineParentRelation", "ndx-cell-culture")
CellCultureSourceLineRelation = get_class("CellCultureSourceLineRelation", "ndx-cell-culture")
CellCultureParentRelation = get_class("CellCultureParentRelation", "ndx-cell-culture")
GeneticVariant = get_class("GeneticVariant", "ndx-cell-culture")
ConstructApplication = get_class("ConstructApplication", "ndx-cell-culture")
CultureProtocol = get_class("CultureProtocol", "ndx-cell-culture")
CultureExperimentContext = get_class("CultureExperimentContext", "ndx-cell-culture")
ExperimentContext = get_class("ExperimentContext", "ndx-cell-culture")
Pharmacology = get_class("Pharmacology", "ndx-cell-culture")


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
    "CellLineParentRelation",
    "CellCultureSourceLineRelation",
    "CellCultureParentRelation",
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
