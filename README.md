# ndx-cell-culture

`ndx-cell-culture` is a Neurodata Without Borders (NWB) extension for describing cultured neural preparations in NWB files. It is intended for labs working with organoids, assembloids, directoids/connectoids, slices, explants, dissociated cultures, engineered cell lines, construct applications, recording context, and pharmacology.

Use this extension when the biological preparation is a cultured neural system rather than an animal subject, and when the metadata needed to interpret the recording cannot be represented clearly with core `NWB.Subject` alone.

## What It Models

The extension keeps the NWB subject as the file-level entry point, but makes the recorded culture explicit:

```text
NWBFile
+-- subject : CellCultureSubject <extends NWB.Subject>
|   +-- inherited NWB.Subject fields
|   +-- culture : CellCulture
|       +-- source_lines : CellLine [0..N]
|       +-- parent_cultures : CellCulture [0..N]
|       +-- GeneticVariant [0..N]
|       +-- ConstructApplication [0..N]
|       +-- CultureProtocol [0..1]
+-- general/devices : NWB.Device / NWB.DeviceModel
+-- lab_meta_data : CultureExperimentContext <extends LabMetaData>
    +-- ExperimentContext [0..1]
    +-- Pharmacology [0..N]
```

Extension-owned types:

- `CellCultureSubject`, extending `NWB.Subject`
- `CellCulture`
- `CellLine`
- `GeneticVariant`
- `ConstructApplication`
- `CultureProtocol`
- `CultureExperimentContext`, extending `LabMetaData`
- `ExperimentContext`
- `Pharmacology`

Core NWB types remain responsible for the NWB file, inherited subject metadata, recording devices, electrodes, acquisition data, imaging data, stimulus data, and other modality-specific structures.

## Installation

Install from the repository:

```bash
python -m pip install git+https://github.com/braingeneers/ndx-cell-culture.git
```

For local development:

```bash
git clone git@github.com:braingeneers/ndx-cell-culture.git
cd ndx-cell-culture
python -m pip install -e ".[dev]"
```

## Quickstart

```python
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBHDF5IO, NWBFile

from ndx_cell_culture import (
    CellCulture,
    CellCultureSubject,
    CellLine,
    CultureExperimentContext,
    CultureProtocol,
    ExperimentContext,
)

line = CellLine(
    name="line",
    cell_line_id="CL-SYN-001",
    cell_line_type="parental_cell_line",
    sample_label="Synthetic iPSC line",
    species="Homo sapiens",
    cell_source_type="iPSC",
    passage_number="p35",
)

protocol = CultureProtocol(
    name="protocol",
    protocol_id="PROTO-SYN-CORTICAL-001",
    protocol_name="Synthetic cortical organoid protocol",
    patterning_summary="forebrain patterning",
    media_summary="neural induction and maturation media",
)

culture = CellCulture(
    name="culture",
    culture_id="CULT-SYN-ORG-001",
    culture_type="organoid",
    sample_label="Synthetic cortical organoid",
    species="Homo sapiens",
    culture_subtype="cortical",
    age="P120D",
    age_reference="days_post_induction",
    cell_lines=[line],
    culture_protocol=protocol,
)

subject = CellCultureSubject(
    subject_id="SUBJ-SYN-ORG-001",
    species="Homo sapiens",
    description="Synthetic cortical organoid recording",
    culture=culture,
)

nwbfile = NWBFile(
    session_description="synthetic organoid recording",
    identifier="NWB-SYN-ORG-001",
    session_start_time=datetime(2026, 1, 1, tzinfo=tzlocal()),
)
nwbfile.subject = subject

device = nwbfile.create_device(name="Example MEA device")

experiment = ExperimentContext(
    name="experiment",
    experiment_id="EXP-SYN-ORG-001",
    subject=subject,
    culture=culture,
    age_at_recording="P120D",
    age_reference="days_post_induction",
    recording_platform="MEA",
    recording_duration_s=1800.0,
    spontaneous_activity=True,
    pharmacology_present=False,
    device=device,
)

nwbfile.add_lab_meta_data(
    CultureExperimentContext(
        name="culture_experiment_context",
        experiment_context=experiment,
    )
)

with NWBHDF5IO("synthetic_organoid.nwb", "w") as io:
    io.write(nwbfile)
```

## Modeling Guidance

- Put the recorded or described preparation in `CellCultureSubject.culture`.
- Use inherited `NWB.Subject` fields for normal subject metadata. Do not put culture age in `NWB.Subject.age`; use `CellCulture.age` and `ExperimentContext.age_at_recording`.
- Use `CellCulture` for the biological preparation: organoid, spheroid, assembloid, slice, explant, dissociated culture, or other cultured neural preparation.
- Use `CellLine` for source line, passage, clone, donor/line provenance, and cell source type.
- Use `CellCulture.source_lines` for one or more source lines when a culture is derived from multiple lines.
- Use `CellCulture.parent_cultures` for culture-to-culture provenance, such as organoid-to-slice or multi-parent assembloid/directoid derivation.
- Use `CellCulture.batch_label` only as a lightweight grouping/search label. Batches are not modeled as separate objects.
- Use `GeneticVariant` for stable or defining engineered genomic changes.
- Use `ConstructApplication` for applied constructs, viral vectors, RNPs, reporters, optogenetic tools, or similar interventions. Attach the construct at the level where it was applied.
- Use `CultureProtocol` for concise structured culture protocol metadata. Detailed protocol documents can be referenced with `protocol_uri` or `protocol_doi`.
- Use `ExperimentContext` and `Pharmacology` for session-level recording context and compounds applied during the experiment.
- Use core NWB `Device` / `DeviceModel` for hardware identity. Detailed acquisition, electrode, imaging, and stimulus data should use the appropriate core NWB structures.

## Examples

Run the basic example:

```bash
python examples/create_basic_organoid_nwb.py
```

Run all synthetic scenario examples:

```bash
python examples/create_synthetic_scenarios.py
```

Generated `.nwb` files are written under `examples/` and ignored by git. The scenarios cover organoid recordings, slices, edited cell lines, pharmacology, directoid-style preparations, and two-line assembloids using synthetic identifiers.

More detail is available in:

- [Data modeling guide](docs/design.md)
- [Schema reference](docs/field_reference.md)
- [Synthetic examples](docs/examples.md)
- [Maintainer review notes](docs/maintainer_review.md)

## DANDI And NWB Notes

NWB files that use this extension require the `ndx-cell-culture` namespace and extension schema to be available when reading or validating the file. Before depositing data, validate the NWB files in the same environment used to create them and make sure the DANDI dataset documentation names the extension dependency.

This extension stores metadata that helps users find, interpret, and compare cultured neural recordings. It does not replace core NWB acquisition, stimulus, electrode, imaging, processing, or device metadata.

## Development

Regenerate the YAML schema:

```bash
python src/spec/create_extension_spec.py
```

Run tests:

```bash
pytest
```

Continuous integration regenerates the schema, runs PyNWB round-trip tests, executes the example writers, and verifies that built wheels include the namespace and extension YAML files.

## Status

This package is an alpha NDX draft. The schema and examples are intended for review with NWB maintainers before broad publication or any proposal for mainline NWB inclusion.

Known review point: recursive and multi-parent provenance relationships such as `CellCulture.parent_cultures`, `CellCulture.source_lines`, and `CellLine.parent_cell_line` are represented in the draft schema as optional generic NWB links. NWB maintainers should confirm whether those relationships should remain generic links, move into a shared container/catalog, use relationship tables, or be represented with another HDMF/NWB idiom before release.
