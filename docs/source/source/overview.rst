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
