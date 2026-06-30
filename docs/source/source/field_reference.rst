Field Reference
===============

This page summarizes the user-facing fields in ``ndx-cell-culture``. The
authoritative machine-readable schema lives in
``spec/ndx-cell-culture.extensions.yaml``.

Requirement terms:

* Required: constructor/schema required in the current draft.
* Optional: omitted values are allowed.
* Recommended terms: documented vocabulary guidance, not hard enum validation
  in the current draft. Use ``ndx_cell_culture.validate_recommended_terms`` for
  opt-in checking.

CellCultureSubject
------------------

``CellCultureSubject`` extends core ``NWB.Subject``.

Inherited fields from ``NWB.Subject`` are not redefined by this extension:
``subject_id``, ``species``, ``sex``, ``description``, ``age``,
``age__reference``, ``date_of_birth``, ``genotype``, ``strain``, and
``weight``. Culture age should not be stored in ``NWB.Subject.age``.

Extension-owned fields:

.. list-table::
   :header-rows: 1
   :widths: 24 18 24 34

   * - Field
     - Requirement
     - Type
     - Guidance
   * - ``culture``
     - Required
     - link to ``CellCulture``
     - Recorded or described cultured neural preparation stored under this
       subject.
   * - ``CellLine`` children
     - Optional/repeated
     - child groups
     - Source-line objects needed to interpret the subject culture provenance.
   * - ``CellCulture`` children
     - Optional/repeated
     - child groups
     - Recorded, related, or parent cultures needed to interpret the subject
       culture provenance. The public ``related_cultures`` constructor alias
       can be used for parent/input cultures.

CellCulture
-----------

.. list-table::
   :header-rows: 1
   :widths: 26 18 24 32

   * - Field
     - Requirement
     - Type
     - Guidance
   * - ``culture_id``
     - Required
     - text attribute
     - Stable culture identifier.
   * - ``culture_type``
     - Required
     - text attribute
     - Recommended terms: ``dissociated_culture``, ``spheroid``, ``organoid``,
       ``assembloid``, ``slice``, ``explant``, ``other``; ``batch`` is
       prohibited.
   * - ``sample_label``
     - Required
     - text attribute
     - Human-readable label.
   * - ``species``
     - Required
     - text attribute
     - Culture-level convenience/search value; may mirror subject species.
   * - ``culture_subtype``
     - Optional
     - text attribute
     - Regional/subtype identity such as ``cortical``, ``thalamic``,
       ``midbrain``, ``hippocampal``, ``retinal``, ``spinal``,
       ``assembloid``, ``tumor_organoid``, ``other``.
   * - ``batch_label``
     - Optional
     - text attribute
     - Lightweight grouping/search label only; not a batch object.
   * - ``age``
     - Optional
     - text attribute
     - Prefer ISO-8601 duration such as ``P120D``; pilot lab labels such as
       ``day45`` are allowed.
   * - ``age_reference``
     - Optional
     - text attribute
     - Recommended reference event for ``age``.
   * - ``disease_or_diagnosis``
     - Optional
     - text attribute
     - Disease background or diagnosis.
   * - ``reference_genome``
     - Optional
     - text attribute
     - Assembly/annotation context; not a substitute for
       ``Subject.genotype``.
   * - ``notes``
     - Optional
     - text attribute
     - Free-text remarks.
   * - ``source_lines``
     - Optional/repeated
     - object references to ``CellLine``
     - Source line or lines used to create this culture. Pass a list of
       ``CellLine`` objects; read back as an object-reference vector.
   * - ``parent_cultures``
     - Optional/repeated
     - object references to ``CellCulture``
     - Parent or input cultures used to derive this culture. Use for slices,
       directoids/connectoids, assembloids, and other culture-derived
       preparations.
   * - ``GeneticVariant`` children
     - Optional/repeated
     - child groups
     - Culture-attached genetic variants.
   * - ``ConstructApplication`` children
     - Optional/repeated
     - child groups
     - Culture-attached construct applications.
   * - ``CultureProtocol`` child
     - Optional
     - child group
     - Structured derivation/preparation protocol.

CellLine
--------

.. list-table::
   :header-rows: 1
   :widths: 26 18 24 32

   * - Field
     - Requirement
     - Type
     - Guidance
   * - ``cell_line_id``
     - Required
     - text attribute
     - Stable cell-line identifier.
   * - ``cell_line_type``
     - Required
     - text attribute
     - Recommended terms: ``donor``, ``parental_cell_line``,
       ``derived_cell_line``, ``immortalized_line``, ``other``.
   * - ``sample_label``
     - Required
     - text attribute
     - Human-readable label.
   * - ``species``
     - Required
     - text attribute
     - Formal binomial preferred.
   * - ``cell_source_type``
     - Required
     - text attribute
     - Recommended terms: ``iPSC``, ``ESC``, ``primary_tissue``,
       ``primary_cells``, ``tumor_line``, ``immortalized_line``, ``other``.
   * - ``cell_line_name``
     - Optional
     - text attribute
     - Canonical/common line name.
   * - ``cell_line_rrid``
     - Optional
     - text attribute
     - RRID when available.
   * - ``clone_id``
     - Optional
     - text attribute
     - Clone identifier for a clonal derived line.
   * - ``clonal_status``
     - Optional
     - text attribute
     - Recommended terms: ``clonal``, ``polyclonal``, ``mixed``,
       ``unknown``.
   * - ``passage_number``
     - Optional
     - text attribute
     - Passaging information; do not use culture-age fields on ``CellLine``.
   * - ``disease_or_diagnosis``
     - Optional
     - text attribute
     - Disease background or diagnosis.
   * - ``reference_genome``
     - Optional
     - text attribute
     - Assembly/annotation context such as ``GRCh38``.
   * - ``notes``
     - Optional
     - text attribute
     - Free-text remarks.
   * - ``parent_cell_line``
     - Optional
     - object reference to ``CellLine``
     - Parent or source line for a derived line. Pass a ``CellLine`` object;
       read back as a one-element object-reference vector.

Provenance
----------

Provenance is represented directly on subject-contained biological objects:

* use ``CellLine.parent_cell_line`` for cell-line derivation;
* use ``CellCulture.source_lines`` for source lines used to create a culture;
* use ``CellCulture.parent_cultures`` for parent/input cultures used to derive
  another culture.

These fields are stored as NWB object-reference datasets so referenced
``CellLine`` and ``CellCulture`` objects are not duplicated.

GeneticVariant
--------------

Required fields are ``variant_id``, ``target_symbol``, ``edit_type``, and
``method``. Optional fields include ``target_coordinates``,
``edit_description``, ``delivery_method``, ``zygosity_or_edit_state``,
``validation_status``, ``validation_method``, ``notes``, and
``related_application``.

Use ``GeneticVariant`` for stable or defining engineered genomic changes, not
as a complete raw sequencing variant table.

ConstructApplication
--------------------

Required fields are ``application_id``, ``vector_type``, and ``payload``.
Optional fields include ``source``, ``delivery_route``,
``delivery_mechanism``, ``promoter``, ``genomic_persistence_state``,
``application_time_relative_to_recording``, ``age_modified``,
``age_modified_reference``, ``expression_status``, ``validation_method``, and
``notes``.

Attach the construct application at the level where it occurred: line-level
engineering on ``CellLine`` and culture-level transduction, transfection,
injection, or perturbation on ``CellCulture``.

CultureProtocol
---------------

Required field: ``protocol_id``. Optional fields: ``protocol_name``,
``protocol_uri``, ``protocol_doi``, ``protocol_version``,
``patterning_summary``, ``media_summary``, and ``notes``.

CultureExperimentContext
------------------------

``CultureExperimentContext`` extends core ``LabMetaData``. Its recommended
group name is ``culture_experiment_context``. It contains one optional
``ExperimentContext`` and repeated ``Pharmacology`` children. Biological
``CellLine`` and ``CellCulture`` objects belong under ``CellCultureSubject``.

ExperimentContext
-----------------

Required fields are ``experiment_id``, ``age_at_recording``,
``recording_platform``, ``subject``, and ``culture``. Optional fields include
``session_id``, ``age_reference``, ``media_or_bath``, ``temperature_c``,
``recording_duration_s``, ``spontaneous_activity``,
``electrical_stimulation``, ``optical_stimulation``,
``pharmacology_present``, ``experimental_setup``, ``notes``, and ``device``.

Use ``device`` to link to a core NWB ``Device``. Detailed acquisition,
electrode, stimulus, imaging, and processing data should use core NWB
structures.

Pharmacology
------------

Required fields are ``pharmacology_id``, ``agent``, and ``experiment``.
Optional fields are ``concentration``, ``concentration_unit``, ``start_time_s``,
``end_time_s``, ``purpose``, and ``notes``.

``concentration`` is a searchable summary and may be a flexible text value or
range when that is useful for dataset discovery.
