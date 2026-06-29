Architecture Decisions
======================

This page records the main design decisions for ``ndx-cell-culture``. It is
written for users and reviewers who want to understand why the extension is
modeled this way.

Semantic Child Objects
----------------------

Repeated metadata such as ``GeneticVariant``, ``ConstructApplication``, and
``Pharmacology`` are semantic child objects rather than ``DynamicTable`` rows.

Rationale:

* These records are usually modest in number for cultured-preparation
  experiments.
* Each record has a clear biological or experimental meaning.
* Semantic objects are easier for labs to instantiate, read, and review than
  tables with row-region bookkeeping.
* The extension is intended to provide consistent metadata structure, not
  high-volume analysis tables.

Shared Catalogs And Relationship Records
----------------------------------------

``CultureExperimentContext`` stores reusable ``CellLine`` and ``CellCulture``
catalog entries. Provenance is represented with explicit relationship records:

* ``CellLineParentRelation``
* ``CellCultureSourceLineRelation``
* ``CellCultureParentRelation``

Rationale:

* A single source line can be reused across many cultures.
* A culture can have multiple source lines.
* A culture can have multiple parent cultures, which is important for
  assembloids, directoids/connectoids, co-cultures, slices, and related
  preparations.
* Relationship objects make many-to-many provenance explicit without nesting
  duplicated parent objects under every child object.

Subject Links To A Cataloged Culture
------------------------------------

``CellCultureSubject.culture`` is a required link to a ``CellCulture`` catalog
entry, not a contained child group.

Rationale:

* ``NWBFile.subject`` remains the file-level subject entry point.
* Culture metadata can be shared and cross-referenced by
  ``ExperimentContext`` and relationship records.
* The model avoids duplicating culture metadata when several recording
  contexts or provenance records refer to the same culture.

Recommended Terms
-----------------

Recommended vocabulary values are documentation-level guidance and opt-in
validation checks, not hard enum constraints in the NWB schema.

Rationale:

* NWB commonly uses text fields with recommended terms where community
  vocabulary is still evolving.
* Cultured neural preparation terminology is active and varied across labs.
* ``ndx_cell_culture.validate_recommended_terms`` gives labs a practical
  pre-submission check without making files unreadable when a new term is
  needed.

NDX First
---------

The extension-owned types remain NDX types rather than being proposed directly
as NWB core types.

Rationale:

* The model needs real-world use and maintainer review before mainline NWB
  inclusion.
* Keeping this as an NDX allows iteration while giving labs a stable package
  to test.
* If adoption is broad, selected pieces can later be proposed for NWB core
  with usage evidence.

Structured Culture Protocols
----------------------------

``CultureProtocol`` remains extension metadata even though core
``NWBFile.protocol`` exists.

Rationale:

* ``NWBFile.protocol`` is not structured enough for culture-protocol review.
* Cultured neural preparations need searchable fields such as protocol
  identifier, version, URI/DOI, patterning summary, and media summary.
* Full protocol documents should still live outside the file and be referenced
  through URI or DOI.

Core NWB Reuse
--------------

The extension intentionally reuses core NWB for:

* inherited subject fields through ``NWB.Subject``;
* hardware identity through ``NWB.Device`` and ``NWB.DeviceModel``;
* acquisition, stimulus, imaging, electrode, processing, and time-series data
  through standard NWB structures.

The extension does not define an external asset registry, publication
registry, custom hardware object, or batch object.
