"""Exercise DANDI's subject checks on written extension files."""

from datetime import datetime, timezone
from pathlib import Path
import re
from textwrap import dedent

from nwbinspector import Importance, inspect_nwbfile, load_config
from pynwb import NWBHDF5IO, NWBFile
import pytest

import ndx_cell_culture as ndx


def _write_subject(path, **subject_fields):
    culture = ndx.CellCulture(
        name="CULT-SYN-DANDI",
        culture_id="CULT-SYN-DANDI",
        culture_type="organoid",
        sample_label="Synthetic culture",
        species="Homo sapiens",
        age="P120D",
        age_reference="days_post_aggregation",
    )
    nwbfile = NWBFile(
        session_description="Synthetic DANDI subject metadata check",
        identifier="DANDI-SUBJECT-CHECK",
        session_start_time=datetime(2026, 5, 12, tzinfo=timezone.utc),
    )
    nwbfile.subject = ndx.CellCultureSubject(
        subject_id="synthetic-subject",
        species="Homo sapiens",
        culture=culture,
        **subject_fields,
    )
    with NWBHDF5IO(str(path), "w") as io:
        io.write(nwbfile)


def _critical_subject_checks(path):
    return {
        message.check_function_name
        for message in inspect_nwbfile(
            nwbfile_path=str(path),
            config=load_config("dandi"),
            importance_threshold=Importance.CRITICAL,
        )
    }


@pytest.mark.parametrize(
    "subject_fields",
    [
        {"age": "P30Y", "sex": "F"},
        {"age": "P25Y/P35Y", "sex": "U"},
        {"age": "P5D", "age__reference": "gestational", "sex": "F"},
        {"date_of_birth": datetime(1996, 5, 12, tzinfo=timezone.utc), "sex": "U"},
    ],
    ids=["donor-age", "donor-age-range", "embryonic-source", "birth-date-only"],
)
def test_dandi_subject_checks_accept_inherited_metadata(tmp_path, subject_fields):
    path = tmp_path / "complete.nwb"
    _write_subject(path, **subject_fields)
    assert _critical_subject_checks(path) == set()
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        nwbfile = io.read()
        assert nwbfile.subject.culture.age == "P120D"
        for field, value in subject_fields.items():
            assert getattr(nwbfile.subject, field) == value
        assert nwbfile.subject.age != nwbfile.subject.culture.age


@pytest.mark.parametrize(
    "subject_fields, expected_checks",
    [
        ({"sex": "U"}, {"check_subject_age"}),
        ({"age": "P30Y"}, {"check_subject_sex"}),
        ({}, {"check_subject_age", "check_subject_sex"}),
    ],
    ids=["culture-age-does-not-fill-core-age", "missing-sex", "both-missing"],
)
def test_dandi_reports_missing_inherited_subject_metadata(tmp_path, subject_fields, expected_checks):
    path = tmp_path / "incomplete.nwb"
    _write_subject(path, **subject_fields)
    assert _critical_subject_checks(path) == expected_checks


_QUICKSTART = Path(__file__).resolve().parents[1] / "docs/source/source/usage.rst"
_QUICKSTART_WRITERS = [
    dedent(match.group(1))
    for match in re.finditer(
        r"^\.\. code-block:: python\n\n((?:^(?:   .*)?\n)+)",
        _QUICKSTART.read_text(),
        flags=re.MULTILINE,
    )
    if "io.write(nwbfile)" in match.group(1)
]


@pytest.mark.parametrize("code", _QUICKSTART_WRITERS, ids=["minimal", "recording-context"])
def test_quickstart_files_pass_dandi_subject_checks(tmp_path, monkeypatch, code):
    monkeypatch.chdir(tmp_path)
    exec(compile(code, str(_QUICKSTART), "exec"), {})
    paths = list(tmp_path.glob("*.nwb"))
    assert len(paths) == 1
    assert _critical_subject_checks(paths[0]) == set()
