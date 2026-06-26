"""Validation helpers for ndx-cell-culture recommended terms."""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Set, Tuple


RecommendedTerms = Mapping[str, Mapping[str, Set[str]]]


RECOMMENDED_TERMS: RecommendedTerms = {
    "CellCulture": {
        "culture_type": {
            "dissociated_culture",
            "spheroid",
            "organoid",
            "assembloid",
            "slice",
            "explant",
            "other",
        },
        "culture_subtype": {
            "cortical",
            "thalamic",
            "midbrain",
            "hippocampal",
            "retinal",
            "spinal",
            "assembloid",
            "tumor_organoid",
            "other",
        },
        "age_reference": {
            "days_in_vitro",
            "days_post_induction",
            "days_post_aggregation",
            "days_post_differentiation",
            "days_since_plated",
            "days_since_sectioning",
            "other",
        },
    },
    "CellLine": {
        "cell_line_type": {
            "donor",
            "parental_cell_line",
            "derived_cell_line",
            "immortalized_line",
            "other",
        },
        "cell_source_type": {
            "iPSC",
            "ESC",
            "primary_tissue",
            "primary_cells",
            "tumor_line",
            "immortalized_line",
            "other",
        },
        "clonal_status": {"clonal", "polyclonal", "mixed", "unknown"},
    },
    "GeneticVariant": {
        "edit_type": {
            "knockout",
            "knockin",
            "point_mutation",
            "deletion",
            "duplication",
            "inversion",
            "tag_insertion",
            "reporter_insertion",
            "CRISPRi_targeting",
            "CRISPRa_targeting",
            "other",
        },
        "method": {
            "CRISPR-Cas9",
            "base_editing",
            "prime_editing",
            "TALEN",
            "ZFNs",
            "homologous_recombination",
            "other",
        },
        "delivery_method": {
            "RNP",
            "plasmid",
            "lentivirus",
            "AAV",
            "electroporation",
            "lipofection",
            "other",
        },
        "zygosity_or_edit_state": {
            "heterozygous",
            "homozygous",
            "biallelic",
            "hemizygous",
            "mosaic",
            "unknown",
            "other",
        },
        "validation_status": {"planned", "screened", "validated", "failed", "unknown"},
        "validation_method": {
            "Sanger",
            "amplicon_seq",
            "WGS",
            "WES",
            "ONT",
            "ddPCR",
            "PCR",
            "fluorescence imaging",
            "other",
        },
    },
    "ConstructApplication": {
        "delivery_route": {"transduction", "transfection", "microinjection", "cell_fusion", "other"},
        "delivery_mechanism": {
            "lipofection",
            "polymer_transfection",
            "calcium_phosphate",
            "electroporation",
            "nucleofection",
            "nanoparticle_mediated",
            "other",
        },
        "vector_type": {
            "AAV",
            "lentivirus",
            "retrovirus",
            "plasmid",
            "transposon",
            "RNP",
            "minicircle_dna",
            "linear_dna",
            "rna",
            "mrna",
            "sirna",
            "crispr_rna",
            "adenovirus",
            "baculovirus",
            "herpes_simplex_virus",
            "other",
        },
        "genomic_persistence_state": {
            "genomically_integrated",
            "episomal_or_extragenomic",
            "transient_nonintegrating",
            "unknown",
            "other",
        },
        "age_modified_reference": {
            "days_in_vitro",
            "days_post_induction",
            "days_post_aggregation",
            "days_post_differentiation",
            "days_since_plated",
            "days_since_sectioning",
            "other",
        },
        "expression_status": {"planned", "observed", "validated", "failed", "unknown"},
        "validation_method": {
            "Sanger",
            "amplicon_seq",
            "WGS",
            "WES",
            "ONT",
            "ddPCR",
            "PCR",
            "fluorescence imaging",
            "other",
        },
    },
    "ExperimentContext": {
        "age_reference": {
            "days_in_vitro",
            "days_post_induction",
            "days_post_aggregation",
            "days_post_differentiation",
            "days_since_plated",
            "days_since_sectioning",
            "other",
        },
        "recording_platform": {"MEA", "patch_clamp", "calcium_imaging", "multimodal", "other"},
    },
    "Pharmacology": {
        "concentration_unit": {"M", "mM", "uM", "nM", "pM", "%", "mg/mL", "ug/mL", "ng/mL", "other"},
    },
    "CellLineParentRelation": {
        "relationship_type": {"derived_from", "cloned_from", "reprogrammed_from", "edited_from", "other"},
    },
    "CellCultureSourceLineRelation": {
        "role": {"primary_source", "component", "control", "other"},
    },
    "CellCultureParentRelation": {
        "relationship_type": {"derived_from", "sliced_from", "assembled_from", "fused_with", "co_cultured_with", "other"},
    },
}


@dataclass(frozen=True)
class RecommendedTermIssue:
    """A recommended-term validation issue."""

    object_type: str
    object_name: str
    field: str
    value: str
    allowed_values: Tuple[str, ...]

    @property
    def message(self) -> str:
        allowed = ", ".join(self.allowed_values)
        return (
            f"{self.object_type} '{self.object_name}' has non-recommended value "
            f"{self.field}={self.value!r}; expected one of: {allowed}"
        )


def validate_recommended_terms(container: Any, terms: RecommendedTerms = RECOMMENDED_TERMS) -> List[RecommendedTermIssue]:
    """Return recommended-term issues found under an NWB container.

    The extension schema intentionally stores controlled-vocabulary-like fields
    as text attributes. This helper provides opt-in machine checking for labs
    that want stronger validation before sharing or depositing data.
    """

    issues: List[RecommendedTermIssue] = []
    for obj in _iter_containers(container):
        object_type = _object_type(obj)
        field_terms = terms.get(object_type)
        if not field_terms:
            continue
        object_name = str(getattr(obj, "name", "<unnamed>"))
        for field, allowed_values in field_terms.items():
            value = _field_value(obj, field)
            if value is None or value == "":
                continue
            if str(value) not in allowed_values:
                issues.append(
                    RecommendedTermIssue(
                        object_type=object_type,
                        object_name=object_name,
                        field=field,
                        value=str(value),
                        allowed_values=tuple(sorted(allowed_values)),
                    )
                )
    return issues


def _field_value(obj: Any, field: str) -> Optional[Any]:
    try:
        return getattr(obj, field)
    except AttributeError:
        return None


def _object_type(obj: Any) -> str:
    value = getattr(obj, "neurodata_type", None)
    if value:
        return str(value)
    return obj.__class__.__name__


def _iter_containers(root: Any) -> Iterable[Any]:
    seen: Set[int] = set()
    stack = [root]
    while stack:
        obj = stack.pop()
        obj_id = id(obj)
        if obj_id in seen:
            continue
        seen.add(obj_id)
        yield obj

        children = getattr(obj, "children", ())
        if isinstance(children, dict):
            stack.extend(children.values())
        else:
            stack.extend(children)
