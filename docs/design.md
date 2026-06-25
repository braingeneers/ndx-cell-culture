# Design Notes

The extension is based on the v0.74 organoid/cultured neural preparation proposal workbook and formal notes. The workbook remains a human review artifact; this repository contains only formal extension artifacts.

## Object Hierarchy

```text
NWBFile
+-- subject : CellCultureSubject <extends NWB.Subject>
|   +-- inherited NWB.Subject fields
|   +-- culture : CellCulture [1]
|       +-- source_lines : CellLine [0..N]
|       |   +-- parent_cell_line : CellLine [0..1]
|       |   +-- GeneticVariant [0..N]
|       |   +-- ConstructApplication [0..N]
|       +-- parent_cultures : CellCulture [0..N]
|       +-- GeneticVariant [0..N]
|       +-- ConstructApplication [0..N]
|       +-- CultureProtocol [0..1]
+-- general/devices : NWB.Device / NWB.DeviceModel [core NWB]
+-- lab_meta_data : CultureExperimentContext <extends LabMetaData>
    +-- ExperimentContext [0..1]
    +-- Pharmacology [0..N]
```

## Core Reuse

`CellCultureSubject` extends `NWB.Subject` and does not redefine inherited subject fields. The only extension-owned relationship added to the subject is `culture : CellCulture [1]`.

Recording hardware identity uses core NWB `Device` and `DeviceModel` objects under `/general/devices`. The extension does not define a custom hardware object.

## Relationship Fields

The review workbook used helper columns such as `source_line_ids`, `parent_culture_ids`, and `core_device_names`. In this formal extension those become NWB links or object-reference datasets, not semicolon-separated string fields.

The first draft uses two relationship idioms:

- Required runtime links from `ExperimentContext` to `CellCultureSubject`, `CellCulture`, and core NWB `Device`, and from `Pharmacology` to `ExperimentContext`.
- Optional object-reference datasets for recursive or multi-parent provenance fields such as `CellCulture.source_lines`, `CellCulture.parent_cultures`, `CellLine.parent_cell_line`, and attachment targets on `GeneticVariant` / `ConstructApplication`.

The recursive provenance fields are intentionally explicit in the schema, but their final storage idiom should be reviewed with NWB maintainers. The key requirement is that these relationships remain formal NWB object references/links, not workbook-style semicolon-delimited strings.

## Intentionally Absent

The following concepts are intentionally not present:

- `ExternalAsset`
- extension-specific publication registry
- extension-specific hardware object
- `culture_type=batch`
- standalone batch objects
- `CellLine.age_or_passage`
- `CellLine.age_reference`
- `CellLine.sex`
- `CellCulture.sex`
- `ExperimentContext.recording_preparation`
- `ExperimentContext.hardware_platform_details`
- `ExperimentContext.chip_id`
- `GeneticVariant.clone_id`
- `GeneticVariant.clonal_status`
- `CultureProtocol.culture_subtype`
