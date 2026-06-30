"""Create a small NWB file using ndx-cell-culture.

Run from the repository root after installing the package:

    python -m pip install -e .
    python examples/create_basic_organoid_nwb.py
"""

from pathlib import Path

from pynwb import NWBHDF5IO

from scenario_builders import build_basic_organoid


def main(output_path=None):
    output_path = Path(output_path) if output_path is not None else Path(__file__).with_name("basic_organoid_example.nwb")
    with NWBHDF5IO(str(output_path), "w") as io:
        io.write(build_basic_organoid())
    print(output_path)
    return output_path


if __name__ == "__main__":
    main()
