ndx-cell-culture
================

``ndx-cell-culture`` is a Neurodata Without Borders (NWB) extension for
describing cultured neural preparations in NWB files. It is intended for labs
working with organoids, assembloids, directoids/connectoids, slices, explants,
spheroids, dissociated cultures, cell lines, defining genetic variants, construct applications,
recording context, and pharmacology.

Use this extension when the biological preparation is a cultured neural system
rather than an animal subject, and when the metadata needed to interpret the
recording cannot be represented clearly with core ``NWB.Subject`` alone.

NWB placement at a glance
-------------------------

The extension keeps core NWB responsible for devices, acquisition, stimulus,
imaging, processing, and other modality-specific data. Cultured-preparation
identity and provenance are attached through the subject; recording context and
pharmacology live in lab metadata.

.. code-block:: text

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
   +-- lab metadata : ExperimentContext <extends LabMetaData>
       +-- device -> NWB.Device [0..1]
       +-- Pharmacology [0..N]

The core mental model is to keep biological preparation metadata, core NWB data
and hardware, and recording context distinct but linked:

.. mermaid::

   %%{init: {
     "theme": "base",
     "themeVariables": {
       "fontFamily": "Arial, sans-serif",
       "fontSize": "14px",
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
       Subject["CellCultureSubject<br/>extends NWB.Subject"]
       Culture["CellCulture<br/>recorded, related,<br/>or parent cultures"]
       Line["CellLine<br/>source line lineage"]
       BioExt["GeneticVariant<br/>ConstructApplication<br/>CultureProtocol"]

       Subject -->|"culture"| Culture
       Culture -.->|"source_lines"| Line
       Culture --> BioExt
     end

     subgraph Core["Core NWB"]
       Device["NWB.Device<br/>NWB.DeviceModel"]
       Data["NWBFile<br/>recorded data and<br/>standard metadata"]
     end

     subgraph Session["Recording context"]
       Context["ExperimentContext<br/>extends LabMetaData"]
       Pharm["Pharmacology"]

       Context --> Pharm
     end

     Data -->|"subject"| Subject
     Data -->|"lab_meta_data"| Context
     Context -.->|"device"| Device

Use this mental model:

* Put biological identity and provenance in ``CellCultureSubject``.
* Put recorded data and hardware in core NWB.
* Put recording conditions and pharmacology in ``ExperimentContext``.
* Dotted arrows show stored references: ``CellCulture.source_lines`` and
  ``ExperimentContext.device``. Subject, culture, and session ID are resolved
  from the enclosing NWB file by the Python API.
* The diagram uses short labels for readability; the ASCII hierarchy above
  gives the exact NWB and extension object names.

.. toctree::
    :numbered:
    :maxdepth: 2
    :caption: User Guide

    overview
    usage
    modeling_guide
    examples
    field_reference
    validation_dandi
    api_reference

.. toctree::
    :numbered:
    :maxdepth: 3
    :caption: Generated Reference

    format

.. toctree::
    :maxdepth: 2
    :caption: Release & Legal

    release_notes
    credits

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
