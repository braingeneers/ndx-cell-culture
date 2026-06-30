Overview
========

``ndx-cell-culture`` is an NWB extension for cultured neural preparations such
as organoids, assembloids, directoids/connectoids, slices, explants, spheroids,
dissociated cultures, engineered cell lines, construct applications, recording
context, and pharmacology.

The extension gives labs a consistent way to describe the biological
preparation behind a recording: what was recorded, what it was derived from,
how it was engineered or treated, and what session-level context is needed to
interpret the data.

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

At a high level, an NWB file using this extension contains:

* one recorded or described cultured preparation;
* subject-contained source lines and related cultures needed to interpret that
  preparation;
* explicit provenance links between source lines, parent cultures, and derived
  cultures;
* engineered variants and construct applications attached where they occurred;
* structured culture protocol metadata;
* session-level recording context and optional pharmacology records.

Core NWB remains responsible for the file container, subject base fields,
devices, electrodes, acquisition, stimulus, imaging, processing data, and other
standard neurophysiology structures. ``ndx-cell-culture`` adds the cultured
biological-preparation metadata that those core objects do not describe.

The detailed NWB placement is described in :doc:`modeling_guide`; field-level
details are listed in :doc:`field_reference`.

Vocabulary Guidance
-------------------

Recommended vocabulary terms are represented as text values, following common
NWB practice for evolving community terminology. Use
``ndx_cell_culture.validate_recommended_terms`` when you want advisory checking
before sharing or depositing files.

Primary Documentation Paths
---------------------------

Start with :doc:`usage` to install the package and create a small file. Use
:doc:`modeling_guide` for guidance about where metadata belongs, and
:doc:`examples` for common modeling patterns. Use :doc:`field_reference` and
:doc:`format` when you need field-level or generated schema details.
