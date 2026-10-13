"""Parent-line constraints, cached-schema reading, and legacy-file compatibility."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import textwrap

import h5py
from hdmf.build.errors import ConstructError
from hdmf.common import VectorData
from pynwb import NWBHDF5IO, NWBFile, get_type_map, validate
import pytest

import ndx_cell_culture as ndx


def _line(name, **kwargs):
    return ndx.CellLine(
        name=name,
        cell_line_id=name,
        cell_line_type="derived_cell_line" if kwargs.get("parent_cell_line") is not None else "parental_cell_line",
        sample_label=name,
        species="Homo sapiens",
        cell_source_type="iPSC",
        **kwargs,
    )


def _culture(name, **kwargs):
    return ndx.CellCulture(
        name=name,
        culture_id=name,
        culture_type="organoid",
        sample_label=name,
        species="Homo sapiens",
        **kwargs,
    )


def _file(lines, culture=None, related_cultures=None):
    culture = culture or _culture("CULT-PARENT-TEST")
    nwbfile = NWBFile(
        session_description="Synthetic parent-line regression",
        identifier="PARENT-LINE-TEST",
        session_start_time=datetime(2026, 10, 10, tzinfo=timezone.utc),
    )
    nwbfile.subject = ndx.CellCultureSubject(
        subject_id="SUBJ-PARENT-TEST",
        species="Homo sapiens",
        sex="U",
        culture=culture,
        cell_lines=lines,
        related_cultures=related_cultures,
    )
    return nwbfile


def _vector(data):
    return VectorData(name="parent_cell_line", description="Immediate parent", data=data)


def _assert_valid(path):
    assert _validation_errors(path) == []


def _validation_errors(path):
    try:
        result = validate(path=str(path))
    except TypeError:
        result = validate(paths=[str(path)])
    return result[0] if isinstance(result, tuple) else result


def _run_script(code, *args):
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code), *map(str, args)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_parent_schema_is_optional_and_has_one_reference():
    spec = get_type_map().namespace_catalog.get_spec("ndx-cell-culture", "CellLine")
    parent_spec = spec.get_dataset("parent_cell_line")
    assert parent_spec.quantity == "?"
    assert tuple(parent_spec.shape) == (1,)
    assert parent_spec.dtype["target_type"] == "CellLine"


@pytest.mark.parametrize("parent", [None, "omitted", "empty"])
def test_no_parent_is_stored_as_none(parent):
    kwargs = {} if parent == "omitted" else {"parent_cell_line": _vector([]) if parent == "empty" else None}
    assert _line("CL-ROOT", **kwargs).parent_cell_line is None


@pytest.mark.parametrize("as_vector", [False, True])
def test_single_parent_is_accepted(as_vector):
    parent = _line("CL-ROOT")
    value = _vector([parent]) if as_vector else parent
    child = _line("CL-CHILD", parent_cell_line=value)
    assert len(child.parent_cell_line) == 1
    assert child.parent_cell_line[0] is parent
    if as_vector:
        assert child.parent_cell_line is value


def test_multiple_parents_are_rejected_at_construction():
    with pytest.raises(ValueError, match="CL-CHILD.*exactly one CellLine.*got 2 references"):
        _line("CL-CHILD", parent_cell_line=_vector([_line("CL-A"), _line("CL-B")]))


@pytest.mark.parametrize("wrong_parent", ["culture", "text"])
def test_wrong_reference_target_is_rejected_at_construction(wrong_parent):
    value = _culture("CULT-WRONG") if wrong_parent == "culture" else "CL-ROOT"
    with pytest.raises(TypeError, match="CL-CHILD.*must reference a CellLine"):
        _line("CL-CHILD", parent_cell_line=_vector([value]))


@pytest.mark.parametrize("mutation", ["multiple", "empty", "wrong_target"])
def test_invalid_mutated_parent_is_rejected_before_writing(tmp_path, mutation):
    parent = _line("CL-ROOT")
    second_parent = _line("CL-SECOND")
    child = _line("CL-CHILD", parent_cell_line=parent)
    nwbfile = _file([parent, second_parent, child])
    if mutation == "multiple":
        child.parent_cell_line.append(second_parent)
    elif mutation == "empty":
        child.parent_cell_line.data.clear()
    else:
        child.parent_cell_line.data[0] = nwbfile.subject.culture
    error = TypeError if mutation == "wrong_target" else ValueError
    with NWBHDF5IO(str(tmp_path / "invalid.nwb"), "w") as io:
        with pytest.raises(error, match="CL-CHILD.*parent_cell_line"):
            io.write(nwbfile)


def test_culture_scalar_inputs_are_converted_before_shape_validation():
    line = _line("CL-SOURCE")
    parent = _culture("CULT-PARENT")
    culture = _culture("CULT-CHILD", source_lines=line, parent_cultures=parent)
    assert culture.source_lines[0] is line
    assert culture.parent_cultures[0] is parent


def test_lineage_chain_shared_parent_and_multiple_culture_inputs(tmp_path):
    root = _line("CL-ROOT")
    first = _line("CL-FIRST", parent_cell_line=root)
    sibling = _line("CL-SIBLING", parent_cell_line=root)
    grandchild = _line("CL-GRANDCHILD", parent_cell_line=first)
    culture_a = _culture("CULT-A", source_lines=grandchild)
    culture_b = _culture("CULT-B", source_lines=sibling)
    culture = _culture(
        "CULT-COMBINED", source_lines=[grandchild, sibling], parent_cultures=[culture_a, culture_b]
    )
    nwbfile = _file([root, first, sibling, grandchild], culture, [culture_a, culture_b])
    path = tmp_path / "lineage.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)
    _assert_valid(path)
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        read = io.read()
        lines = read.subject.cell_lines
        assert lines["CL-ROOT"].parent_cell_line is None
        assert lines["CL-FIRST"].parent_cell_line[0] is lines["CL-ROOT"]
        assert lines["CL-SIBLING"].parent_cell_line[0] is lines["CL-ROOT"]
        assert lines["CL-GRANDCHILD"].parent_cell_line[0] is lines["CL-FIRST"]
        assert read.subject.culture.source_lines[:] == [lines["CL-GRANDCHILD"], lines["CL-SIBLING"]]
        assert read.subject.culture.parent_cultures[:] == [
            read.subject.cell_cultures["CULT-A"], read.subject.cell_cultures["CULT-B"]
        ]


def test_parent_line_cached_schema_without_package_import(tmp_path):
    root = _line("CL-ROOT")
    first = _line("CL-FIRST", parent_cell_line=root)
    sibling = _line("CL-SIBLING", parent_cell_line=root)
    grandchild = _line("CL-GRANDCHILD", parent_cell_line=first)
    nwbfile = NWBFile(
        session_description="Cached parent-line schema regression",
        identifier="CACHED-PARENT-LINE",
        session_start_time=datetime(2026, 10, 10, tzinfo=timezone.utc),
    )
    # Core scratch space isolates the CellLine schema from subject-specific Python shims.
    for line in (root, first, sibling, grandchild):
        nwbfile.add_scratch(line)
    path = tmp_path / "cached_lineage.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)
    _assert_valid(path)
    _run_script(
        """
        import sys
        from pynwb import NWBHDF5IO, validate

        assert "ndx_cell_culture" not in sys.modules
        with NWBHDF5IO(sys.argv[1], "r", load_namespaces=True) as io:
            read = io.read()
            lines = read.scratch
            assert lines["CL-ROOT"].parent_cell_line is None
            assert lines["CL-GRANDCHILD"].parent_cell_line[0] is lines["CL-FIRST"]
            assert lines["CL-FIRST"].parent_cell_line[0] is lines["CL-ROOT"]
            assert lines["CL-SIBLING"].parent_cell_line[0] is lines["CL-ROOT"]
        try:
            result = validate(path=sys.argv[1])
        except TypeError:
            result = validate(paths=[sys.argv[1]])
        assert (result[0] if isinstance(result, tuple) else result) == []
        assert "ndx_cell_culture" not in sys.modules
        """,
        path,
    )


def test_cached_schema_validation_rejects_multiple_parents(tmp_path):
    root = _line("CL-ROOT")
    child = _line("CL-CHILD", parent_cell_line=root)
    path = tmp_path / "malformed_parent.nwb"
    with NWBHDF5IO(str(path), "w") as io:
        io.write(_file([root, child]))
    # Model a file written by a tool that bypassed the package's write-time guard.
    with h5py.File(path, "r+") as h5file:
        group = h5file["general/subject/CL-CHILD"]
        attributes = dict(group["parent_cell_line"].attrs)
        del group["parent_cell_line"]
        dataset = group.create_dataset("parent_cell_line", shape=(2,), dtype=h5py.ref_dtype)
        dataset[:] = [h5file["general/subject/CL-ROOT"].ref] * 2
        dataset.attrs.update(attributes)
    errors = _validation_errors(path)
    assert len(errors) == 1
    assert "parent_cell_line" in str(errors[0])
    assert "incorrect shape" in str(errors[0])


def _write_legacy_file(path, release, count):
    namespace_path = Path(__file__).parent / "fixtures" / ("legacy_" + release) / "ndx-cell-culture.namespace.yaml"
    _run_script(
        """
        from datetime import datetime, timezone
        import sys
        import h5py
        from hdmf.common import VectorData
        from pynwb import NWBHDF5IO, NWBFile, get_class, load_namespaces

        load_namespaces(sys.argv[1])
        CellLine = get_class("CellLine", "ndx-cell-culture")
        CellCulture = get_class("CellCulture", "ndx-cell-culture")
        CellCultureSubject = get_class("CellCultureSubject", "ndx-cell-culture")
        def line(name, **kwargs):
            return CellLine(name=name, cell_line_id=name, cell_line_type="parental_cell_line",
                sample_label=name, species="Homo sapiens", cell_source_type="iPSC", **kwargs)
        parents = [line("CL-A"), line("CL-B")]
        count = int(sys.argv[3])
        kwargs = {} if count < 0 else {"parent_cell_line": VectorData(
            name="parent_cell_line", description="Legacy parent references", data=parents[:count])}
        child = line("CL-LEGACY", **kwargs)
        culture = CellCulture(name="CULT-LEGACY", culture_id="CULT-LEGACY", culture_type="organoid",
            sample_label="Legacy culture", species="Homo sapiens")
        subject = CellCultureSubject(subject_id="SUBJ-LEGACY", species="Homo sapiens", sex="U",
            culture=culture, cell_cultures=[culture], cell_lines=parents + [child])
        nwbfile = NWBFile(session_description="Legacy parent regression", identifier="LEGACY-PARENT",
            session_start_time=datetime(2026, 6, 30, tzinfo=timezone.utc), subject=subject)
        with NWBHDF5IO(sys.argv[2], "w") as io:
            io.write(nwbfile)
        if count == 0:
            # HDMF's empty-list writer infers text; create a correctly typed empty reference fixture.
            with h5py.File(sys.argv[2], "r+") as h5file:
                group = h5file["general/subject/CL-LEGACY"]
                attributes = dict(group["parent_cell_line"].attrs)
                del group["parent_cell_line"]
                dataset = group.create_dataset("parent_cell_line", shape=(0,), dtype=h5py.ref_dtype)
                dataset.attrs.update(attributes)
        assert "ndx_cell_culture" not in sys.modules
        """,
        namespace_path,
        path,
        count,
    )


@pytest.mark.parametrize("release", ["rc2", "rc3"])
@pytest.mark.parametrize("count", [-1, 0, 1])
@pytest.mark.filterwarnings("ignore:Ignoring (cached namespace 'ndx-cell-culture' version|the following cached namespace).*:UserWarning")
def test_legacy_parent_files_read_and_export_with_current_schema(tmp_path, release, count):
    legacy_path = tmp_path / "legacy.nwb"
    export_path = tmp_path / "current.nwb"
    _write_legacy_file(legacy_path, release, count)
    if count != 0:
        _assert_valid(legacy_path)
    else:
        # Older HDMF validators infer text from empty data even for an HDF5 reference dataset.
        with h5py.File(legacy_path, "r") as h5file:
            dataset = h5file["general/subject/CL-LEGACY/parent_cell_line"]
            assert h5py.check_dtype(ref=dataset.dtype) is h5py.Reference
    with NWBHDF5IO(str(legacy_path), "r", load_namespaces=True) as io:
        read = io.read()
        child = read.subject.cell_lines["CL-LEGACY"]
        if count <= 0:
            assert child.parent_cell_line is None
        else:
            assert child.parent_cell_line[0] is read.subject.cell_lines["CL-A"]
        with NWBHDF5IO(str(export_path), "w") as out:
            out.export(src_io=io, nwbfile=read, write_args={"link_data": False})
    _assert_valid(export_path)
    with h5py.File(export_path, "r") as h5file:
        current_version = get_type_map().namespace_catalog.get_namespace("ndx-cell-culture").version
        assert list(h5file["specifications/ndx-cell-culture"]) == [current_version]
        # Export must cache the current schema, including its singleton parent
        # constraint, rather than the frozen development rc3 schema.
        cached_schema = json.loads(
            h5file[f"specifications/ndx-cell-culture/{current_version}/ndx-cell-culture.extensions"][()]
        )
        line_spec = next(group for group in cached_schema["groups"] if group.get("neurodata_type_def") == "CellLine")
        parent_spec = next(dataset for dataset in line_spec["datasets"] if dataset["name"] == "parent_cell_line")
        assert parent_spec["shape"] == [1]
        child_group = h5file["general/subject/CL-LEGACY"]
        if count <= 0:
            assert "parent_cell_line" not in child_group
        else:
            assert child_group["parent_cell_line"].shape == (1,)
    with NWBHDF5IO(str(export_path), "r", load_namespaces=True) as io:
        read = io.read()
        parent = read.subject.cell_lines["CL-LEGACY"].parent_cell_line
        if count <= 0:
            assert parent is None
        else:
            assert parent[0] is read.subject.cell_lines["CL-A"]


@pytest.mark.parametrize("release", ["rc2", "rc3"])
@pytest.mark.filterwarnings("ignore:Ignoring (cached namespace 'ndx-cell-culture' version|the following cached namespace).*:UserWarning")
def test_legacy_multiple_parents_fail_with_line_identifier(tmp_path, release):
    path = tmp_path / "legacy_multiple.nwb"
    _write_legacy_file(path, release, 2)
    _assert_valid(path)
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        with pytest.raises((ValueError, ConstructError), match="CL-LEGACY.*exactly one CellLine.*got 2 references"):
            io.read()
