User Guide
==========

Installation
------------

Install the package from the repository during release-candidate review:

.. code-block:: bash

   python -m pip install git+https://github.com/braingeneers/ndx-cell-culture.git

For local development:

.. code-block:: bash

   git clone git@github.com:braingeneers/ndx-cell-culture.git
   cd ndx-cell-culture
   python -m pip install -e ".[dev]"

Core Usage Pattern
------------------

1. Create reusable ``CellLine`` and ``CellCulture`` objects.
2. Link the recorded preparation through ``CellCultureSubject.culture``.
3. Store catalogs and provenance relations in ``CultureExperimentContext``.
4. Use core NWB ``Device`` / ``DeviceModel`` for hardware identity.
5. Use ``ExperimentContext`` and ``Pharmacology`` for recording-session context.

The public Python API accepts the natural plural spelling ``pharmacologies``
for repeated ``Pharmacology`` records, including constructor input and
``get_pharmacologies`` / ``add_pharmacologies`` / ``create_pharmacologies``
methods.

Validation
----------

Validate NWB files with both PyNWB and NWB Inspector before sharing:

.. code-block:: bash

   pytest -q
   nwbinspector examples/basic_organoid_example.nwb --modules ndx_cell_culture --threshold BEST_PRACTICE_VIOLATION

Run the opt-in recommended-term validator for vocabulary guidance:

.. code-block:: python

   import ndx_cell_culture as ndx

   issues = ndx.validate_recommended_terms(nwbfile)
   for issue in issues:
       print(issue.message)

Examples
--------

The repository includes synthetic examples under ``examples/``:

.. code-block:: bash

   python examples/create_basic_organoid_nwb.py
   python examples/create_synthetic_scenarios.py
