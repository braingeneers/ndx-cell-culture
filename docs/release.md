# Release Checklist

Use this checklist when preparing a versioned `ndx-cell-culture` release.

## Local Validation

- Install development dependencies with `python -m pip install -e ".[dev]"`.
- Run `bash scripts/check_release.sh`.
- Confirm the parent-line regression tests cover legacy-file export and reading
  from the cached schema without importing the extension package.
- Review the generated NWB example files enough to confirm:
  - `CellCultureSubject` stores biological identity and provenance;
  - `ExperimentContext` is stored directly in `lab_meta_data` and owns pharmacology;
  - `parent_cell_line`, `source_lines`, and `parent_cultures` references round-trip;
  - recording hardware is represented with core NWB `Device` / `DeviceModel`;
  - NWB Inspector's DANDI profile has no best-practice violations, including
    missing core subject-age/birth-date or sex findings.
- Review public README and ReadTheDocs source for stale internal or planning terms before publishing.

## Versioning

- Update `pyproject.toml` version.
- Update `scripts/create_extension_spec.py` namespace version to match.
- Regenerate and commit `spec/ndx-cell-culture.namespace.yaml` and `spec/ndx-cell-culture.extensions.yaml`.
- Tag the release as `vX.Y.Z`.

## Distribution

- Publish to TestPyPI first for installation testing.
- Publish to PyPI after the TestPyPI package installs and imports cleanly.
- Update `docs/catalog/ndx-meta.yaml.template` with the final PyPI URL and release version.
- Set catalog `maintainers` to a list of GitHub usernames.
- Submit the completed catalog metadata to the NWB staged extensions repository.
- For DANDI-facing datasets, document the exact `ndx-cell-culture` version used to create the NWB files.

## Documentation

- Public documentation lives under `docs/source/source`.
- The Sphinx HTML build output is intentionally untracked at `docs/_build/html`.
- Read the Docs imports this repository using the root `.readthedocs.yaml` file.
- Keep internal release notes here concise; user-facing model, examples, and field reference content belong in the Sphinx docs.

## External Review

Before recommending broad production use, review the extension with NWB maintainers and at least one external cell-culture lab. The schema is designed to be usable before NWB-core inclusion, but maintainer feedback should inform the first stable release.

## RC API Changes (1.0rc3)

The recording-context and provenance changes address issues #2, #3, #4, and
#6. The singleton parent-line constraint addresses #5. DANDI schema guidance,
examples, and unsuppressed subject validation address #1 in this repository.

Earlier RC files using the previous recording-context model are not supported
by the revised schema. Regenerate them from their source metadata with the
current API; do not merely change the embedded namespace version. Parent-line
provenance files without the changed context or variant fields retain the
normalization and export support covered by the parent-line regression tests.
For files created from an untagged development snapshot, keep its original
source commit as well as the embedded version; the version label alone may
identify more than one development schema.
Update callers as follows:

- Replace `CultureExperimentContext(experiment_context=experiment, ...)` with
  `nwbfile.add_lab_meta_data(experiment)`.
- Move `pharmacologies` and its add/create/get methods onto `ExperimentContext`.
- Remove `subject` and `culture` constructor arguments from `ExperimentContext`;
  attach it to the file and use the derived properties when needed.
- Move `ExperimentContext(session_id=...)` to `NWBFile(session_id=...)` or set
  `nwbfile.session_id` before writing. Context notes describe recording conditions;
  file-wide notes belong in `NWBFile.notes`.
- Remove `Pharmacology(experiment=...)`; add the record to the experiment's
  `pharmacologies` collection. Its `experiment` property resolves ownership.
- Supply an explicit non-empty `GeneticVariant.origin`, using `unknown` when
  appropriate. The schema no longer treats the attribute as optional.
- Referenced provenance is collected at subject construction. Explicit
  collections remain useful for additional objects and for choosing application
  ownership. New references added afterward still require explicit storage.

Core subject fields retain NWB optionality because DANDI's age-or-birth-date
requirement is a deposition constraint, not two independently required NWB
datasets. DANDI-facing examples provide documented synthetic donor/source ages,
and release checks no longer exclude subject-age findings. Regression tests
write/read both age-based and birth-date-based subjects and prove that culture
age alone does not satisfy the DANDI subject checks.

The DANDI Inspector profile is not a complete archive acceptance test. Validate
with the intended DANDI client and review extracted asset metadata before
publication, especially the age reference for embryonic sources. Existing
Uploader authoring, publication workers, and already-uploaded RC files require
separate reviewed updates; this repository change does not migrate them.
