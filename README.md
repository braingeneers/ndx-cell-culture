# ndx-cell-culture

`ndx-cell-culture` is an NWB Neurodata Extension for cultured neural preparations and related metadata. It covers organoids, assembloids, directoid/connectoid-style preparations, slices, explants, dissociated cultures, cell-line provenance, engineered variants, construct applications, structured culture protocols, recording context, and pharmacology.

This repository is the formal extension implementation derived from the Braingeneers organoid/cell-culture metadata workbook and formal notes.

Design artifacts that led to this formal draft are maintained in the companion design repository `braingeneers/nwb-organoid-extension`, especially:

- `workbook/nwb_organoid_sample_workbook_v0.74.xlsx`
- `workbook/nwb_organoid_formal_extension_notes_v0.74.md`
- `docs/formal_nwb_extension_build_plan.md`

## Scope

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

Core NWB types reused directly:

- `NWBFile`
- `NWB.Subject`
- `LabMetaData`
- `Device`
- `DeviceModel`
- modality-specific acquisition/electrode/imaging/stimulus metadata

## Development

Create or update the generated YAML schema:

```bash
python src/spec/create_extension_spec.py
```

Install locally:

```bash
python -m pip install -e .
```

Run tests:

```bash
pytest
```

Run the example:

```bash
python examples/create_basic_organoid_nwb.py
```

Write all review scenarios:

```bash
python examples/create_review_scenarios.py
```

Review examples currently cover:

- basic organoid
- organoid-derived slice with patch-clamp hardware and two pharmacology entries
- KOLF/SHANK3 Org1 manual validation row
- KOLF/SHANK3 Org2 manual validation row without experiment context
- H9-DO11 Ketamine manual validation row with pharmacology
- directoid/connectoid-style assembloid metadata
- two-line assembloid metadata

Reviewer documentation:

- [Design notes](docs/design.md)
- [Field reference](docs/field_reference.md)
- [Review examples](docs/examples.md)
- [Maintainer review notes](docs/maintainer_review.md)

## Design Principles

- Reuse NWB core metadata wherever possible.
- Extend `NWB.Subject` with a single required `culture` relationship rather than duplicating inherited subject fields.
- Keep recording hardware in core NWB `Device` / `DeviceModel`.
- Use formal NWB links/references for relationships that were helper ID columns in the review workbook.
- Do not model batches as objects; use `CellCulture.batch_label`.
- Keep controlled workbook dropdowns as recommended terms unless NWB maintainers request hard enum constraints.

## Review Status

This is an initial formal NDX draft. The schema and examples are intended for review with NWB maintainers before publication or mainline consideration.

Known review point: recursive and multi-parent provenance relationships such as `CellCulture.parent_cultures`, `CellCulture.source_lines`, and `CellLine.parent_cell_line` are represented in the draft schema as optional generic NWB links. The validated examples exercise the stable containment and non-recursive link paths; NWB maintainers should confirm whether those recursive provenance relationships should remain generic links, move into a shared container/catalog, use relationship tables, or be represented with another HDMF/NWB idiom before release.

Continuous integration regenerates the schema, runs the PyNWB round-trip tests, executes the example and review scenario writers, and verifies that built wheels include the namespace and extension YAML files.
