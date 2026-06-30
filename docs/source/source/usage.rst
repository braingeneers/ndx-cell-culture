Installation and Quickstart
===========================

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
3. Store catalogs in ``CultureExperimentContext`` and use direct provenance
   fields such as ``source_lines`` and ``parent_cultures``.
4. Use core NWB ``Device`` / ``DeviceModel`` for hardware identity.
5. Use ``ExperimentContext`` and ``Pharmacology`` for recording-session context.

The public Python API uses ``pharmacologies`` for repeated ``Pharmacology``
records, including constructor input and
``get_pharmacologies`` / ``add_pharmacologies`` / ``create_pharmacologies``
methods.

Minimal Example
---------------

This example creates a synthetic cortical organoid recording with one source
line, one culture, direct source-line provenance, core NWB device metadata, and
one recording context.

.. code-block:: python

   from datetime import datetime

   from dateutil.tz import tzlocal
   from pynwb import NWBHDF5IO, NWBFile

   from ndx_cell_culture import (
       CellCulture,
       CellCultureSubject,
       CellLine,
       CultureExperimentContext,
       CultureProtocol,
       ExperimentContext,
   )

   line = CellLine(
       name="CL-SYN-001",
       cell_line_id="CL-SYN-001",
       cell_line_type="parental_cell_line",
       sample_label="Synthetic iPSC line",
       species="Homo sapiens",
       cell_source_type="iPSC",
       passage_number="p35",
   )

   protocol = CultureProtocol(
       name="PROTO-SYN-CORTICAL-001",
       protocol_id="PROTO-SYN-CORTICAL-001",
       protocol_name="Synthetic cortical organoid protocol",
       patterning_summary="forebrain patterning",
       media_summary="neural induction and maturation media",
   )

   culture = CellCulture(
       name="CULT-SYN-ORG-001",
       culture_id="CULT-SYN-ORG-001",
       culture_type="organoid",
       sample_label="Synthetic cortical organoid",
       species="Homo sapiens",
       culture_subtype="cortical",
       age="P120D",
       age_reference="days_post_induction",
       culture_protocol=protocol,
       source_lines=[line],
   )

   subject = CellCultureSubject(
       subject_id="SUBJ-SYN-ORG-001",
       species="Homo sapiens",
       sex="U",
       description="Synthetic cortical organoid recording",
       culture=culture,
   )

   nwbfile = NWBFile(
       session_description="synthetic organoid recording",
       identifier="NWB-SYN-ORG-001",
       session_start_time=datetime(2026, 1, 1, tzinfo=tzlocal()),
   )
   nwbfile.subject = subject

   device = nwbfile.create_device(name="Example MEA device")

   experiment = ExperimentContext(
       name="EXP-SYN-ORG-001",
       experiment_id="EXP-SYN-ORG-001",
       subject=subject,
       culture=culture,
       age_at_recording="P120D",
       age_reference="days_post_induction",
       recording_platform="MEA",
       recording_duration_s=1800.0,
       spontaneous_activity=True,
       pharmacology_present=False,
       device=device,
   )

   nwbfile.add_lab_meta_data(
       CultureExperimentContext(
           name="culture_experiment_context",
           cell_lines=[line],
           cell_cultures=[culture],
           experiment_context=experiment,
       )
   )

   with NWBHDF5IO("synthetic_organoid.nwb", "w") as io:
       io.write(nwbfile)

Validation
----------

Validate NWB files by reading them back with PyNWB and running NWB Inspector in
an environment where ``ndx-cell-culture`` is installed:

.. code-block:: bash

   python - <<'PY'
   from pynwb import NWBHDF5IO

   with NWBHDF5IO("synthetic_organoid.nwb", "r") as io:
       io.read()
   PY

   nwbinspector synthetic_organoid.nwb --modules ndx_cell_culture --threshold BEST_PRACTICE_VIOLATION

If NWB Inspector reports that ``CellCultureSubject`` is missing ``age`` and
``date_of_birth``, do not put culture age in ``NWB.Subject.age``. Use
``CellCulture.age`` and ``ExperimentContext.age_at_recording`` for culture
timing.

Run the opt-in recommended-term validator for vocabulary guidance:

.. code-block:: python

   import ndx_cell_culture as ndx

   issues = ndx.validate_recommended_terms(nwbfile)
   for issue in issues:
       print(issue.message)

Examples
--------

Additional synthetic examples are available under ``examples/``:

.. code-block:: bash

   python examples/create_basic_organoid_nwb.py
   python examples/create_synthetic_scenarios.py
