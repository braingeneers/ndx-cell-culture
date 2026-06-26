# -*- coding: utf-8 -*-
"""Generate the ndx-cell-culture NWB extension schema."""

from pathlib import Path

from pynwb.spec import (
    NWBAttributeSpec,
    NWBGroupSpec,
    NWBLinkSpec,
    NWBNamespaceBuilder,
    export_spec,
)


NAMESPACE = "ndx-cell-culture"
VERSION = "1.0rc1"


def attr(name, doc, required=True, dtype="text"):
    return NWBAttributeSpec(name=name, doc=doc, dtype=dtype, required=required)


def text_attrs(fields):
    return [attr(name, doc, required) for name, required, doc in fields]


def object_link(name, target_type, doc, quantity="?"):
    return NWBLinkSpec(name=name, doc=doc, target_type=target_type, quantity=quantity)


def build_specs():
    genetic_variant = NWBGroupSpec(
        neurodata_type_def="GeneticVariant",
        neurodata_type_inc="NWBContainer",
        doc=(
            "Stable or defining engineered genomic change attached to a CellLine or CellCulture. "
            "Use for engineered edits, not every raw sequencing variant."
        ),
        attributes=text_attrs(
            [
                ("variant_id", True, "Stable variant identifier."),
                ("target_symbol", True, "Gene symbol or target name."),
                ("target_coordinates", False, "Genomic coordinates, transcript notation, or locus notation."),
                ("edit_type", True, "Recommended terms include knockout, knockin, point_mutation, deletion, duplication, inversion, tag_insertion, reporter_insertion, CRISPRi_targeting, CRISPRa_targeting, other."),
                ("edit_description", False, "Human-readable edit description."),
                ("method", True, "Engineering method, e.g. CRISPR-Cas9, base_editing, prime_editing, TALEN, ZFNs, homologous_recombination, other."),
                ("delivery_method", False, "Method used to deliver edit machinery, e.g. RNP, plasmid, lentivirus, AAV, electroporation, lipofection, other."),
                ("zygosity_or_edit_state", False, "Observed zygosity or edit state, e.g. heterozygous, homozygous, biallelic, hemizygous, mosaic, unknown, other."),
                ("validation_status", False, "Validation state, e.g. planned, screened, validated, failed, unknown."),
                ("validation_method", False, "Assay or method used for validation, e.g. Sanger, amplicon_seq, WGS, WES, ONT, ddPCR, PCR, fluorescence imaging, other."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        links=[
            object_link("related_application", "ConstructApplication", "Link to the ConstructApplication related to this variant, when applicable."),
        ],
    )

    construct_application = NWBGroupSpec(
        neurodata_type_def="ConstructApplication",
        neurodata_type_inc="NWBContainer",
        doc="Construct, vector, reagent, reporter, or perturbation applied to a CellLine or CellCulture.",
        attributes=text_attrs(
            [
                ("application_id", True, "Stable construct application identifier."),
                ("source", False, "Construct source, catalog, plasmid, vendor, manufacturer, person, or lab."),
                ("delivery_route", False, "Broad route, e.g. transduction, transfection, microinjection, cell_fusion, other."),
                ("delivery_mechanism", False, "Technical mechanism, e.g. lipofection, polymer_transfection, calcium_phosphate, electroporation, nucleofection, nanoparticle_mediated, other. Do not use microinjection here."),
                ("vector_type", True, "Vector or reagent class, e.g. AAV, lentivirus, retrovirus, plasmid, transposon, RNP, minicircle_dna, linear_dna, rna, mrna, sirna, crispr_rna, adenovirus, baculovirus, herpes_simplex_virus, other."),
                ("payload", True, "Gene, tool, cassette, or reagent delivered."),
                ("promoter", False, "Promoter driving expression, if known."),
                ("genomic_persistence_state", False, "Persistence state, e.g. genomically_integrated, episomal_or_extragenomic, transient_nonintegrating, unknown, other."),
                ("application_time_relative_to_recording", False, "Human-readable time relative to recording."),
                ("age_modified", False, "Culture age when application occurred."),
                ("age_modified_reference", False, "Reference event for age_modified."),
                ("expression_status", False, "Expression or delivery observation state, e.g. planned, observed, validated, failed, unknown."),
                ("validation_method", False, "Assay or observation used to confirm expression or delivery."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
    )

    cell_line = NWBGroupSpec(
        neurodata_type_def="CellLine",
        neurodata_type_inc="NWBContainer",
        doc="Donor, parental line, derived line, immortalized line, or other cell-line lineage node.",
        attributes=text_attrs(
            [
                ("cell_line_id", True, "Stable cell-line identifier."),
                ("cell_line_type", True, "Recommended terms: donor, parental_cell_line, derived_cell_line, immortalized_line, other."),
                ("sample_label", True, "Human-readable label."),
                ("species", True, "Species of the source line; formal binomial preferred."),
                ("cell_source_type", True, "Recommended terms: iPSC, ESC, primary_tissue, primary_cells, tumor_line, immortalized_line, other."),
                ("cell_line_name", False, "Canonical or common cell-line name."),
                ("cell_line_rrid", False, "Cell-line RRID when available."),
                ("clone_id", False, "Clone identifier for a clonal derived line."),
                ("clonal_status", False, "Clonal state of the line, e.g. clonal, polyclonal, mixed, unknown."),
                ("passage_number", False, "Passage number or passage label. Do not use culture-age fields on CellLine."),
                ("disease_or_diagnosis", False, "Disease background or diagnosis."),
                ("reference_genome", False, "Assembly or annotation context, e.g. GRCh38; not a substitute for Subject.genotype."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        groups=[
            NWBGroupSpec(neurodata_type_inc="GeneticVariant", doc="Genetic variants attached to this cell line.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="ConstructApplication", doc="Construct applications attached to this cell line.", quantity="*"),
        ],
    )

    culture_protocol = NWBGroupSpec(
        neurodata_type_def="CultureProtocol",
        neurodata_type_inc="NWBContainer",
        doc="Structured derivation or preparation protocol metadata for a CellCulture.",
        attributes=text_attrs(
            [
                ("protocol_id", True, "Stable protocol identifier."),
                ("protocol_name", False, "Human-readable protocol name."),
                ("protocol_uri", False, "Direct protocol URI when available."),
                ("protocol_doi", False, "Protocol DOI when available."),
                ("protocol_version", False, "Protocol version or revision label."),
                ("patterning_summary", False, "Short patterning summary, not a complete protocol specification."),
                ("media_summary", False, "Short media summary."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
    )

    cell_culture = NWBGroupSpec(
        neurodata_type_def="CellCulture",
        neurodata_type_inc="NWBContainer",
        doc="Biological cultured preparation being recorded or described.",
        attributes=text_attrs(
            [
                ("culture_id", True, "Stable culture identifier."),
                ("culture_type", True, "Recommended terms: dissociated_culture, spheroid, organoid, assembloid, slice, explant, other. batch is prohibited."),
                ("sample_label", True, "Human-readable culture label."),
                ("species", True, "Culture-level convenience/search species value; may mirror CellCultureSubject.species."),
                ("culture_subtype", False, "Regional or subtype identity, e.g. cortical, thalamic, midbrain, hippocampal, retinal, spinal, assembloid, tumor_organoid, other."),
                ("batch_label", False, "Lightweight grouping/search label only; not a standalone object."),
                ("age", False, "Culture age. Prefer ISO-8601 duration such as P120D; pilot terms like day45 are acceptable."),
                ("age_reference", False, "Reference event for culture age, e.g. days_post_induction or days_post_aggregation."),
                ("disease_or_diagnosis", False, "Disease background or diagnosis."),
                ("reference_genome", False, "Assembly/annotation context for culture-specific cases or cultures without a modeled source line."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        groups=[
            NWBGroupSpec(neurodata_type_inc="GeneticVariant", doc="Genetic variants attached to this culture.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="ConstructApplication", doc="Construct applications attached to this culture.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="CultureProtocol", doc="Structured culture derivation/preparation protocol.", quantity="?"),
        ],
    )

    cell_culture_subject = NWBGroupSpec(
        neurodata_type_def="CellCultureSubject",
        neurodata_type_inc="Subject",
        doc="NWB Subject wrapper for a recorded or described cultured neural preparation.",
        links=[
            object_link("culture", "CellCulture", "Link to the recorded or described cataloged CellCulture.", quantity=1),
        ],
    )

    cell_line_parent_relation = NWBGroupSpec(
        neurodata_type_def="CellLineParentRelation",
        neurodata_type_inc="NWBContainer",
        doc="Relationship edge linking a child CellLine to a parent CellLine.",
        attributes=text_attrs(
            [
                ("relation_id", True, "Stable relation identifier."),
                ("relationship_type", False, "Recommended terms include derived_from, cloned_from, reprogrammed_from, edited_from, other."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        links=[
            object_link("child_cell_line", "CellLine", "Child or derived CellLine in the relationship.", quantity=1),
            object_link("parent_cell_line", "CellLine", "Parent or source CellLine in the relationship.", quantity=1),
        ],
    )

    cell_culture_source_line_relation = NWBGroupSpec(
        neurodata_type_def="CellCultureSourceLineRelation",
        neurodata_type_inc="NWBContainer",
        doc="Relationship edge linking a CellCulture to one source CellLine.",
        attributes=text_attrs(
            [
                ("relation_id", True, "Stable relation identifier."),
                ("role", False, "Recommended terms include primary_source, component, control, other."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        links=[
            object_link("culture", "CellCulture", "CellCulture that used this source line.", quantity=1),
            object_link("source_line", "CellLine", "Source CellLine for the culture.", quantity=1),
        ],
    )

    cell_culture_parent_relation = NWBGroupSpec(
        neurodata_type_def="CellCultureParentRelation",
        neurodata_type_inc="NWBContainer",
        doc="Relationship edge linking a CellCulture to one parent CellCulture.",
        attributes=text_attrs(
            [
                ("relation_id", True, "Stable relation identifier."),
                ("relationship_type", False, "Culture-to-culture relationship type."),
                ("notes", False, "Free-text remarks."),
            ]
        ),
        links=[
            object_link("child_culture", "CellCulture", "Child or derived CellCulture.", quantity=1),
            object_link("parent_culture", "CellCulture", "Parent or input CellCulture.", quantity=1),
        ],
    )

    experiment_context = NWBGroupSpec(
        neurodata_type_def="ExperimentContext",
        neurodata_type_inc="NWBContainer",
        doc="Recording-time or session-level metadata separate from stable biological identity.",
        attributes=[
            *text_attrs(
                [
                    ("experiment_id", True, "Stable experiment context identifier."),
                    ("session_id", False, "Acquisition/session label."),
                    ("age_at_recording", True, "Culture age at recording; separate from CellCulture.age and inherited Subject.age."),
                    ("age_reference", False, "Reference event for age_at_recording."),
                    ("recording_platform", True, "Recommended terms: MEA, patch_clamp, calcium_imaging, multimodal, other."),
                    ("media_or_bath", False, "Media, bath solution, or ACSF during recording."),
                    ("experimental_setup", False, "Short recording setup summary."),
                    ("notes", False, "Free-text remarks."),
                ]
            ),
            attr("temperature_c", "Recording temperature in Celsius.", required=False, dtype="float32"),
            attr("recording_duration_s", "Recording duration in seconds.", required=False, dtype="float32"),
            attr("spontaneous_activity", "Search flag for spontaneous activity.", required=False, dtype="bool"),
            attr("electrical_stimulation", "Search flag for electrical stimulation; detailed waveforms belong in core NWB stimulus data.", required=False, dtype="bool"),
            attr("optical_stimulation", "Search flag for optical stimulation; detailed waveforms belong in core NWB stimulus data.", required=False, dtype="bool"),
            attr("pharmacology_present", "Search flag for pharmacology presence.", required=False, dtype="bool"),
        ],
        links=[
            NWBLinkSpec(doc="CellCultureSubject recorded in this experiment.", target_type="CellCultureSubject", name="subject", quantity=1),
            NWBLinkSpec(doc="CellCulture recorded in this experiment.", target_type="CellCulture", name="culture", quantity=1),
            NWBLinkSpec(doc="Core NWB Device object relevant to this recording context.", target_type="Device", name="device", quantity="?"),
        ],
    )

    pharmacology = NWBGroupSpec(
        neurodata_type_def="Pharmacology",
        neurodata_type_inc="NWBContainer",
        doc="Repeatable pharmacological intervention linked to an ExperimentContext.",
        attributes=text_attrs(
            [
                ("pharmacology_id", True, "Stable pharmacology row identifier."),
                ("agent", True, "Compound or reagent name."),
                ("concentration", False, "Flexible concentration value or range for search/review."),
                ("concentration_unit", False, "Recommended terms: M, mM, uM, nM, pM, %, mg/mL, ug/mL, ng/mL, other."),
                ("purpose", False, "Purpose or interpretation note."),
                ("notes", False, "Free-text remarks."),
            ]
        )
        + [
            attr("start_time_s", "Start time relative to recording start.", required=False, dtype="float32"),
            attr("end_time_s", "End time relative to recording start.", required=False, dtype="float32"),
        ],
        links=[
            NWBLinkSpec(doc="Experiment context this pharmacological intervention belongs to.", target_type="ExperimentContext", name="experiment", quantity=1),
        ],
    )

    culture_experiment_context = NWBGroupSpec(
        neurodata_type_def="CultureExperimentContext",
        neurodata_type_inc="LabMetaData",
        doc="LabMetaData container for culture catalogs, provenance, and context.",
        groups=[
            NWBGroupSpec(neurodata_type_inc="CellLine", doc="Reusable CellLine catalog entries for this NWB file.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="CellCulture", doc="Reusable CellCulture catalog entries for this NWB file.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="CellLineParentRelation", doc="CellLine-to-CellLine provenance relationships.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="CellCultureSourceLineRelation", doc="CellCulture-to-CellLine source relationships.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="CellCultureParentRelation", doc="CellCulture-to-CellCulture provenance relationships.", quantity="*"),
            NWBGroupSpec(neurodata_type_inc="ExperimentContext", doc="Recording/session context for this NWBFile.", quantity="?"),
            NWBGroupSpec(neurodata_type_inc="Pharmacology", doc="Pharmacological interventions linked to experiment contexts.", quantity="*"),
        ],
    )

    return [
        genetic_variant,
        construct_application,
        cell_line,
        culture_protocol,
        cell_culture,
        cell_culture_subject,
        cell_line_parent_relation,
        cell_culture_source_line_relation,
        cell_culture_parent_relation,
        experiment_context,
        pharmacology,
        culture_experiment_context,
    ]


def main():
    ns_builder = NWBNamespaceBuilder(
        name=NAMESPACE,
        version=VERSION,
        doc="NWB extension for cultured neural preparations, organoids, cell lines, variants, constructs, protocols, recording context, and pharmacology.",
        author=["Braingeneers"],
        contact=["braingeneers@ucsc.edu"],
    )
    ns_builder.include_namespace("core")
    output_dir = str((Path(__file__).parent.parent.parent / "spec").absolute())
    export_spec(ns_builder, build_specs(), output_dir)


if __name__ == "__main__":
    main()
