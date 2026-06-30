#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TMP_DIR="$(mktemp -d /tmp/ndx-cell-culture-release-check.XXXXXX)"
cleanup() {
    trash "$TMP_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

python scripts/create_extension_spec.py
git diff --exit-code -- spec/ndx-cell-culture.namespace.yaml spec/ndx-cell-culture.extensions.yaml

pytest -q

python examples/create_basic_organoid_nwb.py
python examples/create_synthetic_scenarios.py

python - <<'PY'
from pathlib import Path

import ndx_cell_culture as ndx
from nwbinspector import Importance, inspect_nwbfile
from pynwb import NWBHDF5IO, validate


def assert_no_validation_errors(path):
    try:
        result = validate(path=str(path))
    except TypeError:
        result = validate(paths=[str(path)])
    errors = result[0] if isinstance(result, tuple) else result
    assert errors == [], (path, errors)


def assert_no_inspector_violations(path):
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
    assert messages == [], (path, messages)


paths = [Path("examples/basic_organoid_example.nwb")]
paths.extend(sorted(Path("examples/generated_scenarios").glob("*.nwb")))
assert len(paths) == 8, paths

for path in paths:
    assert path.exists(), path
    assert_no_validation_errors(path)
    assert_no_inspector_violations(path)
    with NWBHDF5IO(str(path), "r", load_namespaces=True) as io:
        nwbfile = io.read()
        assert ndx.validate_recommended_terms(nwbfile) == []
PY

sphinx-build -W -b html docs/source/source docs/_build/html

python -m build --sdist --wheel --outdir "$TMP_DIR/dist"
python -m twine check "$TMP_DIR"/dist/*

python - <<PY
from pathlib import Path
from tarfile import open as open_tar
from zipfile import ZipFile

dist = Path("$TMP_DIR/dist")
wheel = next(dist.glob("ndx_cell_culture-*.whl"))
sdist = next(dist.glob("ndx_cell_culture-*.tar.gz"))
required_wheel = {
    "ndx_cell_culture/spec/ndx-cell-culture.namespace.yaml",
    "ndx_cell_culture/spec/ndx-cell-culture.extensions.yaml",
    "ndx_cell_culture/validation.py",
}
with ZipFile(wheel) as zf:
    wheel_names = set(zf.namelist())
assert required_wheel <= wheel_names

with open_tar(sdist) as tf:
    sdist_names = set(tf.getnames())
assert any(name.endswith("spec/ndx-cell-culture.namespace.yaml") for name in sdist_names)
assert any(name.endswith("spec/ndx-cell-culture.extensions.yaml") for name in sdist_names)
assert any(name.endswith("scripts/check_release.sh") for name in sdist_names)
assert any(name.endswith("scripts/create_extension_spec.py") for name in sdist_names)
PY

python -m venv "$TMP_DIR/venv"
"$TMP_DIR/venv/bin/python" -m pip install --upgrade pip
"$TMP_DIR/venv/bin/python" -m pip install "$TMP_DIR"/dist/ndx_cell_culture-*.whl
"$TMP_DIR/venv/bin/python" - <<'PY'
import ndx_cell_culture as ndx

assert ndx.CellCultureSubject.__name__ == "CellCultureSubject"
assert ndx.CellCulture.__name__ == "CellCulture"
assert ndx.CellLine.__name__ == "CellLine"
assert ndx.CultureProtocol.__name__ == "CultureProtocol"
assert ndx.CultureExperimentContext.__name__ == "CultureExperimentContext"
assert ndx.ExperimentContext.__name__ == "ExperimentContext"
assert ndx.Pharmacology.__name__ == "Pharmacology"
assert not hasattr(ndx, "CellLineParentRelation")
assert not hasattr(ndx, "CellCultureSourceLineRelation")
assert not hasattr(ndx, "CellCultureParentRelation")
assert hasattr(ndx.CultureExperimentContext, "pharmacologies")
assert hasattr(ndx.CultureExperimentContext, "add_pharmacologies")
assert hasattr(ndx.CultureExperimentContext, "get_pharmacologies")
assert callable(ndx.validate_recommended_terms)
PY
