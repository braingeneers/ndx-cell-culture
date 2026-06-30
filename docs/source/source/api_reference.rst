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
* ``CultureExperimentContext``
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

These fields are stored as NWB object-reference vectors. After reading a file
back, use indexing or slicing to access the referenced objects, for example
``culture.source_lines[:]`` or ``line.parent_cell_line[0]``.

``CellCultureSubject`` automatically stores the linked recorded ``culture`` in
its subject-contained ``cell_cultures`` collection. Use a stable
identifier-style ``CellCulture.name`` such as ``CULT-SYN-001``; the literal
name ``culture`` is reserved for the link name and is rejected by the public
constructor to avoid an HDF5 path conflict.

Pharmacology Records
--------------------

Use ``pharmacologies`` for repeated ``Pharmacology`` records in
``CultureExperimentContext``:

* ``CultureExperimentContext(pharmacologies=[...])``
* ``CultureExperimentContext.pharmacologies``
* ``CultureExperimentContext.add_pharmacologies(...)``
* ``CultureExperimentContext.create_pharmacologies(...)``
* ``CultureExperimentContext.get_pharmacologies(...)``

Recommended-Term Validation
---------------------------

.. autoclass:: ndx_cell_culture.RecommendedTermIssue
   :members:

.. autofunction:: ndx_cell_culture.validate_recommended_terms

``RECOMMENDED_TERMS`` contains the current advisory vocabulary map used by the
validator.
