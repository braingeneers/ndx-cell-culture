"""Verify an index serves exactly the two distributions in a release bundle."""

import argparse
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def verify_files(distribution_dir, published_files):
    paths = sorted(Path(distribution_dir).iterdir())
    if len(paths) != 2 or len([path for path in paths if path.suffix == ".whl"]) != 1 or len(
        [path for path in paths if path.name.endswith(".tar.gz")]
    ) != 1:
        raise ValueError("Release bundle must contain exactly one wheel and one source distribution")
    expected = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    actual = {item["filename"]: item["digests"]["sha256"] for item in published_files}
    if expected != actual:
        raise ValueError("Published filenames/checksums differ from the verified release bundle")


def verify_index(index, release_version, distribution_dir):
    host = "test.pypi.org" if index == "testpypi" else "pypi.org"
    url = "https://{}/pypi/ndx-cell-culture/{}/json".format(host, release_version)
    for attempt in range(12):
        try:
            with urlopen(url, timeout=20) as response:
                metadata = json.load(response)
            assert metadata["info"]["version"] == release_version
            verify_files(distribution_dir, metadata["urls"])
            print("{} filenames and SHA-256 checksums match the release bundle".format(index))
            return
        except HTTPError as exc:
            if exc.code != 404 or attempt == 11:
                raise
        except URLError:
            if attempt == 11:
                raise
        time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", choices=["testpypi", "pypi"], required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--dist-dir", type=Path, required=True)
    arguments = parser.parse_args()
    verify_index(arguments.index, arguments.version, arguments.dist_dir)
