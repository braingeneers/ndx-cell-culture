Release Notes
=============

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
