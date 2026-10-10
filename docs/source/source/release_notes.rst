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

1.0rc2
------

* Represents biological identity and provenance through ``CellCultureSubject``
  with subject-contained ``CellLine`` and ``CellCulture`` objects.
* Uses direct ``parent_cell_line``, ``source_lines``, and ``parent_cultures``
  reference fields for lineage and culture derivation.
* Keeps ``CultureExperimentContext`` focused on recording/session context and
  pharmacology metadata.

1.0rc1
------

Initial release candidate for NWB maintainer, stakeholder, and external lab
review. This release candidate includes the core schema, PyNWB package,
synthetic examples, public documentation, and validation helpers intended for
review before the first stable ``1.0.0`` release.
