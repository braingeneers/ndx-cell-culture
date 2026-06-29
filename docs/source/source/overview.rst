Overview
========

``ndx-cell-culture`` is an NWB extension for cultured neural preparations such
as organoids, assembloids, directoids/connectoids, slices, explants, spheroids,
dissociated cultures, engineered cell lines, construct applications, recording
context, and pharmacology.

The extension keeps core NWB objects responsible for the file, subject base
fields, devices, electrodes, acquisition, stimulus, imaging, and processing
data. Extension-owned metadata describes the cultured biological preparation
and its provenance.

When To Use This Extension
--------------------------

Use ``ndx-cell-culture`` when the recorded or described preparation is a
cultured biological system and the metadata needed to interpret the data spans
cell-line provenance, culture derivation, engineered variants, construct
applications, culture protocol metadata, recording context, or pharmacology.

The extension is not a replacement for core NWB time-series or modality
metadata. Recording traces, electrical stimuli, imaging data, electrodes, and
processing results should still use the appropriate core NWB structures.

High-Level Model
----------------

``CellCultureSubject`` extends core ``NWB.Subject`` and links to the recorded
or described ``CellCulture`` catalog entry. ``CultureExperimentContext`` extends
``LabMetaData`` and stores reusable cell-line and culture catalogs, provenance
relationships, experiment context, and pharmacology records.

Recommended vocabulary terms are represented as text in the schema, with
opt-in validation available through
``ndx_cell_culture.validate_recommended_terms``.

The generated format specification in these docs is built directly from the
YAML schema in the repository ``spec/`` directory.

Primary Documentation Paths
---------------------------

Start with :doc:`usage` to install the package and create a small file. Use
:doc:`modeling_guide` for guidance about where metadata belongs, then use
:doc:`field_reference` and :doc:`format` when you need field-level details.
