# Release Checklist

Use this checklist when preparing a versioned `ndx-cell-culture` release.

## Local Validation

- Install development dependencies with `python -m pip install -e ".[dev]"`.
- Run `bash scripts/check_release.sh`.
- Review the generated NWB example files enough to confirm:
  - `CellCultureSubject` stores biological identity and provenance;
  - `CultureExperimentContext` stores recording/session context and pharmacology;
  - `parent_cell_line`, `source_lines`, and `parent_cultures` references round-trip;
  - recording hardware is represented with core NWB `Device` / `DeviceModel`;
  - NWB Inspector has no best-practice violations except the intentionally ignored core subject-age warning.
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
- Submit the completed catalog metadata to the NWB staged extensions repository.
- For DANDI-facing datasets, document the exact `ndx-cell-culture` version used to create the NWB files.

## Documentation

- Public documentation lives under `docs/source/source`.
- The Sphinx HTML build output is intentionally untracked at `docs/_build/html`.
- Read the Docs imports this repository using the root `.readthedocs.yaml` file.
- Keep internal release notes here concise; user-facing model, examples, and field reference content belong in the Sphinx docs.

## External Review

Before recommending broad production use, review the extension with NWB maintainers and at least one external cell-culture lab. The schema is designed to be usable before NWB-core inclusion, but maintainer feedback should inform the first stable release.
