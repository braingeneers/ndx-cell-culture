# Release Checklist

Use this checklist when preparing a versioned `ndx-cell-culture` release.

## Before Release

- Regenerate schema with `python src/spec/create_extension_spec.py`.
- Run `pytest -q`.
- Run `python examples/create_basic_organoid_nwb.py`.
- Run `python examples/create_synthetic_scenarios.py`.
- Validate generated NWB files with `pynwb.validate`.
- Run `ndx_cell_culture.validate_recommended_terms` on generated examples and expected release fixtures.
- Confirm subject-to-culture, cell-line parent, culture source-line, and culture parent relationships all round-trip.
- Build wheel and source distribution.
- Install the built wheel in a clean environment and verify `import ndx_cell_culture`.
- Review README and docs for user-facing clarity before publishing.

## Versioning

- Update `pyproject.toml` version.
- Update `src/spec/create_extension_spec.py` namespace version to match.
- Regenerate and commit `spec/ndx-cell-culture.namespace.yaml` and `spec/ndx-cell-culture.extensions.yaml`.
- Tag the release as `vX.Y.Z`.

## Distribution

- Publish to TestPyPI first for installation testing.
- Publish to PyPI after the TestPyPI package installs and imports cleanly.
- For DANDI-facing datasets, document the exact `ndx-cell-culture` version used to create the NWB files.

## External Review

Before recommending broad production use, review the extension with NWB maintainers and at least one external cell-culture lab. The schema is designed to be usable before NWB-core inclusion, but maintainer feedback should inform the first stable release.
