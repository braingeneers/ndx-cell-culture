ndx-cell-culture
================

``ndx-cell-culture`` is a Neurodata Without Borders (NWB) extension for
describing cultured neural preparations in NWB files. It is intended for labs
working with organoids, assembloids, directoids/connectoids, slices, explants,
spheroids, dissociated cultures, engineered cell lines, construct applications,
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
   +-- lab metadata : CultureExperimentContext <extends LabMetaData>
       +-- ExperimentContext [0..1]
       |   +-- subject -> CellCultureSubject
       |   +-- culture -> CellCulture
       |   +-- device -> NWB.Device [0..1]
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
     subgraph Biology["Biology"]
       Subject["Subject"]
       Culture["Culture"]
       Line["Source line"]
       BioExt["Genetic variants<br/>Constructs<br/>Protocol"]

       Subject --> Culture
       Culture -.-> Line
       Culture --> BioExt
     end

     subgraph Core["Core NWB"]
       Device["Device<br/>DeviceModel"]
       Data["Recorded data<br/>Standard metadata"]
     end

     subgraph Session["Session"]
       Context["Context"]
       Experiment["Experiment"]
       Pharm["Pharmacology"]

       Context --> Experiment
       Context --> Pharm
     end

     Biology -.-> Session
     Device -.-> Session

Use this mental model:

* Put biological identity and provenance in ``CellCultureSubject``.
* Put recorded data and hardware in core NWB.
* Put recording conditions and pharmacology in ``CultureExperimentContext``.
* Dotted arrows show references: ``CellCulture.source_lines``, plus
  recording-context links back to the recorded ``CellCulture`` and
  ``NWB.Device``.
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
