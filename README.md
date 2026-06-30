# ndx-cell-culture

[![tests](https://github.com/braingeneers/ndx-cell-culture/actions/workflows/test.yml/badge.svg)](https://github.com/braingeneers/ndx-cell-culture/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/ndx-cell-culture/badge/?version=latest)](https://ndx-cell-culture.readthedocs.io/)

`ndx-cell-culture` is a Neurodata Without Borders (NWB) extension for describing cultured neural preparations in NWB files. It is intended for labs working with organoids, assembloids, directoids/connectoids, slices, explants, spheroids, dissociated cultures, engineered cell lines, construct applications, recording context, and pharmacology.

Full user documentation is available at <https://ndx-cell-culture.readthedocs.io/>.

## What It Models

The extension keeps core NWB responsible for devices, acquisition, stimulus, imaging, processing, and other modality-specific data. Cultured-preparation identity and provenance are attached through the subject; recording context and pharmacology live in lab metadata:

```text
NWBFile
+-- subject : CellCultureSubject <extends NWB.Subject>
|   +-- inherited NWB.Subject fields
|   +-- culture -> CellCulture [recorded/described preparation]
|   +-- CellLine [0..N]
|   |   +-- parent_cell_line -> CellLine [0..1]
|   |   +-- GeneticVariant [0..N]
|   |   +-- ConstructApplication [0..N]
|   +-- CellCulture [0..N] [recorded, related, or parent cultures]
|   |   +-- source_lines -> CellLine [0..N]
|   |   +-- parent_cultures -> CellCulture [0..N]
|   |   +-- GeneticVariant [0..N]
|   |   +-- ConstructApplication [0..N]
|   |   +-- CultureProtocol [0..1]
+-- general/devices : NWB.Device [0..N]
+-- general/devices/models : NWB.DeviceModel [0..N] [hardware model metadata]
+-- lab metadata : CultureExperimentContext <extends LabMetaData>
    +-- ExperimentContext [0..1]
    |   +-- subject -> CellCultureSubject
    |   +-- culture -> CellCulture
    |   +-- device -> NWB.Device [0..1]
    +-- Pharmacology [0..N]
```

The core mental model is to keep biological preparation metadata, core NWB data
and hardware, and recording context distinct but linked:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontFamily": "Inter, Arial, sans-serif",
    "fontSize": "15px",
    "primaryColor": "#f8fafc",
    "primaryTextColor": "#111827",
    "primaryBorderColor": "#64748b",
    "lineColor": "#64748b",
    "clusterBkg": "#f1f5f9",
    "clusterBorder": "#94a3b8"
  }
}}%%
flowchart LR
  subgraph Biology["Biological preparation"]
    Subject["CellCultureSubject"]
    Culture["CellCulture"]
    Line["CellLine"]
    BioExt["GeneticVariant<br/>ConstructApplication<br/>CultureProtocol"]

    Subject --> Culture
    Culture -.-> Line
    Culture --> BioExt
  end

  subgraph Core["Core NWB"]
    Device["NWB.Device<br/>NWB.DeviceModel"]
    Data["recorded data<br/>standard NWB metadata"]
  end

  subgraph Session["Recording context"]
    Context["CultureExperimentContext"]
    Experiment["ExperimentContext"]
    Pharm["Pharmacology"]

    Context --> Experiment
    Context --> Pharm
  end

  Biology -.-> Session
  Device -.-> Session
```

Use this mental model:

- Put biological identity and provenance in `CellCultureSubject`.
- Put recorded data and hardware in core NWB.
- Put recording conditions and pharmacology in `CultureExperimentContext`.
- Dotted arrows show references: `CellCulture.source_lines`, plus recording-context links back to the recorded `CellCulture` and `NWB.Device`.

Use this extension when the biological preparation is a cultured neural system rather than an animal subject, and when the metadata needed to interpret the recording cannot be represented clearly with core `NWB.Subject` alone.

## Installation

Install the current release candidate from GitHub:

```bash
python -m pip install git+https://github.com/braingeneers/ndx-cell-culture.git
```

For local development:

```bash
git clone git@github.com:braingeneers/ndx-cell-culture.git
cd ndx-cell-culture
python -m pip install -e ".[dev]"
```

## Documentation

Start with the hosted documentation:

- [Installation and quickstart](https://ndx-cell-culture.readthedocs.io/en/latest/usage.html)
- [Which objects do I need?](https://ndx-cell-culture.readthedocs.io/en/latest/usage.html#which-objects-do-i-need)
- [Modeling guide](https://ndx-cell-culture.readthedocs.io/en/latest/modeling_guide.html)
- [Field reference](https://ndx-cell-culture.readthedocs.io/en/latest/field_reference.html)
- [Examples and recipes](https://ndx-cell-culture.readthedocs.io/en/latest/examples.html)
- [Validation and DANDI notes](https://ndx-cell-culture.readthedocs.io/en/latest/validation_dandi.html)
- [Generated schema reference](https://ndx-cell-culture.readthedocs.io/en/latest/format.html)

## Examples

Run the basic synthetic example:

```bash
python examples/create_basic_organoid_nwb.py
```

Run all synthetic scenario examples:

```bash
python examples/create_synthetic_scenarios.py
```

Generated `.nwb` files are written under `examples/` and ignored by git. The scenarios cover organoid recordings, slices, edited cell lines, pharmacology, directoid-style preparations, and two-line assembloids using synthetic identifiers.

## Development

Regenerate the YAML schema:

```bash
python scripts/create_extension_spec.py
```

Run the local release checks:

```bash
bash scripts/check_release.sh
```

Build the HTML documentation:

```bash
python -m pip install -e ".[docs]"
make -C docs/source html
```

The generated site is written to `docs/_build/html`. Continuous integration runs the same release-check script across supported Python versions, including schema regeneration, PyNWB round-trip tests, example writers, NWB Inspector, docs build, clean wheel installation, and wheel/source distribution checks.

## Status

This package is a release-candidate NDX intended for stakeholder and NWB maintainer review. The core model is encoded in the schema and documentation, and automated tests cover the public examples and relationship model.
