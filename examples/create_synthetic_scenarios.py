"""Write all ndx-cell-culture synthetic scenario NWB files."""

from pathlib import Path

from pynwb import NWBHDF5IO

from scenario_builders import SCENARIOS


def main(output_dir=None):
    output_dir = Path(output_dir) if output_dir is not None else Path(__file__).with_name("generated_scenarios")
    output_dir.mkdir(exist_ok=True)
    paths = []
    for name, builder in SCENARIOS.items():
        path = output_dir / f"{name}.nwb"
        with NWBHDF5IO(str(path), "w") as io:
            io.write(builder())
        print(path)
        paths.append(path)
    return paths


if __name__ == "__main__":
    main()
