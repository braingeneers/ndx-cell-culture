Release Notes
=============

1.0rc3
------

.. warning::

   This release changes the recording-context schema. Files using the older
   ``CultureExperimentContext`` layout are not supported by the current schema.
   Reading them with RC3 can omit their recording
   context from ``NWBFile.lab_meta_data``; exporting the resulting object can
   lose that metadata, including pharmacology records.

   Read existing files with the extension version used to create them until
   they can be regenerated from source metadata or explicitly migrated while
   preserving recording context and pharmacology. Changing only the embedded
   namespace version does not migrate a file. The parent-vector compatibility
   described below applies to files without the changed recording-context or
   variant fields.

* Limits ``CellLine.parent_cell_line`` to one immediate parent when present,
  with schema, constructor, and write-time validation.
* Reads singleton parent vectors from earlier release candidates and
  normalizes empty parent vectors to an absent parent. Multiple-parent line
  records require correction before they can be read with this package.
* Keeps multiple source lines and parent cultures available on ``CellCulture``.
* Accepts single objects for culture provenance references as well as lists.
* Recording context is a ``LabMetaData`` object stored directly under the NWB
  file and owns optional pharmacology records.
* The Python API resolves the subject, recorded culture, and session ID from
  the enclosing file, and resolves each intervention's containing experiment.
* Genetic variants require an explicit, non-empty preparation-oriented origin.
* Subject construction collects referenced biological provenance and reports
  ambiguous ownership or conflicting object names.
* Schema guidance and examples make DANDI's inherited core subject requirements
  explicit, with donor/source age separate from culture timing. Release checks
  use the DANDI Inspector profile without suppressing subject-age findings.
