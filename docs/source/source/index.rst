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
metadata is attached through the subject and file-level lab metadata.

.. code-block:: text

   NWBFile
   +-- subject : CellCultureSubject <extends NWB.Subject>
   |   +-- inherited NWB.Subject fields
   |   +-- culture -> CellCulture catalog entry
   +-- general/devices : NWB.Device / NWB.DeviceModel
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
