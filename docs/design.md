# Data Modeling Guide

`ndx-cell-culture` represents cultured neural preparations as first-class NWB metadata while reusing core NWB objects wherever possible.

The extension is designed for files where the recorded subject is a culture-derived preparation such as an organoid, assembloid, directoid/connectoid, slice, explant, spheroid, or dissociated culture.

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

## Subject And Culture

`CellCultureSubject` extends core `NWB.Subject`. It does not redefine inherited subject fields such as `subject_id`, `species`, `sex`, `age`, `genotype`, or `description`.

The extension-owned child `culture : CellCulture` identifies the cultured preparation being recorded or described. Culture-specific timing belongs in `CellCulture.age` or `ExperimentContext.age_at_recording`, not in `NWB.Subject.age`.

`CellCulture` describes the preparation itself. Use it for the culture type, subtype, source lines, parent cultures, culture age, batch label, disease/diagnosis, reference genome, attached variants, construct applications, and culture protocol metadata.

## Provenance

Use `CellLine` for source-line identity and lineage metadata such as passage, clone, clonal status, source type, and line-level variants or construct applications.

Use `CellCulture.source_lines` when a culture is derived from one or more source lines. Use `CellCulture.parent_cultures` when a culture is biologically derived from one or more prior culture preparations, such as an organoid-derived slice or a multi-parent assembloid/directoid.

The recursive and multi-parent relationship fields are represented in the draft schema as formal NWB links. Their final storage idiom should be reviewed with NWB maintainers before release.

## Variants And Construct Applications

Use `GeneticVariant` for stable or defining engineered genomic changes. Do not use it as a complete raw sequencing variant table.

Use `ConstructApplication` for applied constructs, viral vectors, RNPs, reporters, optogenetic tools, or similar interventions. Attach the application where it occurred:

- line-level engineering belongs on `CellLine`;
- culture-level transduction, transfection, injection, or acute perturbation belongs on `CellCulture`;
- detailed recorded stimulus waveforms belong in core NWB stimulus/acquisition structures.

## Protocols

Use `CultureProtocol` for concise structured protocol metadata that helps readers interpret the culture. It is not intended to replace a full protocol document. Use `protocol_uri` or `protocol_doi` to point to a full protocol when available.

## Recording Context And Devices

Use `ExperimentContext` for session-level searchable context: recording platform, culture age at recording, media or bath, temperature, duration, broad stimulation flags, pharmacology flag, and a short setup description.

Use core NWB `Device` / `DeviceModel` for recording hardware. The extension does not define a custom hardware object.

Use `Pharmacology` for compounds applied during a recording session. More detailed time series or stimulus data should use core NWB structures.

## Intentionally Absent

The following concepts are intentionally not part of the extension:

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
