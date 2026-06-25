"""Create a small NWB file using ndx-cell-culture.

Run from the repository root after installing the package:

    python -m pip install -e .
    python examples/create_basic_organoid_nwb.py
"""

from datetime import datetime
from pathlib import Path

from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

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


def build_nwbfile() -> NWBFile:
    """Build a representative organoid NWBFile."""
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

    nwbfile = NWBFile(
        session_description="Example ndx-cell-culture organoid recording",
        identifier="NWB-EX-ORG-001",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject
    device = nwbfile.create_device(
        name="MaxTwo MX2-CHIP-17",
        description="Core NWB Device representing the MEA recording system/chip.",
    )
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
        pharmacology_present=True,
        experimental_setup="spontaneous + blue light stimulation",
        device=device,
    )
    pharmacology = Pharmacology(
        name="PHARM-EX-CNQX-01",
        pharmacology_id="PHARM-EX-CNQX-01",
        experiment=experiment,
        agent="CNQX",
        concentration="10",
        concentration_unit="uM",
        start_time_s=300.0,
        end_time_s=900.0,
        purpose="block AMPA/kainate receptors",
    )
    nwbfile.add_lab_meta_data(
        CultureExperimentContext(
            name="culture_experiment_context",
            experiment_context=experiment,
            pharmacologys=[pharmacology],
        )
    )
    return nwbfile


def main():
    output_path = Path(__file__).with_name("basic_organoid_example.nwb")
    with NWBHDF5IO(str(output_path), "w") as io:
        io.write(build_nwbfile())
    print(output_path)


if __name__ == "__main__":
    main()
