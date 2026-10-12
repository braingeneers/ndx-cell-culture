Release Notes
=============

1.0rc4
------

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
