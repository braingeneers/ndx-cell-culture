Release Notes
=============

1.0rc2
------

* Simplifies provenance entry by replacing explicit relation object types with
  direct ``parent_cell_line``, ``source_lines``, and ``parent_cultures``
  reference fields.
* Keeps biological identity and provenance under ``CellCultureSubject`` instead
  of ``CultureExperimentContext``. ``CultureExperimentContext`` is limited to
  recording/session context and pharmacology metadata.

1.0rc1
------

Initial release candidate for NWB maintainer, stakeholder, and external lab
review. This release candidate includes the core schema, PyNWB package,
synthetic examples, public documentation, and validation helpers intended for
review before the first stable ``1.0.0`` release.
