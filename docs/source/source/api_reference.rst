Python API Reference
====================

Import the extension classes directly from ``ndx_cell_culture`` after
installing the package. Importing the package also loads the
``ndx-cell-culture`` namespace so PyNWB can read and write files that use the
extension.

Importable Classes
------------------

Import these classes directly from ``ndx_cell_culture``:

* ``CellCultureSubject``
* ``CellCulture``
* ``CellLine``
* ``GeneticVariant``
* ``ConstructApplication``
* ``CultureProtocol``
* ``ExperimentContext``
* ``Pharmacology``

The constructor signatures are generated from the NWB extension schema. The
curated field guidance is in :doc:`field_reference`; the formal generated
schema reference is in :doc:`format`.

Provenance References
---------------------

The public constructors accept normal objects for subject biological context
and provenance fields:

* ``CellCultureSubject(culture=culture, cell_lines=[line])``
* ``CellCultureSubject(culture=slice_culture, related_cultures=[parent_organoid])``
* ``CellLine(parent_cell_line=parent_line)``
* ``CellCulture(source_lines=[line_a, line_b])``
* ``CellCulture(parent_cultures=[parent_organoid])``

The line and culture provenance fields are stored as NWB object-reference
vectors. ``CellLine.parent_cell_line`` has zero or one immediate parent: omit
the argument when the parent is unknown, or pass a single ``CellLine``. A
one-element ``VectorData`` containing a ``CellLine`` is also accepted. Multiple
parents and references to other object types are rejected, including vectors
modified before writing.

After reading a file back, use indexing or slicing to access the referenced
objects, for example ``culture.source_lines[:]`` or
``line.parent_cell_line[0]`` when ``line.parent_cell_line is not None``.
``CellCulture.source_lines`` and ``CellCulture.parent_cultures`` can contain
multiple inputs.

Files from earlier release candidates with no parent dataset or a singleton
parent vector remain readable. Empty parent vectors are normalized to ``None``
and omitted when exporting with ``NWBHDF5IO.export``. Files containing multiple
parents for a ``CellLine`` raise an error identifying the affected line;
resolve the lineage before exporting with the current schema.

``CellCultureSubject`` automatically stores the linked recorded ``culture`` in
its subject-contained ``cell_cultures`` collection. It also collects referenced
source and parent lines, parent cultures, and variant-related applications.
Explicit ``cell_lines`` and ``related_cultures`` arguments remain available to
include additional objects. Use a stable
identifier-style ``CellCulture.name`` such as ``CULT-SYN-001``; the literal
name ``culture`` is reserved for the link name and is rejected by the public
constructor to avoid an HDF5 path conflict.

An unowned application referenced by a variant is attached to the line or
culture containing that variant. Existing application ownership is preserved.
If an unowned application is referenced from multiple biological objects,
attach it explicitly to the appropriate ``construct_applications`` collection
before constructing the subject. Objects already owned by another subject and
distinct objects with conflicting names raise descriptive errors.

Automatic collection happens during subject construction. When adding new
references afterward, explicitly add the targets with ``add_cell_lines``,
``add_related_cultures``, or the appropriate biological object's
``add_construct_applications`` method. Referencing an unstored target can cause
``ReferenceTargetNotBuiltError`` when writing.

Recording Context
-----------------

Store ``ExperimentContext`` directly with
``nwbfile.add_lab_meta_data(experiment)``. Its read-only ``subject``, ``culture``,
and ``session_id`` properties resolve values from the enclosing ``NWBFile``.
Set ``session_id`` on the file. Accessing derived relationships before
attachment, or subject/culture on a file without ``CellCultureSubject``, raises
a descriptive ``ValueError``.

Pharmacology Records
--------------------

Use ``pharmacologies`` for repeated ``Pharmacology`` records in
``ExperimentContext``:

* ``ExperimentContext(pharmacologies=[...], ...)``
* ``ExperimentContext.pharmacologies``
* ``ExperimentContext.add_pharmacologies(...)``
* ``ExperimentContext.create_pharmacologies(...)``
* ``ExperimentContext.get_pharmacologies(...)``

``Pharmacology.experiment`` resolves the containing ``ExperimentContext``;
attach the intervention to that context before accessing the property.

Recommended-Term Validation
---------------------------

.. autoclass:: ndx_cell_culture.RecommendedTermIssue
   :members:

.. autofunction:: ndx_cell_culture.validate_recommended_terms

``RECOMMENDED_TERMS`` contains the current advisory vocabulary map used by the
validator.
