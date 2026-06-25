"""Reusable example NWBFile builders for ndx-cell-culture review scenarios."""

from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from ndx_cell_culture import (
    CellCulture,
    CellCultureSubject,
    CellLine,
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
        name="culture",
        culture_id="CULT-EX-ORG-001",
        culture_type="organoid",
        sample_label="Example organoid A",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
        cell_lines=[line],
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
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(name="culture_experiment_context", experiment_context=experiment)
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
    construct = ConstructApplication(
        name="APP-EX-AAV-CHR2-01",
        application_id="APP-EX-AAV-CHR2-01",
        delivery_route="microinjection",
        vector_type="AAV",
        payload="ChR2(H134R)-EYFP",
        expression_status="observed",
    )
    culture = CellCulture(
        name="culture",
        culture_id="CULT-EX-SLICE-001",
        culture_type="slice",
        sample_label="Example slice A",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
        notes="Derived from parent organoid CULT-EX-ORG-001; formal parent_cultures reference idiom is under NWB review.",
        cell_lines=[line],
        construct_applications=[construct],
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-SLICE-001",
        species="Homo sapiens",
        description="Example organoid-derived slice",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-EX-SLICE-001", "Example organoid slice patch-clamp recording")
    nwbfile.subject = subject
    device = _device(nwbfile, "Axon Multiclamp 700B", "Patch-clamp amplifier")
    experiment = ExperimentContext(
        name="EXP-EX-SLICE-001",
        experiment_id="EXP-EX-SLICE-001",
        subject=subject,
        culture=culture,
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
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(
            name="culture_experiment_context",
            experiment_context=experiment,
            pharmacologys=pharmacology,
        )
    )
    return nwbfile


def build_kolf_shank3_org1():
    parental = CellLine(
        name="KOLF2.2j",
        cell_line_id="KOLF2.2j",
        cell_line_type="parental_cell_line",
        sample_label="KOLF2.2j",
        species="Homo sapiens",
        cell_source_type="iPSC",
        cell_line_name="KOLF2.2j",
        clonal_status="clonal",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
    )
    variant = GeneticVariant(
        name="MOD-SHANK3-het",
        variant_id="MOD-SHANK3+/-",
        target_symbol="SHANK3",
        edit_type="knockin",
        edit_description="exon X frameshift mutation resulting in stop codon",
        method="CRISPR-Cas9",
        zygosity_or_edit_state="heterozygous",
        validation_status="screened",
        validation_method="ONT",
    )
    derived = CellLine(
        name="KOLF2.2j-SHANK3-het",
        cell_line_id="KOLF2.2j-SHANK3+/-",
        cell_line_type="derived_cell_line",
        sample_label="KOLF2.2j-SHANK3+/-",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clonal_status="clonal",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
        genetic_variants=[variant],
        notes="Derived from KOLF2.2j; parent_cell_line reference idiom is under NWB review.",
    )
    protocol = CultureProtocol(
        name="BGR-proto-progCtx",
        protocol_id="BGR-proto-progCtx",
        protocol_name="Prog ctx v1",
        patterning_summary="dual-SMAD inhibition w/ WNT inhibitor, forebrain patterning",
        media_summary="neural induction + maturation media",
    )
    culture = CellCulture(
        name="culture",
        culture_id="KOLF2.2j-SHANK3+/- Org 1",
        culture_type="organoid",
        sample_label="Batch 1 Org 1",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="Batch 1",
        age="day45",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
        cell_lines=[parental, derived],
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-KOLF2.2J-SHANK3-ORG1",
        species="Homo sapiens",
        sex="M",
        description="Legacy Org 1 subject mapped from manual validation data",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-KOLF-SHANK3-ORG1", "KOLF SHANK3 organoid manual validation example")
    nwbfile.subject = subject
    device = _device(nwbfile, "MaxOne P004714", "MEA recording system/chip")
    experiment = ExperimentContext(
        name="EXP-ORG001-MEA-01",
        experiment_id="EXP-ORG001-MEA-01",
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
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(name="culture_experiment_context", experiment_context=experiment)
    )
    return nwbfile


def build_kolf_shank3_org2():
    parental = CellLine(
        name="KOLF2.2j",
        cell_line_id="KOLF2.2j",
        cell_line_type="parental_cell_line",
        sample_label="KOLF2.2j",
        species="Homo sapiens",
        cell_source_type="iPSC",
        cell_line_name="KOLF2.2j",
        clonal_status="clonal",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
    )
    variant = GeneticVariant(
        name="MOD-SHANK3-het",
        variant_id="MOD-SHANK3+/-",
        target_symbol="SHANK3",
        edit_type="knockin",
        edit_description="exon X frameshift mutation resulting in stop codon",
        method="CRISPR-Cas9",
        zygosity_or_edit_state="heterozygous",
        validation_status="screened",
        validation_method="ONT",
    )
    derived = CellLine(
        name="KOLF2.2j-SHANK3-het",
        cell_line_id="KOLF2.2j-SHANK3+/-",
        cell_line_type="derived_cell_line",
        sample_label="KOLF2.2j-SHANK3+/-",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clonal_status="clonal",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
        genetic_variants=[variant],
        notes="Derived from KOLF2.2j; parent_cell_line reference idiom is under NWB review.",
    )
    protocol = CultureProtocol(
        name="BGR-proto-progCtx",
        protocol_id="BGR-proto-progCtx",
        protocol_name="Prog ctx v1",
        patterning_summary="dual-SMAD inhibition w/ WNT inhibitor, forebrain patterning",
        media_summary="neural induction + maturation media",
    )
    culture = CellCulture(
        name="culture",
        culture_id="KOLF2.2j-SHANK3+/- Org 2",
        culture_type="organoid",
        sample_label="Batch 1 Org 2",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="Batch 1",
        age="day45",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="ASD",
        reference_genome="GRCh38",
        cell_lines=[parental, derived],
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-KOLF2.2J-SHANK3-ORG2",
        species="Homo sapiens",
        sex="M",
        description="Legacy Org 2 subject mapped from manual validation data",
        culture=culture,
    )
    nwbfile = _nwbfile(
        "NWB-KOLF-SHANK3-ORG2",
        "KOLF SHANK3 organoid 2 manual validation example without experiment row",
    )
    nwbfile.subject = subject
    return nwbfile


def build_h9_do11_ketamine():
    line = CellLine(
        name="H9",
        cell_line_id="H9",
        cell_line_type="parental_cell_line",
        sample_label="H9",
        species="HOMO SAPIENS",
        cell_source_type="ESC",
        cell_line_name="H9",
        clonal_status="unknown",
        passage_number="p35+4",
        disease_or_diagnosis="WT",
        notes="Manual validation row contained N/A placeholders; optional placeholders omitted.",
    )
    protocol = CultureProtocol(
        name="RNH",
        protocol_id="RNH",
        protocol_name="RNH cortical",
        patterning_summary="single-SMAD inhibition w/ WNT inhibitor, dorsal forebrain patterning",
    )
    culture = CellCulture(
        name="culture",
        culture_id="H9-DO11",
        culture_type="organoid",
        sample_label="DO11",
        species="HOMO SAPIENS",
        culture_subtype="cortical",
        age="day84",
        age_reference="days_post_aggregation",
        disease_or_diagnosis="WT",
        cell_lines=[line],
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-H9-DO11",
        species="HOMO SAPIENS",
        sex="F",
        description="Legacy H9-DO11 subject mapped from manual validation data",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-H9-DO11-KETAMINE", "H9 DO11 ketamine manual validation example")
    nwbfile.subject = subject
    device = _device(nwbfile, "MaxTwo m07575", "MEA recording system/chip")
    experiment = ExperimentContext(
        name="DO11-Ketamine",
        experiment_id="DO11-Ketamine",
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
        experimental_setup="Titration of ketamine from 5 uM to 100 uM with washout at end",
        device=device,
    )
    pharmacology = Pharmacology(
        name="H9-DO11",
        pharmacology_id="H9-DO11",
        experiment=experiment,
        agent="Ketamine",
        concentration="5-100",
        concentration_unit="uM",
        start_time_s=300.0,
        end_time_s=2700.0,
        purpose="examine ketamine effects at rising concentrations",
    )
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(
            name="culture_experiment_context",
            experiment_context=experiment,
            pharmacologys=[pharmacology],
        )
    )
    return nwbfile


def build_directoid():
    cortical = CellLine(
        name="CL-EX-CORTICAL",
        cell_line_id="CL-EX-CORTICAL",
        cell_line_type="derived_cell_line",
        sample_label="Cortical source line",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    thalamic = CellLine(
        name="CL-EX-THALAMIC",
        cell_line_id="CL-EX-THALAMIC",
        cell_line_type="derived_cell_line",
        sample_label="Thalamic source line",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    protocol = CultureProtocol(
        name="PROTO-EX-DIRECTOID",
        protocol_id="PROTO-EX-DIRECTOID",
        protocol_name="Cortico-thalamic directoid microfluidic protocol",
        patterning_summary="cortical and thalamic organoids aligned across microfluidic channels",
        media_summary="shared maturation media during channel-directed axon growth",
    )
    culture = CellCulture(
        name="culture",
        culture_id="CULT-EX-DIRECTOID-001",
        culture_type="assembloid",
        sample_label="Example directoid",
        species="Homo sapiens",
        culture_subtype="assembloid",
        age="P90D",
        age_reference="days_post_aggregation",
        notes=(
            "Directoid/connectoid-style preparation assembled from cortical and thalamic organoids "
            "with axons directed through microfluidic channels. Parent culture object references are "
            "part of the schema review point."
        ),
        cell_lines=[cortical, thalamic],
        culture_protocol=protocol,
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-DIRECTOID-001",
        species="Homo sapiens",
        description="Example cortico-thalamic directoid",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-EX-DIRECTOID-001", "Directoid synthetic example")
    nwbfile.subject = subject
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
        name="culture",
        culture_id="CULT-EX-ASSEMBLOID-2LINE-001",
        culture_type="assembloid",
        sample_label="Example two-line assembloid",
        species="Homo sapiens",
        culture_subtype="assembloid",
        notes="Synthetic example assembled from two distinct source cell lines.",
        cell_lines=[line_a, line_b],
    )
    subject = CellCultureSubject(
        subject_id="SUBJ-EX-ASSEMBLOID-2LINE-001",
        species="Homo sapiens",
        description="Example assembloid from two distinct source lines",
        culture=culture,
    )
    nwbfile = _nwbfile("NWB-EX-ASSEMBLOID-2LINE-001", "Two-line assembloid synthetic example")
    nwbfile.subject = subject
    return nwbfile


SCENARIOS = {
    "basic_organoid": build_basic_organoid,
    "slice_patch_clamp": build_slice_patch_clamp,
    "kolf_shank3_org1": build_kolf_shank3_org1,
    "kolf_shank3_org2": build_kolf_shank3_org2,
    "h9_do11_ketamine": build_h9_do11_ketamine,
    "directoid": build_directoid,
    "two_line_assembloid": build_two_line_assembloid,
}
