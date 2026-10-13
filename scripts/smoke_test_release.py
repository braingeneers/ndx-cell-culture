"""Check an installed distribution's version, schema, and NWB round-trip."""

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

import h5py
import ndx_cell_culture as ndx
from pynwb import NWBHDF5IO, NWBFile, get_type_map, validate


def smoke_test(expected_version):
    assert version("ndx-cell-culture") == expected_version
    namespace = get_type_map().namespace_catalog.get_namespace("ndx-cell-culture")
    assert namespace.version == expected_version
    assert not hasattr(ndx, "CultureExperimentContext")

    parent = ndx.CellLine(
        name="parent", cell_line_id="parent", cell_line_type="parental_cell_line",
        sample_label="Synthetic parent", species="Homo sapiens", cell_source_type="iPSC",
    )
    child = ndx.CellLine(
        name="child", cell_line_id="child", cell_line_type="derived_cell_line",
        sample_label="Synthetic child", species="Homo sapiens", cell_source_type="iPSC",
        parent_cell_line=parent,
    )
    culture = ndx.CellCulture(
        name="CULT-SMOKE", culture_id="CULT-SMOKE", culture_type="organoid",
        sample_label="Synthetic organoid", species="Homo sapiens", source_lines=child,
    )
    nwbfile = NWBFile(
        session_description="Synthetic release installation check",
        identifier="release-smoke-test",
        session_start_time=datetime(2026, 10, 13, tzinfo=timezone.utc),
    )
    nwbfile.subject = ndx.CellCultureSubject(
        subject_id="synthetic", species="Homo sapiens", sex="U", age="P30Y",
        description="Synthetic source donor age for an installation test", culture=culture,
    )
    nwbfile.add_lab_meta_data(ndx.ExperimentContext(
        name="recording", experiment_id="recording", age_at_recording="P60D",
        age_reference="days_post_induction", recording_platform="MEA",
    ))

    with TemporaryDirectory(prefix="ndx-cell-culture-smoke-") as temporary_dir:
        path = Path(temporary_dir) / "smoke.nwb"
        with NWBHDF5IO(str(path), "w") as io:
            io.write(nwbfile)
        try:
            result = validate(path=str(path))
        except TypeError:
            result = validate(paths=[str(path)])
        errors = result[0] if isinstance(result, tuple) else result
        assert errors == [], errors
        with h5py.File(path, "r") as h5file:
            assert list(h5file["specifications/ndx-cell-culture"]) == [expected_version]
        with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
            read = io.read()
            assert read.subject.culture.source_lines[0] is read.subject.cell_lines["child"]
            assert read.subject.cell_lines["child"].parent_cell_line[0] is read.subject.cell_lines["parent"]
            assert read.lab_meta_data["recording"].culture is read.subject.culture
            assert ndx.validate_recommended_terms(read) == []
    print("Installed ndx-cell-culture {}: version, schema, and NWB round-trip passed".format(expected_version))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    smoke_test(parser.parse_args().version)
