Examples And Recipes
====================

These examples show common modeling patterns for cultured neural preparations:
whole-organoid recordings, organoid-derived slices, edited source lines,
directoids/connectoids, assembloids, biological-metadata-only files, and
pharmacology titrations. All identifiers and biological details are synthetic.

Example builder scripts under ``examples/`` generate complete NWB files for
inspection.

Run all scenarios:

.. code-block:: bash

   python examples/create_synthetic_scenarios.py

Generated ``.nwb`` files are written to ``examples/generated_scenarios/``,
which is ignored by git.

Scenario Coverage
-----------------

.. list-table::
   :header-rows: 1
   :widths: 24 32 44

   * - Scenario
     - Builder
     - Purpose
   * - Basic organoid
     - ``build_basic_organoid``
     - Complete synthetic organoid with a subject-to-culture link,
       source-line relation, line-level variant, culture-level construct
       application, protocol metadata, MEA context, and core ``Device``.
   * - Slice patch clamp
     - ``build_slice_patch_clamp``
     - Organoid-derived slice with ``CellCultureParentRelation``,
       patch-clamp device metadata, AAV construct application, and two
       pharmacology entries.
   * - Edited iPSC organoid
     - ``build_edited_ipsc_organoid_mea``
     - Synthetic edited iPSC lineage using ``CellLineParentRelation``,
       line-level variant, source-line relation, protocol metadata, MEA
       context, and no pharmacology.
   * - Biological metadata only
     - ``build_biological_metadata_only_organoid``
     - Synthetic organoid with culture and line catalogs but no
       recording/session context.
   * - Pharmacology titration
     - ``build_pharmacology_titration_organoid``
     - Synthetic organoid recording with a pharmacology concentration range and
       MEA device.
   * - Directoid
     - ``build_directoid``
     - Directoid/connectoid-style ``assembloid`` example with two parent
       organoids represented by repeated ``CellCultureParentRelation`` objects.
   * - Two-line assembloid
     - ``build_two_line_assembloid``
     - ``assembloid`` example from two distinct synthetic source lines
       represented by repeated ``CellCultureSourceLineRelation`` objects.

Common Modeling Recipes
-----------------------

Organoid recording
~~~~~~~~~~~~~~~~~~

Create one ``CellCultureSubject`` linked to the recorded ``CellCulture``. Store
the source line in the ``CellLine`` catalog, add a
``CellCultureSourceLineRelation``, and put searchable recording context in
``ExperimentContext``.

Organoid-derived slice
~~~~~~~~~~~~~~~~~~~~~~

Catalog both the parent organoid and the slice as ``CellCulture`` objects. Link
the slice to the parent organoid with ``CellCultureParentRelation`` using a
relationship such as ``sliced_from``.

Directoid or connectoid
~~~~~~~~~~~~~~~~~~~~~~~

Represent the final connected preparation as a ``CellCulture`` with
``culture_type`` set to ``assembloid``. Link each input organoid or region with
a repeated ``CellCultureParentRelation``.

Two-line assembloid
~~~~~~~~~~~~~~~~~~~

Represent the final preparation as one ``CellCulture`` and link each input
source line with a repeated ``CellCultureSourceLineRelation``. Use relation
``role`` values such as ``component`` when the source lines contribute
distinct components.

Pharmacology titration
~~~~~~~~~~~~~~~~~~~~~~

Use ``ExperimentContext`` for the recording session and add one or more
``Pharmacology`` records linked to that context. ``concentration`` is a
searchable text value and may contain a range when that is the most useful
summary for discovery.
