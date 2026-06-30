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
        "CellLineParentRelation",
        "CellCultureSourceLineRelation",
        "CellCultureParentRelation",
        "GeneticVariant",
        "ConstructApplication",
        "CultureProtocol",
        "CultureExperimentContext",
        "ExperimentContext",
        "Pharmacology",
    ]:
        assert hasattr(ndx, name)
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
    source_relation = ndx.CellCultureSourceLineRelation(
        name="REL-EX-ORG-SOURCE-001",
        relation_id="REL-EX-ORG-SOURCE-001",
        culture=culture,
        source_line=line,
        role="primary_source",
    )
    nwbfile.add_lab_meta_data(
        ndx.CultureExperimentContext(
            name="culture_experiment_context",
            cell_lines=[line],
            cell_cultures=[culture],
            cell_culture_source_line_relations=[source_relation],
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
        context = read.lab_meta_data["culture_experiment_context"]
        assert context.cell_cultures["CULT-EX-ORG-001"] is read.subject.culture
        assert context.cell_culture_source_line_relations["REL-EX-ORG-SOURCE-001"].source_line.cell_line_id == "CL-EX-CTRL-001"
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
        "source_lines",
        "parent_cultures",
    ]:
        assert removed not in schema


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
        "CellLineParentRelation",
        "CellCultureSourceLineRelation",
        "CellCultureParentRelation",
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
        "neurodata_type_def: CellLineParentRelation",
        "neurodata_type_def: CellCultureSourceLineRelation",
        "neurodata_type_def: CellCultureParentRelation",
        "name: child_cell_line",
        "name: parent_cell_line",
        "name: source_line",
        "name: child_culture",
        "name: parent_culture",
        "target_type: CellLine",
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
    subject = ndx.CellCultureSubject(subject_id="SUBJ", species="Homo sapiens", culture=culture)
    assert subject.culture.culture_id == "CULT"


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
    culture = ndx.CellCulture(
        name="culture",
        culture_id="CULT-REL",
        culture_type="organoid",
        sample_label="Relationship culture",
        species="Homo sapiens",
        construct_applications=[application],
        genetic_variants=[variant],
        culture_protocol=protocol,
    )
    line_parent_relation = ndx.CellLineParentRelation(
        name="REL-LINE-PARENT",
        relation_id="REL-LINE-PARENT",
        child_cell_line=derived_line,
        parent_cell_line=parent_line,
        relationship_type="edited_from",
    )
    source_relation = ndx.CellCultureSourceLineRelation(
        name="REL-CULTURE-SOURCE",
        relation_id="REL-CULTURE-SOURCE",
        culture=culture,
        source_line=derived_line,
        role="primary_source",
    )
    parent_culture = ndx.CellCulture(
        name="parent_culture",
        culture_id="CULT-PARENT",
        culture_type="organoid",
        sample_label="Parent culture",
        species="Homo sapiens",
    )
    culture_parent_relation = ndx.CellCultureParentRelation(
        name="REL-CULTURE-PARENT",
        relation_id="REL-CULTURE-PARENT",
        child_culture=culture,
        parent_culture=parent_culture,
        relationship_type="sliced_from",
    )
    subject = ndx.CellCultureSubject(subject_id="SUBJ-REL", species="Homo sapiens", culture=culture)
    nwbfile = NWBFile(
        session_description="relationship test",
        identifier="RELATIONSHIP-TEST",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject
    nwbfile.add_lab_meta_data(
        ndx.CultureExperimentContext(
            name="culture_experiment_context",
            cell_lines=[parent_line, derived_line],
            cell_cultures=[parent_culture, culture],
            cell_line_parent_relations=[line_parent_relation],
            cell_culture_source_line_relations=[source_relation],
            cell_culture_parent_relations=[culture_parent_relation],
        )
    )

    path = tmp_path / "relationships.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)

    _assert_no_validation_errors(path)

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        context = read.lab_meta_data["culture_experiment_context"]
        assert context.cell_line_parent_relations["REL-LINE-PARENT"].parent_cell_line.name == "parent"
        assert context.cell_culture_source_line_relations["REL-CULTURE-SOURCE"].source_line.name == "derived"
        assert context.cell_culture_parent_relations["REL-CULTURE-PARENT"].parent_culture.name == "parent_culture"
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
        name="culture",
        culture_id="CULT",
        culture_type="batch",
        sample_label="Culture",
        species="Homo sapiens",
    )
    subject = ndx.CellCultureSubject(subject_id="SUBJ", species="Homo sapiens", culture=culture)
    nwbfile = NWBFile(
        session_description="recommended-term validator test",
        identifier="TERM-VALIDATOR-TEST",
        session_start_time=datetime(2026, 5, 12, tzinfo=tzlocal()),
    )
    nwbfile.subject = subject
    nwbfile.add_lab_meta_data(
        ndx.CultureExperimentContext(
            name="culture_experiment_context",
            cell_lines=[line],
            cell_cultures=[culture],
        )
    )

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
            context = read.lab_meta_data["culture_experiment_context"]
            assert read.subject.culture.name in context.cell_cultures
            if platform is not None:
                context = read.lab_meta_data["culture_experiment_context"]
                assert context.experiment_context.recording_platform == platform
                assert len(context.pharmacologies) == pharmacology_count


def test_biological_metadata_only_scenario_has_catalog_but_no_experiment_context(tmp_path):
    path = tmp_path / "biological_metadata_only_organoid.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(SCENARIOS["biological_metadata_only_organoid"]())

    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        assert read.subject.subject_id == "SUBJ-SYN-EDITED-ORG-002"
        assert read.subject.culture.culture_id == "CULT-SYN-EDITED-ORG-002"
        context = read.lab_meta_data["culture_experiment_context"]
        assert context.experiment_context is None
        assert len(context.cell_cultures) == 1
