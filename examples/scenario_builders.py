"""Reusable synthetic NWBFile builders for ndx-cell-culture scenarios."""

from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from ndx_cell_culture import (
    CellCulture,
    CellCultureParentRelation,
    CellCultureSourceLineRelation,
    CellCultureSubject,
    CellLine,
    CellLineParentRelation,
    ConstructApplication,
    CultureExperimentContext,
    CultureProtocol,
    ExperimentContext,
    GeneticVariant,
    Pharmacology,
)


SESSION_TIME = datetime(2026, 5, 12, tzinfo=tzlocal())


def _nwbfile(identifier, description):
    return NWBFile(
        session_description=description,
        identifier=identifier,
        session_start_time=SESSION_TIME,
    )


def _device(nwbfile, name, description):
    return nwbfile.create_device(name=name, description=description)


def _source_relation(relation_id, culture, source_line, role="primary_source"):
    return CellCultureSourceLineRelation(
        name=relation_id,
        relation_id=relation_id,
        culture=culture,
        source_line=source_line,
        role=role,
    )


def _line_parent_relation(relation_id, child_cell_line, parent_cell_line, relationship_type="derived_from"):
    return CellLineParentRelation(
        name=relation_id,
        relation_id=relation_id,
        child_cell_line=child_cell_line,
        parent_cell_line=parent_cell_line,
        relationship_type=relationship_type,
    )


def _culture_parent_relation(relation_id, child_culture, parent_culture, relationship_type):
    return CellCultureParentRelation(
        name=relation_id,
        relation_id=relation_id,
        child_culture=child_culture,
        parent_culture=parent_culture,
        relationship_type=relationship_type,
    )


def _add_context(
    nwbfile,
    *,
    cell_lines=None,
    cell_cultures=None,
    cell_line_parent_relations=None,
    cell_culture_source_line_relations=None,
    cell_culture_parent_relations=None,
    experiment_context=None,
    pharmacologys=None,
):
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(
            name="culture_experiment_context",
            cell_lines=cell_lines or [],
            cell_cultures=cell_cultures or [],
            cell_line_parent_relations=cell_line_parent_relations or [],
            cell_culture_source_line_relations=cell_culture_source_line_relations or [],
            cell_culture_parent_relations=cell_culture_parent_relations or [],
            experiment_context=experiment_context,
            pharmacologys=pharmacologys or [],
        )
    )


def build_basic_organoid():
    variant = GeneticVariant(
        name="VAR-EX-SYNGAP1-KO-01",
        variant_id="VAR-EX-SYNGAP1-KO-01",
        target_symbol="SYNGAP1",
        target_coordinates="chr6:33424312-33424345",
        edit_type="knockout",
        edit_description="exon 8 frameshift indel",
        method="CRISPR-Cas9",
        delivery_method="RNP",
        zygosity_or_edit_state="biallelic",
        validation_status="validated",
        validation_method="amplicon_seq",
    )
    construct = ConstructApplication(
        name="APP-EX-LV-GCAMP6F-01",
        application_id="APP-EX-LV-GCAMP6F-01",
        delivery_route="transduction",
        vector_type="lentivirus",
        payload="GCaMP6f",
        promoter="hSyn",
        genomic_persistence_state="genomically_integrated",
        application_time_relative_to_recording="21 days before recording",
        age_modified="P99D",
        age_modified_reference="days_post_induction",
        expression_status="validated",
        validation_method="fluorescence imaging",
    )
    line = CellLine(
        name="CL-EX-SYNGAP1-KO-C7",
        cell_line_id="CL-EX-SYNGAP1-KO-C7",
        cell_line_type="derived_cell_line",
        sample_label="Example SYNGAP1 KO clone C7",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clone_id="C7",
        clonal_status="clonal",
        reference_genome="GRCh38",
        genetic_variants=[variant],
    )
    protocol = CultureProtocol(
        name="PROTO-EX-CORT-V3",
        protocol_id="PROTO-EX-CORT-V3",
        protocol_name="Cortical organoid v3",
        protocol_uri="https://www.protocols.io/example",
        protocol_doi="10.1234/example",
        protocol_version="v3.1",
        patterning_summary="dual-SMAD inhibition, forebrain patterning",
        media_summary="neural induction + maturation media",
    )
    culture = CellCulture(
        name="CULT-EX-ORG-001",
        culture_id="CULT-EX-ORG-001",
        culture_type="organoid",
        sample_label="Example organoid A",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
        construct_applications=[construct],
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-ORG-001",
        species="Homo sapiens",
        sex="F",
        description="Recorded cortical organoid on MEA",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-EX-ORG-001", "Example organoid recording")
    nwbfile.subject = subject
    device = _device(nwbfile, "MaxTwo MX2-CHIP-17", "MEA recording system/chip")
    experiment = ExperimentContext(
        name="EXP-EX-ORG-001",
        experiment_id="EXP-EX-ORG-001",
        subject=subject,
        culture=culture,
        session_id="2026-05-12-A",
        age_at_recording="P120D",
        age_reference="days_post_induction",
        recording_platform="MEA",
        media_or_bath="BrainPhys + supplements",
        temperature_c=37.0,
        recording_duration_s=1800.0,
        spontaneous_activity=True,
        electrical_stimulation=False,
        optical_stimulation=True,
        pharmacology_present=False,
        experimental_setup="spontaneous + blue light stimulation",
        device=device,
    )
    _add_context(
        nwbfile,
        cell_lines=[line],
        cell_cultures=[culture],
        cell_culture_source_line_relations=[_source_relation("REL-EX-ORG-SOURCE-001", culture, line)],
        experiment_context=experiment,
    )
    return nwbfile


def build_slice_patch_clamp():
    line = CellLine(
        name="CL-EX-SYNGAP1-KO-C7",
        cell_line_id="CL-EX-SYNGAP1-KO-C7",
        cell_line_type="derived_cell_line",
        sample_label="Example SYNGAP1 KO clone C7",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clone_id="C7",
        clonal_status="clonal",
    )
    parent_organoid = CellCulture(
        name="CULT-EX-ORG-001",
        culture_id="CULT-EX-ORG-001",
        culture_type="organoid",
        sample_label="Example parent organoid",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
    )
    construct = ConstructApplication(
        name="APP-EX-AAV-CHR2-01",
        application_id="APP-EX-AAV-CHR2-01",
        delivery_route="microinjection",
        vector_type="AAV",
        payload="ChR2(H134R)-EYFP",
        expression_status="observed",
    )
    slice_culture = CellCulture(
        name="CULT-EX-SLICE-001",
        culture_id="CULT-EX-SLICE-001",
        culture_type="slice",
        sample_label="Example slice A",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
        construct_applications=[construct],
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-SLICE-001",
        species="Homo sapiens",
        description="Example organoid-derived slice",
        culture=slice_culture,
    )
    nwbfile = _nwbfile("NWB-EX-SLICE-001", "Example organoid slice patch-clamp recording")
    nwbfile.subject = subject
    device = _device(nwbfile, "Axon Multiclamp 700B", "Patch-clamp amplifier")
    experiment = ExperimentContext(
        name="EXP-EX-SLICE-001",
        experiment_id="EXP-EX-SLICE-001",
        subject=subject,
        culture=slice_culture,
        age_at_recording="P120D",
        age_reference="days_post_induction",
        recording_platform="patch_clamp",
        media_or_bath="ACSF",
        temperature_c=32.0,
        recording_duration_s=900.0,
        spontaneous_activity=True,
        electrical_stimulation=True,
        optical_stimulation=False,
        pharmacology_present=True,
        device=device,
    )
    pharmacology = [
        Pharmacology(
            name="PHARM-EX-CNQX-01",
            pharmacology_id="PHARM-EX-CNQX-01",
            experiment=experiment,
            agent="CNQX",
            concentration="10",
            concentration_unit="uM",
            start_time_s=300.0,
            end_time_s=900.0,
        ),
        Pharmacology(
            name="PHARM-EX-APV-01",
            pharmacology_id="PHARM-EX-APV-01",
            experiment=experiment,
            agent="APV",
            concentration="50",
            concentration_unit="uM",
            start_time_s=300.0,
            end_time_s=900.0,
        ),
    ]
    _add_context(
        nwbfile,
        cell_lines=[line],
        cell_cultures=[parent_organoid, slice_culture],
        cell_culture_source_line_relations=[
            _source_relation("REL-EX-SLICE-SOURCE-001", slice_culture, line),
            _source_relation("REL-EX-ORG-SOURCE-001", parent_organoid, line),
        ],
        cell_culture_parent_relations=[
            _culture_parent_relation("REL-EX-SLICE-PARENT-001", slice_culture, parent_organoid, "sliced_from"),
        ],
        experiment_context=experiment,
        pharmacologys=pharmacology,
    )
    return nwbfile


def build_edited_ipsc_organoid_mea():
    parental = CellLine(
        name="SYN-iPSC-A",
        cell_line_id="SYN-iPSC-A",
        cell_line_type="parental_cell_line",
        sample_label="Synthetic iPSC line A",
        species="Homo sapiens",
        cell_source_type="iPSC",
        cell_line_name="SYN-iPSC-A",
        clonal_status="clonal",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
    )
    variant = GeneticVariant(
        name="VAR-SYN-GENE1-HET",
        variant_id="VAR-SYN-GENE1-HET",
        target_symbol="GENE1",
        edit_type="knockin",
        edit_description="synthetic heterozygous frameshift edit",
        method="CRISPR-Cas9",
        zygosity_or_edit_state="heterozygous",
        validation_status="screened",
        validation_method="ONT",
    )
    derived = CellLine(
        name="SYN-iPSC-A-GENE1-HET-C1",
        cell_line_id="SYN-iPSC-A-GENE1-HET-C1",
        cell_line_type="derived_cell_line",
        sample_label="Synthetic edited iPSC clone C1",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clone_id="C1",
        clonal_status="clonal",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
        genetic_variants=[variant],
    )
    protocol = CultureProtocol(
        name="PROTO-SYN-FOREBRAIN-001",
        protocol_id="PROTO-SYN-FOREBRAIN-001",
        protocol_name="Synthetic forebrain organoid protocol",
        patterning_summary="dual-SMAD inhibition w/ WNT inhibitor, forebrain patterning",
        media_summary="neural induction + maturation media",
    )
    culture = CellCulture(
        name="CULT-SYN-EDITED-ORG-001",
        culture_id="CULT-SYN-EDITED-ORG-001",
        culture_type="organoid",
        sample_label="Synthetic edited organoid 1",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="SYN-BATCH-1",
        age="day45",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-SYN-EDITED-ORG-001",
        species="Homo sapiens",
        sex="M",
        description="Synthetic edited organoid subject",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-SYN-EDITED-ORG-001", "Synthetic edited organoid MEA example")
    nwbfile.subject = subject
    device = _device(nwbfile, "Example MEA Device A", "MEA recording system")
    experiment = ExperimentContext(
        name="EXP-SYN-EDITED-MEA-001",
        experiment_id="EXP-SYN-EDITED-MEA-001",
        subject=subject,
        culture=culture,
        session_id="2026-03-09",
        age_at_recording="day7",
        age_reference="days_since_plated",
        recording_platform="MEA",
        media_or_bath="BrainPhys + supplements",
        temperature_c=37.0,
        recording_duration_s=600.0,
        spontaneous_activity=True,
        electrical_stimulation=False,
        optical_stimulation=False,
        pharmacology_present=False,
        device=device,
    )
    _add_context(
        nwbfile,
        cell_lines=[parental, derived],
        cell_cultures=[culture],
        cell_line_parent_relations=[
            _line_parent_relation("REL-SYN-LINE-PARENT-001", derived, parental, "edited_from"),
        ],
        cell_culture_source_line_relations=[
            _source_relation("REL-SYN-EDITED-ORG-SOURCE-001", culture, derived),
        ],
        experiment_context=experiment,
    )
    return nwbfile


def build_biological_metadata_only_organoid():
    parental = CellLine(
        name="SYN-iPSC-A",
        cell_line_id="SYN-iPSC-A",
        cell_line_type="parental_cell_line",
        sample_label="Synthetic iPSC line A",
        species="Homo sapiens",
        cell_source_type="iPSC",
        cell_line_name="SYN-iPSC-A",
        clonal_status="clonal",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
    )
    variant = GeneticVariant(
        name="VAR-SYN-GENE1-HET",
        variant_id="VAR-SYN-GENE1-HET",
        target_symbol="GENE1",
        edit_type="knockin",
        edit_description="synthetic heterozygous frameshift edit",
        method="CRISPR-Cas9",
        zygosity_or_edit_state="heterozygous",
        validation_status="screened",
        validation_method="ONT",
    )
    derived = CellLine(
        name="SYN-iPSC-A-GENE1-HET-C1",
        cell_line_id="SYN-iPSC-A-GENE1-HET-C1",
        cell_line_type="derived_cell_line",
        sample_label="Synthetic edited iPSC clone C1",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clone_id="C1",
        clonal_status="clonal",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
        genetic_variants=[variant],
    )
    protocol = CultureProtocol(
        name="PROTO-SYN-FOREBRAIN-002",
        protocol_id="PROTO-SYN-FOREBRAIN-002",
        protocol_name="Synthetic forebrain organoid protocol",
        patterning_summary="dual-SMAD inhibition w/ WNT inhibitor, forebrain patterning",
        media_summary="neural induction + maturation media",
    )
    culture = CellCulture(
        name="CULT-SYN-EDITED-ORG-002",
        culture_id="CULT-SYN-EDITED-ORG-002",
        culture_type="organoid",
        sample_label="Synthetic edited organoid 2",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="SYN-BATCH-1",
        age="day45",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="synthetic neurodevelopmental condition",
        reference_genome="GRCh38",
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-SYN-EDITED-ORG-002",
        species="Homo sapiens",
        sex="M",
        description="Synthetic edited organoid subject without recording context",
        culture=culture,
    )
    nwbfile = _nwbfile(
        "NWB-SYN-EDITED-ORG-002",
        "Synthetic edited organoid biological metadata example",
    )
    nwbfile.subject = subject
    _add_context(
        nwbfile,
        cell_lines=[parental, derived],
        cell_cultures=[culture],
        cell_line_parent_relations=[
            _line_parent_relation("REL-SYN-LINE-PARENT-002", derived, parental, "edited_from"),
        ],
        cell_culture_source_line_relations=[
            _source_relation("REL-SYN-EDITED-ORG-SOURCE-002", culture, derived),
        ],
    )
    return nwbfile


def build_pharmacology_titration_organoid():
    line = CellLine(
        name="SYN-ESC-A",
        cell_line_id="SYN-ESC-A",
        cell_line_type="parental_cell_line",
        sample_label="Synthetic ESC line A",
        species="Homo sapiens",
        cell_source_type="ESC",
        cell_line_name="SYN-ESC-A",
        clonal_status="unknown",
        passage_number="p35+4",
        disease_or_diagnosis="unaffected synthetic control",
    )
    protocol = CultureProtocol(
        name="PROTO-SYN-CORTICAL-ESC-001",
        protocol_id="PROTO-SYN-CORTICAL-ESC-001",
        protocol_name="Synthetic ESC cortical organoid protocol",
        patterning_summary="single-SMAD inhibition w/ WNT inhibitor, dorsal forebrain patterning",
    )
    culture = CellCulture(
        name="CULT-SYN-PHARM-ORG-001",
        culture_id="CULT-SYN-PHARM-ORG-001",
        culture_type="organoid",
        sample_label="Synthetic pharmacology organoid",
        species="Homo sapiens",
        culture_subtype="cortical",
        age="day84",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="unaffected synthetic control",
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-SYN-PHARM-ORG-001",
        species="Homo sapiens",
        sex="F",
        description="Synthetic organoid subject for pharmacology titration",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-SYN-PHARM-ORG-001", "Synthetic pharmacology titration example")
    nwbfile.subject = subject
    device = _device(nwbfile, "Example MEA Device B", "MEA recording system")
    experiment = ExperimentContext(
        name="EXP-SYN-PHARM-TITRATION-001",
        experiment_id="EXP-SYN-PHARM-TITRATION-001",
        subject=subject,
        culture=culture,
        age_at_recording="day121",
        age_reference="days_post_aggregation",
        recording_platform="MEA",
        media_or_bath="BrainPhys + supplements",
        recording_duration_s=3600.0,
        spontaneous_activity=True,
        electrical_stimulation=False,
        optical_stimulation=False,
        pharmacology_present=True,
        experimental_setup="Titration of ExampleDrug-A from 5 uM to 100 uM with washout at end",
        device=device,
    )
    pharmacology = Pharmacology(
        name="PHARM-SYN-EXAMPLEDRUG-A-001",
        pharmacology_id="PHARM-SYN-EXAMPLEDRUG-A-001",
        experiment=experiment,
        agent="ExampleDrug-A",
        concentration="5-100",
        concentration_unit="uM",
        start_time_s=300.0,
        end_time_s=2700.0,
        purpose="examine concentration-dependent effects in a synthetic example",
    )
    _add_context(
        nwbfile,
        cell_lines=[line],
        cell_cultures=[culture],
        cell_culture_source_line_relations=[_source_relation("REL-SYN-PHARM-SOURCE-001", culture, line)],
        experiment_context=experiment,
        pharmacologys=[pharmacology],
    )
    return nwbfile


def build_directoid():
    cortical_line = CellLine(
        name="CL-EX-CORTICAL",
        cell_line_id="CL-EX-CORTICAL",
        cell_line_type="derived_cell_line",
        sample_label="Cortical source line",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    thalamic_line = CellLine(
        name="CL-EX-THALAMIC",
        cell_line_id="CL-EX-THALAMIC",
        cell_line_type="derived_cell_line",
        sample_label="Thalamic source line",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    cortical_organoid = CellCulture(
        name="CULT-EX-CORTICAL-ORG-001",
        culture_id="CULT-EX-CORTICAL-ORG-001",
        culture_type="organoid",
        sample_label="Cortical organoid input",
        species="Homo sapiens",
        culture_subtype="cortical",
        age="P90D",
        age_reference="days_post_aggregation",
    )
    thalamic_organoid = CellCulture(
        name="CULT-EX-THALAMIC-ORG-001",
        culture_id="CULT-EX-THALAMIC-ORG-001",
        culture_type="organoid",
        sample_label="Thalamic organoid input",
        species="Homo sapiens",
        culture_subtype="thalamic",
        age="P90D",
        age_reference="days_post_aggregation",
    )
    protocol = CultureProtocol(
        name="PROTO-EX-DIRECTOID",
        protocol_id="PROTO-EX-DIRECTOID",
        protocol_name="Cortico-thalamic directoid microfluidic protocol",
        patterning_summary="cortical and thalamic organoids aligned across microfluidic channels",
        media_summary="shared maturation media during channel-directed axon growth",
    )
    directoid = CellCulture(
        name="CULT-EX-DIRECTOID-001",
        culture_id="CULT-EX-DIRECTOID-001",
        culture_type="assembloid",
        sample_label="Example directoid",
        species="Homo sapiens",
        culture_subtype="assembloid",
        age="P90D",
        age_reference="days_post_aggregation",
        notes="Directoid/connectoid-style preparation with axons directed through microfluidic channels.",
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-DIRECTOID-001",
        species="Homo sapiens",
        description="Example cortico-thalamic directoid",
        culture=directoid,
    )
    nwbfile = _nwbfile("NWB-EX-DIRECTOID-001", "Directoid synthetic example")
    nwbfile.subject = subject
    _add_context(
        nwbfile,
        cell_lines=[cortical_line, thalamic_line],
        cell_cultures=[cortical_organoid, thalamic_organoid, directoid],
        cell_culture_source_line_relations=[
            _source_relation("REL-EX-CORTICAL-SOURCE-001", cortical_organoid, cortical_line),
            _source_relation("REL-EX-THALAMIC-SOURCE-001", thalamic_organoid, thalamic_line),
        ],
        cell_culture_parent_relations=[
            _culture_parent_relation("REL-EX-DIRECTOID-PARENT-CORTICAL", directoid, cortical_organoid, "assembled_from"),
            _culture_parent_relation("REL-EX-DIRECTOID-PARENT-THALAMIC", directoid, thalamic_organoid, "assembled_from"),
        ],
    )
    return nwbfile


def build_two_line_assembloid():
    line_a = CellLine(
        name="CL-EX-ASSEMBLOID-A",
        cell_line_id="CL-EX-ASSEMBLOID-A",
        cell_line_type="derived_cell_line",
        sample_label="Assembloid line A",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    line_b = CellLine(
        name="CL-EX-ASSEMBLOID-B",
        cell_line_id="CL-EX-ASSEMBLOID-B",
        cell_line_type="derived_cell_line",
        sample_label="Assembloid line B",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    culture = CellCulture(
        name="CULT-EX-ASSEMBLOID-2LINE-001",
        culture_id="CULT-EX-ASSEMBLOID-2LINE-001",
        culture_type="assembloid",
        sample_label="Example two-line assembloid",
        species="Homo sapiens",
        culture_subtype="assembloid",
        notes="Synthetic example assembled from two distinct source cell lines.",
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-ASSEMBLOID-2LINE-001",
        species="Homo sapiens",
        description="Example assembloid from two distinct source lines",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-EX-ASSEMBLOID-2LINE-001", "Two-line assembloid synthetic example")
    nwbfile.subject = subject
    _add_context(
        nwbfile,
        cell_lines=[line_a, line_b],
        cell_cultures=[culture],
        cell_culture_source_line_relations=[
            _source_relation("REL-EX-ASSEMBLOID-SOURCE-A", culture, line_a, role="component"),
            _source_relation("REL-EX-ASSEMBLOID-SOURCE-B", culture, line_b, role="component"),
        ],
    )
    return nwbfile


SCENARIOS = {
    "basic_organoid": build_basic_organoid,
    "slice_patch_clamp": build_slice_patch_clamp,
    "edited_ipsc_organoid_mea": build_edited_ipsc_organoid_mea,
    "biological_metadata_only_organoid": build_biological_metadata_only_organoid,
    "pharmacology_titration_organoid": build_pharmacology_titration_organoid,
    "directoid": build_directoid,
    "two_line_assembloid": build_two_line_assembloid,
}
