from datetime import datetime, timezone

import h5py
import pytest
from hdmf.common import VectorData
from pynwb import NWBHDF5IO, NWBFile, validate
from pynwb.file import LabMetaData, Subject

import ndx_cell_culture as ndx


def _line(name, **kwargs):
    return ndx.CellLine(
        name=name, cell_line_id=name, cell_line_type="derived_cell_line",
        sample_label=name, species="Homo sapiens", cell_source_type="iPSC", **kwargs
    )


def _culture(name="CULT", **kwargs):
    return ndx.CellCulture(
        name=name, culture_id=name, culture_type="organoid",
        sample_label=name, species="Homo sapiens", **kwargs
    )


def _application(name="APP"):
    return ndx.ConstructApplication(
        name=name, application_id=name, vector_type="plasmid", payload="reporter"
    )


def _variant(name="VAR", **kwargs):
    return ndx.GeneticVariant(
        name=name, variant_id=name, target_symbol="GENE", edit_type="point_mutation",
        origin="unknown", **kwargs
    )


def _subject(culture, **kwargs):
    return ndx.CellCultureSubject(
        subject_id="SUBJ", species="Homo sapiens", sex="U", culture=culture, **kwargs
    )


def _file(subject=None, **kwargs):
    nwbfile = NWBFile(
        session_description="review regression", identifier="REVIEW-REGRESSION",
        session_start_time=datetime(2026, 1, 1, tzinfo=timezone.utc), **kwargs
    )
    nwbfile.subject = subject
    return nwbfile


def _experiment(**kwargs):
    return ndx.ExperimentContext(
        name="EXP", experiment_id="EXP", age_at_recording="P1D", recording_platform="MEA", **kwargs
    )


def _write(nwbfile, path):
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)
    try:
        result = validate(path=str(path))
    except TypeError:
        result = validate(paths=[str(path)])
    assert (result[0] if isinstance(result, tuple) else result) == []


def test_context_ownership_and_derived_properties_roundtrip(tmp_path):
    culture = _culture()
    subject = _subject(culture)
    nwbfile = _file(subject, session_id="SESSION", notes="file notes")
    pharmacology = ndx.Pharmacology(name="PHARM", pharmacology_id="PHARM", agent="CNQX")
    device = nwbfile.create_device(name="DEVICE")
    experiment = _experiment(pharmacologies=[pharmacology], notes="bath notes", device=device)
    assert isinstance(experiment, LabMetaData)
    nwbfile.add_lab_meta_data(experiment)
    assert experiment.subject is subject
    assert experiment.culture is culture
    assert experiment.session_id == "SESSION"
    assert pharmacology.experiment is experiment
    assert experiment.notes != nwbfile.notes
    assert not hasattr(ndx, "CultureExperimentContext")

    path = tmp_path / "context.nwb"
    _write(nwbfile, path)
    with h5py.File(path, "r") as h5:
        context = h5["general/EXP"]
        assert "subject" not in context and "culture" not in context
        assert "session_id" not in context.attrs and "session_id" not in context
        assert "experiment" not in context["PHARM"]
        assert "device" in context
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        context = read.lab_meta_data["EXP"]
        assert context.subject is read.subject
        assert context.culture is read.subject.culture
        assert context.session_id == read.session_id == "SESSION"
        assert context.device is read.devices["DEVICE"]
        assert context.pharmacologies["PHARM"].experiment is context
        assert context.notes == "bath notes" and read.notes == "file notes"


@pytest.mark.parametrize("field", ["subject", "culture", "session_id"])
def test_context_requires_attachment_for_file_properties(field):
    with pytest.raises(ValueError, match="attached to an NWBFile"):
        getattr(_experiment(), field)


@pytest.mark.parametrize("subject", [None, Subject(subject_id="ANIMAL", species="Mus musculus", sex="U")])
def test_context_requires_cultured_subject(subject):
    nwbfile = _file(subject)
    experiment = _experiment()
    nwbfile.add_lab_meta_data(experiment)
    assert experiment.session_id is None
    for field in ("subject", "culture"):
        with pytest.raises(ValueError, match="CellCultureSubject"):
            getattr(experiment, field)


def test_pharmacology_requires_containing_context():
    pharmacology = ndx.Pharmacology(name="PHARM", pharmacology_id="PHARM", agent="CNQX")
    with pytest.raises(ValueError, match="attached to an ExperimentContext"):
        _ = pharmacology.experiment
    experiment = _experiment()
    experiment.add_pharmacologies(pharmacology)
    assert pharmacology.experiment is experiment
    created = experiment.create_pharmacologies(name="SECOND", pharmacology_id="SECOND", agent="APV")
    assert experiment.get_pharmacologies("SECOND") is created
    assert created.experiment is experiment


@pytest.mark.parametrize("origin", [None, "", "   ", "\t\n"])
def test_variant_rejects_empty_origin(origin):
    with pytest.raises((TypeError, ValueError), match="origin"):
        ndx.GeneticVariant(name="VAR", variant_id="VAR", target_symbol="GENE", edit_type="knockout", origin=origin)


def test_variant_requires_origin_argument():
    with pytest.raises(TypeError, match="origin"):
        ndx.GeneticVariant(name="VAR", variant_id="VAR", target_symbol="GENE", edit_type="knockout")


@pytest.mark.parametrize("origin", ["donor_derived", "engineered", "culture_acquired", "unknown", "other", "lab_defined"])
def test_variant_origin_vocabulary_remains_advisory(origin):
    variant = ndx.GeneticVariant(
        name="VAR", variant_id="VAR", target_symbol="GENE", edit_type="knockout", origin=origin, method="other"
    )
    assert variant.origin == origin
    issues = ndx.validate_recommended_terms(variant)
    if origin == "lab_defined":
        assert [issue.field for issue in issues] == ["origin"]
    else:
        assert issues == []


def test_subject_collects_recursive_provenance_and_applications(tmp_path):
    ancestor = _line("ANCESTOR")
    application = _application()
    derived = _line("DERIVED", parent_cell_line=ancestor, genetic_variants=[_variant(related_application=application)])
    parent = _culture("PARENT", source_lines=[derived])
    culture = _culture(source_lines=[derived, derived], parent_cultures=[parent])
    subject = _subject(culture)
    assert set(subject.cell_lines) == {"ANCESTOR", "DERIVED"}
    assert set(subject.related_cultures) == {"CULT", "PARENT"}
    assert application.parent is derived
    assert derived.construct_applications["APP"] is application
    path = tmp_path / "provenance.nwb"
    _write(_file(subject), path)
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        line = read.subject.cell_lines["DERIVED"]
        assert read.subject.culture.source_lines[0] is line
        assert read.subject.culture.source_lines[1] is line
        assert read.subject.related_cultures["PARENT"].source_lines[0] is line
        assert line.parent_cell_line[0] is read.subject.cell_lines["ANCESTOR"]
        assert line.genetic_variants["VAR"].related_application is line.construct_applications["APP"]


def test_subject_collects_culture_level_application(tmp_path):
    application = _application()
    culture = _culture(genetic_variants=[_variant(related_application=application)])
    subject = _subject(culture)
    assert culture.construct_applications["APP"] is application
    _write(_file(subject), tmp_path / "application.nwb")


def test_subject_preserves_application_owner_and_collects_that_owner(tmp_path):
    application = _application()
    owner = _line("OWNER", construct_applications=[application])
    culture = _culture(genetic_variants=[_variant(related_application=application)])
    subject = _subject(culture)
    assert subject.cell_lines["OWNER"] is owner
    assert application.parent is owner
    assert not culture.construct_applications
    _write(_file(subject), tmp_path / "owned-application.nwb")


def test_subject_preserves_explicit_objects_and_deduplicates_identity():
    line = _line("LINE")
    extra_line = _line("EXTRA")
    culture = _culture(source_lines=[line])
    extra_culture = _culture("EXTRA-CULTURE")
    subject = _subject(
        culture, cell_lines={line.name: line, extra_line.name: extra_line},
        cell_cultures=[culture, extra_culture], related_cultures=[extra_culture]
    )
    assert set(subject.cell_lines) == {"LINE", "EXTRA"}
    assert list(subject.cell_cultures) == ["CULT", "EXTRA-CULTURE"]


def test_shared_unowned_application_requires_explicit_owner_before_any_attachment():
    application = _application()
    first = _line("FIRST", genetic_variants=[_variant("VAR1", related_application=application)])
    second = _line("SECOND", genetic_variants=[_variant("VAR2", related_application=application)])
    culture = _culture(source_lines=[first, second])
    with pytest.raises(ValueError, match="APP.*multiple biological owners.*attach it explicitly"):
        _subject(culture)
    assert application.parent is None
    assert first.parent is None and second.parent is None and culture.parent is None
    first.add_construct_applications(application)
    subject = _subject(culture)
    assert application.parent is first
    assert set(subject.cell_lines) == {"FIRST", "SECOND"}


@pytest.mark.parametrize("collision", ["lines", "line_and_culture", "applications"])
def test_subject_rejects_distinct_objects_with_same_storage_name(collision):
    if collision == "lines":
        culture = _culture(source_lines=[_line("DUPLICATE"), _line("DUPLICATE")])
    elif collision == "line_and_culture":
        culture = _culture("DUPLICATE", source_lines=[_line("DUPLICATE")])
    else:
        culture = _culture(
            construct_applications=[_application("DUPLICATE")],
            genetic_variants=[_variant(related_application=_application("DUPLICATE"))]
        )
    with pytest.raises(ValueError, match="Distinct objects named 'DUPLICATE'"):
        _subject(culture)
    assert culture.parent is None


@pytest.mark.parametrize("reference", ["primary", "line", "parent", "application_owner"])
def test_subject_rejects_foreign_subject_ownership(reference):
    line = _line("LINE")
    application = _application()
    line.add_construct_applications(application)
    foreign_culture = _culture("FOREIGN", source_lines=[line])
    original = _subject(foreign_culture)
    culture = {
        "primary": lambda: foreign_culture,
        "line": lambda: _culture(source_lines=[line]),
        "parent": lambda: _culture(parent_cultures=[foreign_culture]),
        "application_owner": lambda: _culture(genetic_variants=[_variant(related_application=application)]),
    }[reference]()
    with pytest.raises(ValueError, match="already owned.*reuse its original subject"):
        _subject(culture)
    assert foreign_culture.parent is original and line.parent is original
    assert application.parent is line


def test_provenance_collection_terminates_reference_cycles(tmp_path):
    first = _culture("FIRST")
    second = _culture("SECOND", parent_cultures=[first])
    first.parent_cultures = VectorData(name="parent_cultures", description="cyclic references", data=[second])
    subject = _subject(first)
    assert set(subject.related_cultures) == {"FIRST", "SECOND"}
    _write(_file(subject), tmp_path / "cycle.nwb")


def test_collection_accepts_scalar_and_vector_parent_references(monkeypatch):
    # The collector supports the independently revised #5 representation too.
    from ndx_cell_culture._provenance import collect_subject_provenance

    ancestor = _line("ANCESTOR")
    derived = _line("DERIVED")
    culture = _culture(source_lines=[derived])
    for reference in (ancestor, VectorData(name="parent_cell_line", description="parent", data=[ancestor])):
        with monkeypatch.context() as patch:
            patch.setattr(ndx.CellLine, "parent_cell_line", property(lambda self: reference if self is derived else None))
            lines, cultures, attachments = collect_subject_provenance(object(), culture, None, None)
            assert lines == [derived, ancestor]
            assert cultures == [culture] and attachments == []
