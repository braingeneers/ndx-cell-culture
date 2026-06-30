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
       direct source-line provenance, line-level variant, culture-level construct
       application, protocol metadata, MEA context, and core ``Device``.
   * - Slice patch clamp
     - ``build_slice_patch_clamp``
     - Organoid-derived slice with ``parent_cultures`` provenance,
       patch-clamp device metadata, AAV construct application, and two
       pharmacology entries.
   * - Edited iPSC organoid
     - ``build_edited_ipsc_organoid_mea``
     - Synthetic edited iPSC lineage using ``parent_cell_line``,
       line-level variant, ``source_lines`` provenance, protocol metadata, MEA
       context, and no pharmacology.
   * - Biological metadata only
     - ``build_biological_metadata_only_organoid``
     - Synthetic organoid with subject-contained culture and line metadata but no
       recording/session context.
   * - Pharmacology titration
     - ``build_pharmacology_titration_organoid``
     - Synthetic organoid recording with a pharmacology concentration range and
       MEA device.
   * - Directoid
     - ``build_directoid``
     - Directoid/connectoid-style ``assembloid`` example with two parent
       organoids represented by ``parent_cultures``.
   * - Two-line assembloid
     - ``build_two_line_assembloid``
     - ``assembloid`` example from two distinct synthetic source lines
       represented by ``source_lines``.

Common Modeling Recipes
-----------------------

Organoid recording
~~~~~~~~~~~~~~~~~~

Create one ``CellCultureSubject`` linked to the recorded ``CellCulture``. Store
the source line under the subject with ``cell_lines=[line]``, set
``CellCulture.source_lines=[line]``, and put searchable recording context in
``ExperimentContext``.

Organoid-derived slice
~~~~~~~~~~~~~~~~~~~~~~

Store both the parent organoid and the slice under ``CellCultureSubject``. Link
the slice to the parent organoid with ``CellCulture.parent_cultures``.

Directoid or connectoid
~~~~~~~~~~~~~~~~~~~~~~~

Represent the final connected preparation as a ``CellCulture`` with
``culture_type`` set to ``assembloid``. Link each input organoid or region with
``CellCulture.parent_cultures``.

Two-line assembloid
~~~~~~~~~~~~~~~~~~~

Represent the final preparation as one ``CellCulture`` and link each input
source line with ``CellCulture.source_lines``. Describe component roles in
``CellCulture.notes`` when the source lines contribute distinct components.

Pharmacology titration
~~~~~~~~~~~~~~~~~~~~~~

Use ``ExperimentContext`` for the recording session and add one or more
``Pharmacology`` records linked to that context. ``concentration`` is a
searchable text value and may contain a range when that is the most useful
summary for discovery.
