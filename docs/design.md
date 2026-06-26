# Data Modeling Guide

`ndx-cell-culture` represents cultured neural preparations as first-class NWB metadata while reusing core NWB objects wherever possible.

The extension is designed for files where the recorded subject is a culture-derived preparation such as an organoid, assembloid, directoid/connectoid, slice, explant, spheroid, or dissociated culture.

## Object Hierarchy

```text
NWBFile
+-- subject : CellCultureSubject <extends NWB.Subject>
|   +-- inherited NWB.Subject fields
|   +-- culture -> CellCulture catalog entry [1]
+-- general/devices : NWB.Device / NWB.DeviceModel [core NWB]
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

## Subject And Culture

`CellCultureSubject` extends core `NWB.Subject`. It does not redefine inherited subject fields such as `subject_id`, `species`, `sex`, `age`, `genotype`, or `description`.

The extension-owned `culture` link identifies the `CellCulture` catalog entry being recorded or described. Culture-specific timing belongs in `CellCulture.age` or `ExperimentContext.age_at_recording`, not in `NWB.Subject.age`.

`CellCulture` describes the preparation itself: type, subtype, culture age, batch label, disease/diagnosis, reference genome, attached variants, construct applications, and culture protocol metadata.

## Catalogs And Provenance

`CultureExperimentContext` is the file-level metadata catalog for cultured preparations. It stores reusable `CellLine` and `CellCulture` objects and explicit relationship records between them.

Use `CellLine` for source-line identity and lineage metadata such as passage, clone, clonal status, source type, line-level variants, or construct applications.

Use relationship records for provenance:

- `CellLineParentRelation` links a child or derived line to a parent line.
- `CellCultureSourceLineRelation` links a culture to one source line. Repeat it when a culture has multiple source lines.
- `CellCultureParentRelation` links a culture to one parent culture. Repeat it for slices, assembloids, directoids/connectoids, and other multi-parent culture derivations.

This catalog model avoids duplicating shared cell lines or parent cultures across several subjects, and it keeps multi-parent provenance explicit.

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

Use `Pharmacology` for compounds applied during a recording session. The intended scale is modest searchable metadata, not a full protocol or time-series pharmacology representation.

## Recommended Terms

Recommended vocabulary terms are stored as text attributes in the schema. Use `ndx_cell_culture.validate_recommended_terms` for opt-in checking before sharing or depositing files.

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
