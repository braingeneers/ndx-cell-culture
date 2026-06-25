from datetime import datetime
from pathlib import Path
import sys

from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

import ndx_cell_culture as ndx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from scenario_builders import SCENARIOS  # noqa: E402


def test_dynamic_classes_are_available():
    for name in [
        "CellCultureSubject",
        "CellCulture",
        "CellLine",
        "GeneticVariant",
        "ConstructApplication",
        "CultureProtocol",
        "CultureExperimentContext",
        "ExperimentContext",
        "Pharmacology",
    ]:
        assert hasattr(ndx, name)


def _build_roundtrip_file():
    line = ndx.CellLine(
        name="CL-EX-CTRL-001",
        cell_line_id="CL-EX-CTRL-001",
        cell_line_type="parental_cell_line",
        sample_label="Example line",
        species="Homo sapiens",
        cell_source_type="iPSC",
        clonal_status="clonal",
        passage_number="p35",
    )
    variant = ndx.GeneticVariant(
        name="VAR-EX-SYNGAP1-KO-01",
        variant_id="VAR-EX-SYNGAP1-KO-01",
        target_symbol="SYNGAP1",
        edit_type="knockout",
        method="CRISPR-Cas9",
        zygosity_or_edit_state="biallelic",
        validation_status="validated",
    )
    construct = ndx.ConstructApplication(
        name="APP-EX-LV-GCAMP6F-01",
        application_id="APP-EX-LV-GCAMP6F-01",
        vector_type="lentivirus",
        payload="GCaMP6f",
        delivery_route="transduction",
    )
    protocol = ndx.CultureProtocol(
        name="PROTO-EX-CORT-V3",
        protocol_id="PROTO-EX-CORT-V3",
        protocol_name="Cortical organoid v3",
        patterning_summary="dual-SMAD inhibition, forebrain patterning",
    )
    culture = ndx.CellCulture(
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
        genetic_variants=[variant],
        construct_applications=[construct],
        culture_protocol=protocol,
    )
    subject = ndx.CellCultureSubject(
        subject_id="SUBJ-EX-ORG-001",
        species="Homo sapiens",
        sex="F",
        description="Recorded cortical organoid on MEA",
        culture=culture,
    )
    nwbfile = NWBFile(
        session_description="round-trip test",
        identifier="TEST-NDX-CELL-CULTURE",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject
    device = nwbfile.create_device(name="MaxTwo MX2-CHIP-17", description="MEA device")
    experiment = ndx.ExperimentContext(
        name="EXP-EX-ORG-001",
        experiment_id="EXP-EX-ORG-001",
        subject=subject,
        culture=culture,
        age_at_recording="P120D",
        age_reference="days_post_induction",
        recording_platform="MEA",
        spontaneous_activity=True,
        electrical_stimulation=False,
        optical_stimulation=True,
        pharmacology_present=True,
        device=device,
    )
    pharmacology = ndx.Pharmacology(
        name="PHARM-EX-CNQX-01",
        pharmacology_id="PHARM-EX-CNQX-01",
        experiment=experiment,
        agent="CNQX",
        concentration="10",
        concentration_unit="uM",
        start_time_s=300.0,
        end_time_s=900.0,
    )
    nwbfile.add_lab_meta_data(
        ndx.CultureExperimentContext(
            name="culture_experiment_context",
            experiment_context=experiment,
            pharmacologys=[pharmacology],
        )
    )
    return nwbfile


def test_write_read_roundtrip(tmp_path):
    path = tmp_path / "roundtrip.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(_build_roundtrip_file())

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.subject_id == "SUBJ-EX-ORG-001"
        assert read.subject.culture.culture_id == "CULT-EX-ORG-001"
        assert read.subject.culture.culture_type == "organoid"
        assert read.subject.sex == "F"
        context = read.lab_meta_data["culture_experiment_context"]
        assert context.experiment_context.experiment_id == "EXP-EX-ORG-001"
        assert context.experiment_context.device.name == "MaxTwo MX2-CHIP-17"
        assert context.pharmacologys["PHARM-EX-CNQX-01"].agent == "CNQX"


def test_removed_terms_are_absent_from_schema():
    schema = "\n".join(p.read_text() for p in Path("spec").glob("*.yaml"))
    for removed in [
        "ExternalAsset",
        "external_assets",
        "validation_asset_id",
        "age_or_passage",
        "recording_preparation",
        "hardware_platform_details",
        "chip_id",
        "viral_infection",
    ]:
        assert removed not in schema


def test_reviewer_docs_cover_extension_types_and_design_sources():
    docs_text = "\n".join(
        Path(path).read_text()
        for path in [
            "README.md",
            "docs/design.md",
            "docs/field_reference.md",
            "docs/examples.md",
            "docs/maintainer_review.md",
        ]
    )
    for name in [
        "CellCultureSubject",
        "CellCulture",
        "CellLine",
        "GeneticVariant",
        "ConstructApplication",
        "CultureProtocol",
        "CultureExperimentContext",
        "ExperimentContext",
        "Pharmacology",
    ]:
        assert name in docs_text
    for design_source in [
        "nwb_organoid_sample_workbook_v0.74.xlsx",
        "nwb_organoid_formal_extension_notes_v0.74.md",
        "formal_nwb_extension_build_plan.md",
    ]:
        assert design_source in docs_text


def test_schema_declares_critical_relationships():
    schema = "\n".join(p.read_text() for p in Path("spec").glob("*.yaml"))
    for relationship in [
        "neurodata_type_def: CellCultureSubject",
        "neurodata_type_inc: Subject",
        "neurodata_type_def: CultureExperimentContext",
        "neurodata_type_inc: LabMetaData",
        "name: culture",
        "name: source_lines",
        "name: parent_cultures",
        "name: parent_cell_line",
        "name: subject",
        "target_type: CellCultureSubject",
        "name: device",
        "target_type: Device",
        "name: experiment",
        "target_type: ExperimentContext",
    ]:
        assert relationship in schema


def test_required_culture_on_subject():
    line = ndx.CellLine(
        name="CL",
        cell_line_id="CL",
        cell_line_type="parental_cell_line",
        sample_label="CL",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    culture = ndx.CellCulture(
        name="culture",
        culture_id="CULT",
        culture_type="organoid",
        sample_label="Culture",
        species="Homo sapiens",
        cell_lines=[line],
    )
    subject = ndx.CellCultureSubject(subject_id="SUBJ", species="Homo sapiens", culture=culture)
    assert subject.culture.culture_id == "CULT"


def test_review_scenarios_write_and_read(tmp_path):
    expected = {
        "basic_organoid": ("organoid", "MEA", 0),
        "slice_patch_clamp": ("slice", "patch_clamp", 2),
        "kolf_shank3_org1": ("organoid", "MEA", 0),
        "h9_do11_ketamine": ("organoid", "MEA", 1),
        "directoid": ("assembloid", None, 0),
        "two_line_assembloid": ("assembloid", None, 0),
    }
    for name, (culture_type, platform, pharmacology_count) in expected.items():
        path = tmp_path / f"{name}.nwb"
        with NWBHDF5IO(str(path), "w") as io:
            io.write(SCENARIOS[name]())

        with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
            read = io.read()
            assert read.subject.culture.culture_type == culture_type
            if platform is None:
                assert not read.lab_meta_data
            else:
                context = read.lab_meta_data["culture_experiment_context"]
                assert context.experiment_context.recording_platform == platform
                assert len(context.pharmacologys) == pharmacology_count


def test_kolf_org2_is_biological_metadata_only(tmp_path):
    path = tmp_path / "kolf_org2.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(SCENARIOS["kolf_shank3_org2"]())

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.subject_id == "SUBJ-KOLF2.2J-SHANK3-ORG2"
        assert read.subject.culture.culture_id == "KOLF2.2j-SHANK3+/- Org 2"
        assert not read.lab_meta_data
