# ndx-cell-culture

[![tests](https://github.com/braingeneers/ndx-cell-culture/actions/workflows/test.yml/badge.svg)](https://github.com/braingeneers/ndx-cell-culture/actions/workflows/test.yml)

`ndx-cell-culture` is a Neurodata Without Borders (NWB) extension for describing cultured neural preparations in NWB files. It is intended for labs working with organoids, assembloids, directoids/connectoids, slices, explants, spheroids, dissociated cultures, engineered cell lines, construct applications, recording context, and pharmacology.

Use this extension when the biological preparation is a cultured neural system rather than an animal subject, and when the metadata needed to interpret the recording cannot be represented clearly with core `NWB.Subject` alone.

## What It Models

The extension keeps the NWB subject as the file-level entry point, but stores reusable culture and cell-line objects in a shared metadata catalog:

```text
NWBFile
+-- subject : CellCultureSubject <extends NWB.Subject>
|   +-- inherited NWB.Subject fields
|   +-- culture -> CellCulture catalog entry
+-- general/devices : NWB.Device / NWB.DeviceModel
+-- lab_meta_data : CultureExperimentContext <extends LabMetaData>
    +-- CellLine [0..N]
    |   +-- GeneticVariant [0..N]
    |   +-- ConstructApplication [0..N]
    +-- CellCulture [0..N]
    |   +-- GeneticVariant [0..N]
    |   +-- ConstructApplication [0..N]
    |   +-- CultureProtocol [0..1]
    +-- CellLineParentRelation [0..N]
    +-- CellCultureSourceLineRelation [0..N]
    +-- CellCultureParentRelation [0..N]
    +-- ExperimentContext [0..1]
    +-- Pharmacology [0..N]
```

Extension-owned types:

- `CellCultureSubject`, extending `NWB.Subject`
- `CellCulture`
- `CellLine`
- `CellLineParentRelation`
- `CellCultureSourceLineRelation`
- `CellCultureParentRelation`
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
    CellCultureSourceLineRelation,
    CellCultureSubject,
    CellLine,
    CultureExperimentContext,
    CultureProtocol,
    ExperimentContext,
)

line = CellLine(
    name="CL-SYN-001",
    cell_line_id="CL-SYN-001",
    cell_line_type="parental_cell_line",
    sample_label="Synthetic iPSC line",
    species="Homo sapiens",
    cell_source_type="iPSC",
    passage_number="p35",
)

protocol = CultureProtocol(
    name="PROTO-SYN-CORTICAL-001",
    protocol_id="PROTO-SYN-CORTICAL-001",
    protocol_name="Synthetic cortical organoid protocol",
    patterning_summary="forebrain patterning",
    media_summary="neural induction and maturation media",
)

culture = CellCulture(
    name="CULT-SYN-ORG-001",
    culture_id="CULT-SYN-ORG-001",
    culture_type="organoid",
    sample_label="Synthetic cortical organoid",
    species="Homo sapiens",
    culture_subtype="cortical",
    age="P120D",
    age_reference="days_post_induction",
    culture_protocol=protocol,
)

source_relation = CellCultureSourceLineRelation(
    name="REL-SYN-ORG-SOURCE-001",
    relation_id="REL-SYN-ORG-SOURCE-001",
    culture=culture,
    source_line=line,
    role="primary_source",
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
    name="EXP-SYN-ORG-001",
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
        cell_lines=[line],
        cell_cultures=[culture],
        cell_culture_source_line_relations=[source_relation],
        experiment_context=experiment,
    )
)

with NWBHDF5IO("synthetic_organoid.nwb", "w") as io:
    io.write(nwbfile)
```

## Modeling Guidance

- Put the recorded or described preparation in `CellCultureSubject.culture` as a link to a cataloged `CellCulture`.
- Store reusable `CellLine` and `CellCulture` entries in `CultureExperimentContext`.
- Use inherited `NWB.Subject` fields for normal subject metadata. Do not put culture age in `NWB.Subject.age`; use `CellCulture.age` and `ExperimentContext.age_at_recording`.
- Use `CellCultureSourceLineRelation` to link a culture to one or more source lines.
- Use `CellLineParentRelation` for donor, parental, derived, cloned, edited, or reprogrammed line provenance.
- Use `CellCultureParentRelation` for organoid-to-slice, assembloid, directoid/connectoid, co-culture, or other culture-to-culture provenance.
- Use `CellCulture.batch_label` only as a lightweight grouping/search label. Batches are not modeled as separate objects.
- Use `GeneticVariant` for stable or defining engineered genomic changes.
- Use `ConstructApplication` for applied constructs, viral vectors, RNPs, reporters, optogenetic tools, or similar interventions. Attach the construct at the level where it was applied.
- Use `CultureProtocol` for concise structured culture protocol metadata. Detailed protocol documents can be referenced with `protocol_uri` or `protocol_doi`.
- Use `ExperimentContext` and `Pharmacology` for session-level recording context and compounds applied during the experiment.
- Use core NWB `Device` / `DeviceModel` for hardware identity. Detailed acquisition, electrode, imaging, and stimulus data should use the appropriate core NWB structures.
- Use the public `pharmacologies=[...]` constructor argument when adding repeated `Pharmacology` records to `CultureExperimentContext`.

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
- [Architecture decisions](docs/architecture_decisions.md)
- [Release checklist](docs/release.md)

## DANDI And NWB Notes

NWB files that use this extension require the `ndx-cell-culture` namespace and extension schema to be available when reading or validating the file. Before depositing data, validate the NWB files in the same environment used to create them and make sure the DANDI dataset documentation names the extension dependency.

This extension stores metadata that helps users find, interpret, and compare cultured neural recordings. It does not replace core NWB acquisition, stimulus, electrode, imaging, processing, or device metadata.

Recommended vocabulary terms are stored as text in the NWB schema, following common NWB practice. Use `ndx_cell_culture.validate_recommended_terms(nwbfile)` before sharing or depositing files if you want opt-in checking for values such as `culture_type`, `cell_source_type`, `recording_platform`, and concentration units.

## Development

Regenerate the YAML schema:

```bash
python src/spec/create_extension_spec.py
```

Run tests:

```bash
pytest
```

Build the HTML documentation:

```bash
python -m pip install -e ".[docs]"
make -C docs/source html
```

The generated site is written to `docs/_build/html`.
The repository also includes `.readthedocs.yaml`, so Read the Docs can import the GitHub repository and build from `docs/source/source/conf.py`.

Continuous integration regenerates the schema, runs PyNWB round-trip tests, executes the example writers, runs NWB Inspector, builds the docs, verifies clean wheel installation, and checks wheel/source distributions before release.

## Status

This package is a release-candidate NDX intended for final stakeholder and NWB maintainer review. The core modeling decisions are encoded in the schema and documentation, automated tests cover the public examples and relationship model, and the repository is intended to be releasable after approval.
