# Synthetic Examples

The example builders in `examples/scenario_builders.py` create small NWB files that exercise the extension. All identifiers and biological details are synthetic.

Run all scenarios:

```bash
python examples/create_synthetic_scenarios.py
```

Generated `.nwb` files are written to `examples/generated_scenarios/`, which is ignored by git.

## Scenario Coverage

| Scenario | Builder | Purpose |
| --- | --- | --- |
| Basic organoid | `build_basic_organoid` | Complete synthetic organoid with a subject-to-culture link, direct source-line provenance, line-level variant, culture-level construct application, protocol metadata, MEA context, and core `Device`. |
| Slice patch clamp | `build_slice_patch_clamp` | Organoid-derived slice with `parent_cultures` provenance, patch-clamp device metadata, AAV construct application, and two pharmacology entries. |
| Edited iPSC organoid | `build_edited_ipsc_organoid_mea` | Synthetic edited iPSC lineage using `parent_cell_line`, line-level variant, `source_lines` provenance, protocol metadata, MEA context, and no pharmacology. |
| Biological metadata only | `build_biological_metadata_only_organoid` | Synthetic organoid with culture and line catalogs but no recording/session context. |
| Pharmacology titration | `build_pharmacology_titration_organoid` | Synthetic organoid recording with a pharmacology concentration range and MEA device. |
| Directoid | `build_directoid` | Directoid/connectoid-style `assembloid` example with two parent organoids represented by `parent_cultures`. |
| Two-line assembloid | `build_two_line_assembloid` | `assembloid` example from two distinct synthetic source lines represented by `source_lines`. |

## Expected Validation

The test suite writes and reads the scenario files with `NWBHDF5IO`. This verifies:

- namespace loading;
- all extension-owned neurodata types can be instantiated;
- `CellCultureSubject` can be stored in `NWBFile.subject`;
- `CultureExperimentContext` can be stored under `NWBFile.lab_meta_data`;
- `CellLine` and `CellCulture` catalog entries round-trip;
- `parent_cell_line`, `source_lines`, and `parent_cultures` provenance references round-trip;
- `ExperimentContext` links to `CellCultureSubject`, `CellCulture`, and core NWB `Device`;
- repeated `Pharmacology` children round-trip;
- synthetic examples cover edited lines, pharmacology, slice recordings, multi-source cultures, directoid-style parent cultures, and biological-metadata-only files.
