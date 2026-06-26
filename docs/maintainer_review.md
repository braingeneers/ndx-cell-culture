# Maintainer Review Notes

This page collects the questions and checks intended for NWB architects/admins reviewing the `ndx-cell-culture` draft.

## Review Bundle

The current repository provides:

- namespace YAML: `spec/ndx-cell-culture.namespace.yaml`;
- extension YAML: `spec/ndx-cell-culture.extensions.yaml`;
- schema generator: `src/spec/create_extension_spec.py`;
- PyNWB dynamic bindings: `src/ndx_cell_culture/__init__.py`;
- round-trip tests: `tests/test_schema.py`;
- synthetic examples: `examples/scenario_builders.py`;
- design notes: `docs/design.md`;
- field reference: `docs/field_reference.md`.

## Decisions Requested

Please review these points before release or mainline schema consideration:

1. Should repeated child objects such as variants, construct applications, and pharmacology remain semantic child groups, or should any be represented as `DynamicTable`s?
2. Should recursive provenance relationships (`CellCulture.parent_cultures`, `CellCulture.source_lines`, `CellLine.parent_cell_line`) remain generic links, move into a shared object catalog, become relationship tables, or use another HDMF/NWB pattern?
3. Should `CellCultureSubject.culture` remain a contained child group under `NWBFile.subject`, or should culture objects live in a shared container with subject pointing to the recorded culture?
4. Should recommended terms remain documentation-level guidance, or should selected fields become formal enum-like constraints?
5. Should any of the extension-owned types be proposed directly for NWB core instead of remaining NDX types?
6. Is `CultureProtocol` appropriately modeled as extension metadata, given that the existing `NWBFile.protocol` field is not structured enough for organoid/culture protocol review?

## Explicit Core Reuse

The extension intentionally reuses:

- core `NWB.Subject`, extended by `CellCultureSubject`;
- core `LabMetaData`, extended by `CultureExperimentContext`;
- core `Device` / `DeviceModel` for hardware identity under `/general/devices`;
- core acquisition/electrode/imaging/stimulus structures for detailed recorded data and stimulus waveforms.

## Explicitly Out Of Scope

Do not reintroduce these without a new design decision:

- `ExternalAsset`;
- extension-specific publication registry;
- extension-specific hardware/device object;
- `culture_type=batch`;
- standalone batch objects;
- `CellLine.age_or_passage`;
- `CellLine.age_reference`;
- `CellLine.sex`;
- `CellCulture.sex`;
- `ExperimentContext.recording_preparation`;
- `ExperimentContext.hardware_platform_details`;
- `ExperimentContext.chip_id`;
- `GeneticVariant.clone_id`;
- `GeneticVariant.clonal_status`;
- `CultureProtocol.culture_subtype`;
- `viral_infection` as a `vector_type`.
