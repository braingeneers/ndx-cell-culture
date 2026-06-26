# Release Checklist

Use this checklist when preparing a versioned `ndx-cell-culture` release.

## Before Release

- Regenerate schema with `python src/spec/create_extension_spec.py`.
- Run `pytest -q`.
- Run `python examples/create_basic_organoid_nwb.py`.
- Run `python examples/create_synthetic_scenarios.py`.
- Validate generated NWB files with `pynwb.validate`.
- Run NWB Inspector on generated examples with threshold `BEST_PRACTICE_VIOLATION`.
- Run `ndx_cell_culture.validate_recommended_terms` on generated examples and expected release fixtures.
- Confirm subject-to-culture, cell-line parent, culture source-line, and culture parent relationships all round-trip.
- Install docs dependencies with `python -m pip install -e ".[docs]"`.
- Build HTML docs with `make -C docs/source html` and review `docs/_build/html`.
- Build wheel and source distribution with `python -m build --sdist --wheel`.
- Check distribution metadata with `python -m twine check dist/*`.
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
- Update `docs/catalog/ndx-meta.yaml.template` with the final PyPI URL and release version.
- Submit the completed catalog metadata to the NWB staged extensions repository.
- For DANDI-facing datasets, document the exact `ndx-cell-culture` version used to create the NWB files.

## Documentation

- Generated source files live under `docs/source`.
- The Sphinx HTML build output is intentionally untracked at `docs/_build/html`.
- Host the contents of `docs/_build/html` when publishing public documentation.
- Read the Docs can import this repository using the root `.readthedocs.yaml` file. The RTD project should build from `docs/source/source/conf.py` and install the package with the `docs` extra.

## External Review

Before recommending broad production use, review the extension with NWB maintainers and at least one external cell-culture lab. The schema is designed to be usable before NWB-core inclusion, but maintainer feedback should inform the first stable release.
