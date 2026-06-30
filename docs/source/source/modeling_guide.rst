Modeling Guide
==============

``ndx-cell-culture`` represents cultured neural preparations as first-class
NWB metadata while reusing core NWB objects wherever possible. The extension is
designed for files where the recorded subject is a culture-derived preparation
such as an organoid, assembloid, directoid/connectoid, slice, explant,
spheroid, or dissociated culture.

Where Metadata Belongs
----------------------

.. list-table::
   :header-rows: 1
   :widths: 28 28 44

   * - Metadata
     - Use
     - Guidance
   * - File-level subject entry point
     - ``CellCultureSubject``
     - Links ``NWBFile.subject`` to the recorded or described cultured
       preparation.
   * - Normal subject fields
     - inherited ``NWB.Subject`` fields
     - Use core subject fields such as ``subject_id``, ``species``, ``sex``,
       ``genotype``, and ``description`` without redefining them.
   * - Cultured preparation identity
     - ``CellCulture``
     - Describe the preparation type, age, subtype, batch label, disease or
       diagnosis, reference genome, and attached culture-level metadata.
   * - Source-line identity
     - ``CellLine``
     - Describe cell-line provenance, source type, passage, clone, clonal
       status, and line-level metadata.
   * - Line and culture provenance
     - direct reference fields
     - Use ``CellLine.parent_cell_line``, ``CellCulture.source_lines``, and
       ``CellCulture.parent_cultures`` to capture lineage without separate
       provenance rows.
   * - Stable engineered genomic changes
     - ``GeneticVariant``
     - Attach variants to the ``CellLine`` or ``CellCulture`` where the
       defining edit belongs.
   * - Applied constructs and reagents
     - ``ConstructApplication``
     - Attach vectors, RNPs, reporters, optogenetic tools, or similar
       interventions where they were applied.
   * - Culture protocol summary
     - ``CultureProtocol``
     - Store concise structured protocol metadata and link to full protocol
       documents with ``protocol_uri`` or ``protocol_doi`` when available.
   * - Recording hardware
     - core ``NWB.Device`` / ``NWB.DeviceModel``
     - Use core NWB for hardware identity; this extension does not define a
       custom device object.
   * - Recording/session context
     - ``ExperimentContext``
     - Store searchable session-level context such as recording platform,
       culture age at recording, media or bath, temperature, duration, and
       broad stimulation flags.
   * - Compounds during recording
     - ``Pharmacology``
     - Store modest searchable metadata for applied agents linked to the
       recording context.
   * - Acquired data and detailed stimuli
     - core NWB acquisition, stimulus, imaging, electrodes, and processing
     - Use standard NWB structures for time-series data, electrode metadata,
       imaging data, stimulus waveforms, and processing results.

What This Extension Does Not Replace
------------------------------------

``ndx-cell-culture`` does not replace core NWB structures for acquisition,
stimulus, electrode, imaging, processing, or device metadata. It adds the
cultured-preparation context needed to interpret those data.

Subject And Culture
-------------------

``CellCultureSubject`` extends core ``NWB.Subject``. It does not redefine
inherited subject fields such as ``subject_id``, ``species``, ``sex``, ``age``,
``genotype``, or ``description``.

The extension-owned ``culture`` link identifies the subject-contained
``CellCulture`` object being recorded or described. That culture and any source
lines or related parent cultures are stored under ``CellCultureSubject``.
Culture-specific timing belongs in
``CellCulture.age`` or ``ExperimentContext.age_at_recording``, not in
``NWB.Subject.age``.

``CellCulture`` describes the preparation itself: type, subtype, culture age,
batch label, disease or diagnosis, reference genome, attached variants,
construct applications, and culture protocol metadata.

Biological Context And Provenance
---------------------------------

``CellCultureSubject`` stores the biological context needed to interpret the
recorded preparation: source ``CellLine`` objects, the recorded
``CellCulture``, and any related or parent ``CellCulture`` inputs.
``CultureExperimentContext`` is reserved for recording/session context and
pharmacology metadata.

Use ``CellLine`` for source-line identity and lineage metadata such as passage,
clone, clonal status, source type, line-level variants, or construct
applications.

Use direct reference fields for provenance:

* ``CellLine.parent_cell_line`` answers: what line did this line come from?
* ``CellCulture.source_lines`` answers: which source line or lines made this
  culture?
* ``CellCulture.parent_cultures`` answers: which parent culture or cultures
  produced this culture?

This subject-centered model keeps biological identity with the subject while
still allowing multi-parent provenance for slices, assembloids,
directoids/connectoids, and other derived cultures.

Variants And Construct Applications
-----------------------------------

Use ``GeneticVariant`` for stable or defining engineered genomic changes. Do
not use it as a complete raw sequencing variant table.

Use ``ConstructApplication`` for applied constructs, viral vectors, RNPs,
reporters, optogenetic tools, or similar interventions. Attach the application
where it occurred:

* line-level engineering belongs on ``CellLine``;
* culture-level transduction, transfection, injection, or acute perturbation
  belongs on ``CellCulture``;
* detailed recorded stimulus waveforms belong in core NWB stimulus/acquisition
  structures.

Repeated variants, construct applications, and pharmacology records are
semantic child objects. Use them for records with clear biological or
experimental meaning; use core NWB tables and time series for high-volume
acquisition, stimulus, electrode, imaging, processing, and analysis data.

Protocols
---------

Use ``CultureProtocol`` for concise structured protocol metadata that helps
readers interpret the culture. It is not intended to replace a full protocol
document. Use ``protocol_uri`` or ``protocol_doi`` to point to a full protocol
when available.

Recording Context And Devices
-----------------------------

Use ``ExperimentContext`` for session-level searchable context: recording
platform, culture age at recording, media or bath, temperature, duration,
broad stimulation flags, pharmacology flag, and a short setup description.

Use core NWB ``Device`` / ``DeviceModel`` for recording hardware. The
extension does not define a custom hardware object.

Use ``Pharmacology`` for compounds applied during a recording session. The
intended scale is modest searchable metadata, not a full protocol or
time-series pharmacology representation.

Recommended Terms
-----------------

Recommended vocabulary terms are stored as text attributes in the schema. Use
``ndx_cell_culture.validate_recommended_terms`` for opt-in checking before
sharing or depositing files.

Intentionally Absent
--------------------

The following concepts are intentionally not part of the extension:

* extension-specific external asset registry;
* extension-specific publication registry;
* extension-specific hardware object;
* ``culture_type=batch``;
* standalone batch objects;
* ``CellLine.age_or_passage``;
* ``CellLine.age_reference``;
* ``CellLine.sex``;
* ``CellCulture.sex``;
* ``ExperimentContext.recording_preparation``;
* ``ExperimentContext.hardware_platform_details``;
* ``ExperimentContext.chip_id``;
* ``GeneticVariant.clone_id``;
* ``GeneticVariant.clonal_status``;
* ``CultureProtocol.culture_subtype``.
