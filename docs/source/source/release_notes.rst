Release Notes
=============

1.0rc4
------

* Recording context is a ``LabMetaData`` object stored directly under the NWB
  file and owns optional pharmacology records.
* The Python API resolves the subject, recorded culture, and session ID from
  the enclosing file, and resolves each intervention's containing experiment.
* Genetic variants require an explicit, non-empty preparation-oriented origin.
* Subject construction collects referenced biological provenance and reports
  ambiguous ownership or conflicting object names.
