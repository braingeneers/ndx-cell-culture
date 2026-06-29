Python API Reference
====================

The package loads the ``ndx-cell-culture`` namespace on import and exposes the
schema-generated PyNWB classes from ``ndx_cell_culture``.

Schema-Generated Classes
------------------------

Import these classes directly from ``ndx_cell_culture``:

* ``CellCultureSubject``
* ``CellCulture``
* ``CellLine``
* ``CellLineParentRelation``
* ``CellCultureSourceLineRelation``
* ``CellCultureParentRelation``
* ``GeneticVariant``
* ``ConstructApplication``
* ``CultureProtocol``
* ``CultureExperimentContext``
* ``ExperimentContext``
* ``Pharmacology``

The constructor signatures are generated from the NWB extension schema. The
curated field guidance is in :doc:`field_reference`; the formal generated
schema reference is in :doc:`format`.

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
