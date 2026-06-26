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


_original_culture_experiment_context_init = CultureExperimentContext.__init__
_culture_experiment_context_docval = []
for _arg in get_docval(_original_culture_experiment_context_init):
    _culture_experiment_context_docval.append(_arg)
    if _arg["name"] == "pharmacologys":
        _alias_arg = dict(_arg)
        _alias_arg["name"] = "pharmacologies"
        _alias_arg["doc"] = "Natural plural alias for pharmacologys."
        _culture_experiment_context_docval.append(_alias_arg)


@docval(*_culture_experiment_context_docval)
def _culture_experiment_context_init(self, **kwargs):
    """Accept the natural plural spelling for repeated Pharmacology children."""

    pharmacologies = popargs("pharmacologies", kwargs)
    if pharmacologies is not None:
        generated_value = kwargs.get("pharmacologys")
        if generated_value:
            raise ValueError("Use either pharmacologies or pharmacologys, not both.")
        kwargs["pharmacologys"] = pharmacologies
    _original_culture_experiment_context_init(self, **kwargs)


def _get_pharmacologies(self):
    return self.pharmacologys


CultureExperimentContext.__init__ = _culture_experiment_context_init
CultureExperimentContext.pharmacologies = property(_get_pharmacologies)
CultureExperimentContext.add_pharmacologies = CultureExperimentContext.add_pharmacologys
CultureExperimentContext.create_pharmacologies = CultureExperimentContext.create_pharmacologys
CultureExperimentContext.get_pharmacologies = CultureExperimentContext.get_pharmacologys

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
