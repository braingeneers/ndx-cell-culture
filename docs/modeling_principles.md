# Modeling Principles

This page describes the current `ndx-cell-culture` metadata model. It is a usage guide for how the extension represents cell-culture metadata in NWB.

## Semantic Child Objects

Repeated metadata such as `GeneticVariant`, `ConstructApplication`, and `Pharmacology` are represented as semantic child objects. Use these objects for records with clear biological or experimental meaning.

Use core NWB tables and time series for high-volume acquisition, stimulus, electrode, imaging, processing, and analysis data.

## Shared Catalogs And Relationship Records

`CultureExperimentContext` stores reusable `CellLine` and `CellCulture` catalog entries for the NWB file. Provenance is represented with explicit relationship records:

- `CellLineParentRelation`
- `CellCultureSourceLineRelation`
- `CellCultureParentRelation`

Repeat relation objects when a culture has multiple source lines or multiple parent cultures. This is the expected pattern for assembloids, directoids/connectoids, co-cultures, slices, and related preparations.

## Subject Links To A Cataloged Culture

`CellCultureSubject.culture` is a required link to a `CellCulture` catalog entry. `NWBFile.subject` remains the file-level subject entry point, while the detailed cultured-preparation metadata lives in the shared `CultureExperimentContext` catalog.

## Recommended Terms

Recommended vocabulary values are stored as text in the NWB schema. Use `ndx_cell_culture.validate_recommended_terms` when you want advisory checking before sharing or depositing files.

## Structured Culture Protocols

Use `CultureProtocol` for structured culture-protocol metadata such as a protocol identifier, version, URI/DOI, patterning summary, and media summary. Use `protocol_uri` or `protocol_doi` to point to a full protocol document when one is available.

## Core NWB Reuse

The extension uses core NWB for:

- inherited subject fields through `NWB.Subject`;
- hardware identity through `NWB.Device` and `NWB.DeviceModel`;
- acquisition, stimulus, imaging, electrode, processing, and time-series data through standard NWB structures.

The extension does not define an external asset registry, publication registry, custom hardware object, or batch object.
