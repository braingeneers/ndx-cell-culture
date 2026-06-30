from datetime import datetime
from pathlib import Path
import sys

from dateutil.tz import tzlocal
from hdmf.utils import get_docval
from nwbinspector import Importance, inspect_nwbfile
from pynwb import NWBHDF5IO, NWBFile, validate
import pytest

import ndx_cell_culture as ndx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from scenario_builders import SCENARIOS  # noqa: E402


def _assert_no_validation_errors(path):
    try:
        result = validate(path=str(path))
    except TypeError:
        result = validate(paths=[str(path)])
    if isinstance(result, tuple):
        errors = result[0]
    else:
        errors = result
    assert errors == []


def _assert_no_inspector_violations(path):
    messages = list(
        inspect_nwbfile(
            nwbfile_path=str(path),
            importance_threshold=Importance.BEST_PRACTICE_VIOLATION,
        )
    )
    messages = [
        message
        for message in messages
        if not (
            message.check_function_name == "check_subject_age"
            and message.object_type == "CellCultureSubject"
        )
    ]
    assert messages == []


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
    for removed_name in [
        "CellLineParentRelation",
        "CellCultureSourceLineRelation",
        "CellCultureParentRelation",
    ]:
        assert not hasattr(ndx, removed_name)
    assert hasattr(ndx, "validate_recommended_terms")


def test_pharmacologies_alias_is_public_spelling():
    culture = ndx.CellCulture(
        name="CULT-ALIAS",
        culture_id="CULT-ALIAS",
        culture_type="organoid",
        sample_label="Alias culture",
        species="Homo sapiens",
    )
    subject = ndx.CellCultureSubject(
        subject_id="SUBJ-ALIAS",
        species="Homo sapiens",
        culture=culture,
    )
    experiment = ndx.ExperimentContext(
        name="EXP-ALIAS",
        experiment_id="EXP-ALIAS",
        subject=subject,
        culture=culture,
        age_at_recording="P1D",
        recording_platform="MEA",
    )
    pharmacology = ndx.Pharmacology(
        name="PHARM-ALIAS",
        pharmacology_id="PHARM-ALIAS",
        experiment=experiment,
        agent="CNQX",
    )
    context = ndx.CultureExperimentContext(
        name="culture_experiment_context",
        pharmacologies=[pharmacology],
    )
    generated_plural = "pharmacology" + "s"
    docval_names = [arg["name"] for arg in get_docval(ndx.CultureExperimentContext.__init__)]
    assert "pharmacologies" in docval_names
    with pytest.raises(ValueError, match="Use pharmacologies"):
        ndx.CultureExperimentContext(
            name="culture_experiment_context",
            pharmacologies=[pharmacology],
            **{generated_plural: [pharmacology]},
        )
    assert context.pharmacologies["PHARM-ALIAS"] is pharmacology
    assert context.get_pharmacologies("PHARM-ALIAS") is pharmacology
    assert hasattr(context, "add_pharmacologies")
    assert hasattr(context, "create_pharmacologies")


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
        name="CULT-EX-ORG-001",
        culture_id="CULT-EX-ORG-001",
        culture_type="organoid",
        sample_label="Example organoid A",
        species="Homo sapiens",
        culture_subtype="cortical",
        batch_label="EX-B1",
        age="P120D",
        age_reference="days_post_induction",
        genetic_variants=[variant],
        construct_applications=[construct],
        culture_protocol=protocol,
        source_lines=[line],
    )
    subject = ndx.CellCultureSubject(
        subject_id="SUBJ-EX-ORG-001",
        species="Homo sapiens",
        sex="F",
        description="Recorded cortical organoid on MEA",
        culture=culture,
        cell_lines=[line],
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
            pharmacologies=[pharmacology],
        )
    )
    return nwbfile


def test_write_read_roundtrip(tmp_path):
    path = tmp_path / "roundtrip.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(_build_roundtrip_file())

    _assert_no_validation_errors(path)
    _assert_no_inspector_violations(path)

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.subject_id == "SUBJ-EX-ORG-001"
        assert read.subject.culture.culture_id == "CULT-EX-ORG-001"
        assert read.subject.culture.culture_type == "organoid"
        assert read.subject.sex == "F"
        assert read.subject.cell_cultures["CULT-EX-ORG-001"] is read.subject.culture
        assert read.subject.cell_lines["CL-EX-CTRL-001"] is read.subject.culture.source_lines[0]
        context = read.lab_meta_data["culture_experiment_context"]
        assert read.subject.culture.source_lines[0].cell_line_id == "CL-EX-CTRL-001"
        assert context.experiment_context.experiment_id == "EXP-EX-ORG-001"
        assert context.experiment_context.device.name == "MaxTwo MX2-CHIP-17"
        assert context.pharmacologies["PHARM-EX-CNQX-01"].agent == "CNQX"


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
        "starting_material_line",
        "CellLineParentRelation",
        "CellCultureSourceLineRelation",
        "CellCultureParentRelation",
        "relation_id",
        "child_cell_line",
        "child_culture",
        "cell_line_parent_relations",
        "cell_culture_source_line_relations",
        "cell_culture_parent_relations",
        "Reusable CellLine catalog entries",
        "Reusable CellCulture catalog entries",
    ]:
        assert removed not in schema
    for required in [
        "source_lines",
        "parent_cultures",
        "parent_cell_line",
    ]:
        assert required in schema


def test_user_docs_cover_extension_types_without_planning_artifacts():
    docs_paths = [
        "README.md",
        "docs/design.md",
        "docs/field_reference.md",
        "docs/examples.md",
        "docs/release.md",
    ]
    docs_paths.extend(str(path) for path in Path("docs/source/source").glob("*.rst"))
    docs_text = "\n".join(Path(path).read_text() for path in docs_paths)
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
    for planning_or_lab_specific_term in [
        "workbook",
        "nwb_organoid",
        "v0.74",
        "KOLF",
        "H9",
        "DO11",
        "manual validation",
        "Legacy",
        "Decisions Requested",
        "Architecture Decisions",
        "Rationale:",
        "NDX First",
        "pharmacology" + "s",
        "open question",
        "release-blocking",
        "CellLineParentRelation",
        "CellCultureSourceLineRelation",
        "CellCultureParentRelation",
        "CellCulture catalog entry",
        "file-level metadata catalog",
        "CellLine and CellCulture catalog entries",
        "CultureExperimentContext`` is the file-level metadata catalog",
    ]:
        assert planning_or_lab_specific_term not in docs_text


def test_schema_declares_critical_relationships():
    schema = "\n".join(p.read_text() for p in Path("spec").glob("*.yaml"))
    for relationship in [
        "neurodata_type_def: CellCultureSubject",
        "neurodata_type_inc: Subject",
        "neurodata_type_def: CultureExperimentContext",
        "neurodata_type_inc: LabMetaData",
        "name: culture",
        "name: parent_cell_line",
        "name: source_lines",
        "name: parent_cultures",
        "target_type: CellLine",
        "target_type: CellCulture",
        "name: related_application",
        "target_type: ConstructApplication",
        "name: subject",
        "target_type: CellCultureSubject",
        "name: device",
        "target_type: Device",
        "name: experiment",
        "target_type: ExperimentContext",
    ]:
        assert relationship in schema
    context_spec = schema.split("neurodata_type_def: CultureExperimentContext", 1)[1]
    assert "neurodata_type_inc: CellLine" not in context_spec
    assert "neurodata_type_inc: CellCulture" not in context_spec


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
        name="CULT",
        culture_id="CULT",
        culture_type="organoid",
        sample_label="Culture",
        species="Homo sapiens",
    )
    subject = ndx.CellCultureSubject(subject_id="SUBJ", species="Homo sapiens", culture=culture, cell_lines=[line])
    assert subject.culture.culture_id == "CULT"
    assert subject.cell_cultures["CULT"] is culture
    assert subject.cell_lines["CL"] is line
    subject_docval_names = [arg["name"] for arg in get_docval(ndx.CellCultureSubject.__init__)]
    assert "related_cultures" in subject_docval_names
    context_docval_names = [arg["name"] for arg in get_docval(ndx.CultureExperimentContext.__init__)]
    assert "cell_lines" not in context_docval_names
    assert "cell_cultures" not in context_docval_names


def test_stable_relationship_links_write_read_and_validate(tmp_path):
    parent_line = ndx.CellLine(
        name="parent",
        cell_line_id="CL-PARENT",
        cell_line_type="parental_cell_line",
        sample_label="Parent",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    derived_line = ndx.CellLine(
        name="derived",
        cell_line_id="CL-DERIVED",
        cell_line_type="derived_cell_line",
        sample_label="Derived",
        species="Homo sapiens",
        cell_source_type="iPSC",
        parent_cell_line=parent_line,
    )
    application = ndx.ConstructApplication(
        name="application",
        application_id="APP-REL",
        vector_type="plasmid",
        payload="reporter",
    )
    variant = ndx.GeneticVariant(
        name="variant",
        variant_id="VAR-REL",
        target_symbol="GENE1",
        edit_type="knockout",
        method="CRISPR-Cas9",
        related_application=application,
    )
    protocol = ndx.CultureProtocol(
        name="protocol",
        protocol_id="PROTO-REL",
    )
    parent_culture = ndx.CellCulture(
        name="parent_culture",
        culture_id="CULT-PARENT",
        culture_type="organoid",
        sample_label="Parent culture",
        species="Homo sapiens",
    )
    culture = ndx.CellCulture(
        name="CULT-REL",
        culture_id="CULT-REL",
        culture_type="organoid",
        sample_label="Relationship culture",
        species="Homo sapiens",
        construct_applications=[application],
        genetic_variants=[variant],
        culture_protocol=protocol,
        source_lines=[derived_line],
        parent_cultures=[parent_culture],
    )
    subject = ndx.CellCultureSubject(
        subject_id="SUBJ-REL",
        species="Homo sapiens",
        culture=culture,
        cell_lines=[parent_line, derived_line],
        related_cultures=[parent_culture],
    )
    nwbfile = NWBFile(
        session_description="relationship test",
        identifier="RELATIONSHIP-TEST",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject

    path = tmp_path / "relationships.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)

    _assert_no_validation_errors(path)

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.cell_lines["derived"].parent_cell_line[0].name == "parent"
        assert read.subject.cell_cultures["CULT-REL"].source_lines[0].name == "derived"
        assert read.subject.cell_cultures["CULT-REL"].parent_cultures[0].name == "parent_culture"
        assert read.subject.get_related_cultures("parent_culture").culture_id == "CULT-PARENT"
        assert read.subject.culture.genetic_variants["variant"].related_application.name == "application"


def test_recommended_term_validator_reports_invalid_values():
    line = ndx.CellLine(
        name="line",
        cell_line_id="CL",
        cell_line_type="not_a_recommended_term",
        sample_label="CL",
        species="Homo sapiens",
        cell_source_type="iPSC",
    )
    culture = ndx.CellCulture(
        name="CULT",
        culture_id="CULT",
        culture_type="batch",
        sample_label="Culture",
        species="Homo sapiens",
    )
    subject = ndx.CellCultureSubject(subject_id="SUBJ", species="Homo sapiens", culture=culture, cell_lines=[line])
    nwbfile = NWBFile(
        session_description="recommended-term validator test",
        identifier="TERM-VALIDATOR-TEST",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject

    issues = ndx.validate_recommended_terms(nwbfile)
    assert {(issue.object_type, issue.field, issue.value) for issue in issues} == {
        ("CellCulture", "culture_type", "batch"),
        ("CellLine", "cell_line_type", "not_a_recommended_term"),
    }
    assert "expected one of" in issues[0].message


def test_synthetic_scenarios_write_read_and_validate(tmp_path):
    expected = {
        "basic_organoid": ("organoid", "MEA", 0),
        "slice_patch_clamp": ("slice", "patch_clamp", 2),
        "edited_ipsc_organoid_mea": ("organoid", "MEA", 0),
        "pharmacology_titration_organoid": ("organoid", "MEA", 1),
        "directoid": ("assembloid", None, 0),
        "two_line_assembloid": ("assembloid", None, 0),
    }
    for name, (culture_type, platform, pharmacology_count) in expected.items():
        path = tmp_path / f"{name}.nwb"
        with NWBHDF5IO(str(path), "w") as io:
            io.write(SCENARIOS[name]())

        _assert_no_validation_errors(path)
        _assert_no_inspector_violations(path)

        with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
            read = io.read()
            assert ndx.validate_recommended_terms(read) == []
            assert read.subject.culture.culture_type == culture_type
            assert read.subject.culture.name in read.subject.cell_cultures
            if platform is not None:
                context = read.lab_meta_data["culture_experiment_context"]
                assert context.experiment_context.recording_platform == platform
                assert len(context.pharmacologies) == pharmacology_count
            else:
                assert not read.lab_meta_data or "culture_experiment_context" not in read.lab_meta_data


def test_biological_metadata_only_scenario_has_subject_biology_but_no_experiment_context(tmp_path):
    path = tmp_path / "biological_metadata_only_organoid.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(SCENARIOS["biological_metadata_only_organoid"]())

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.subject_id == "SUBJ-SYN-EDITED-ORG-002"
        assert read.subject.culture.culture_id == "CULT-SYN-EDITED-ORG-002"
        assert not read.lab_meta_data or "culture_experiment_context" not in read.lab_meta_data
        assert len(read.subject.cell_cultures) == 1
        assert len(read.subject.cell_lines) == 2
