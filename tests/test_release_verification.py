"""Publication must reject files that differ from the verified release bundle."""

import hashlib
import importlib.util
from pathlib import Path

import pytest


_script = Path(__file__).resolve().parents[1] / "scripts" / "verify_release_index.py"
_spec = importlib.util.spec_from_file_location("verify_release_index", _script)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)


@pytest.fixture
def distributions(tmp_path):
    published = []
    for name, data in [("ndx_cell_culture-1.0.0-py3-none-any.whl", b"wheel"),
                       ("ndx_cell_culture-1.0.0.tar.gz", b"sdist")]:
        (tmp_path / name).write_bytes(data)
        published.append({"filename": name, "digests": {"sha256": hashlib.sha256(data).hexdigest()}})
    return tmp_path, published


def test_identical_published_distributions_pass(distributions):
    directory, published = distributions
    _module.verify_files(directory, published)


@pytest.mark.parametrize("change", ["different-content", "missing-file", "extra-file"])
def test_different_published_distributions_fail(distributions, change):
    directory, published = distributions
    if change == "different-content":
        published[0]["digests"]["sha256"] = "0" * 64
    elif change == "missing-file":
        published.pop()
    else:
        published.append({"filename": "unexpected.whl", "digests": {"sha256": "0" * 64}})
    with pytest.raises(ValueError, match="filenames/checksums differ"):
        _module.verify_files(directory, published)


def test_old_distributions_cannot_enter_release_bundle(distributions):
    directory, published = distributions
    (directory / "ndx_cell_culture-1.0rc3.tar.gz").write_bytes(b"old release")
    with pytest.raises(ValueError, match="exactly one wheel and one source"):
        _module.verify_files(directory, published)
