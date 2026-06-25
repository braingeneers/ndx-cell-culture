# Review Examples

The example builders in `examples/scenario_builders.py` are executable review fixtures. They are intentionally small but cover the biological cases from the review workbook and formal notes.

Run all review scenarios:

```bash
python examples/create_review_scenarios.py
```

Generated `.nwb` files are written to `examples/generated_scenarios/`, which is ignored by git.

## Scenario Coverage

| Scenario | Builder | Purpose |
| --- | --- | --- |
| Basic organoid | `build_basic_organoid` | Complete synthetic organoid with `CellCultureSubject`, `CellCulture`, `CellLine`, `GeneticVariant`, `ConstructApplication`, `CultureProtocol`, `ExperimentContext`, core `Device`, and `CultureExperimentContext`. |
| Slice patch clamp | `build_slice_patch_clamp` | Slice culture with patch-clamp device metadata, AAV construct application, and two pharmacology entries. |
| KOLF SHANK3 Org1 | `build_kolf_shank3_org1` | Manual validation example with KOLF line lineage, SHANK3 variant, protocol metadata, MEA context, and no pharmacology. |
| KOLF SHANK3 Org2 | `build_kolf_shank3_org2` | Manual validation example with biological metadata only and no experiment context. |
| H9 DO11 Ketamine | `build_h9_do11_ketamine` | Manual validation example with ketamine pharmacology range, MEA device, and H9 ESC source line. |
| Directoid | `build_directoid` | Synthetic directoid/connectoid-style `assembloid` example with two brain-region source lines and microfluidic-channel provenance in protocol/notes. |
| Two-line assembloid | `build_two_line_assembloid` | Synthetic `assembloid` example from two distinct source lines. |

## Expected Validation

The test suite writes and reads the scenario files with `NWBHDF5IO`. This verifies:

- namespace loading;
- all extension-owned neurodata types can be instantiated;
- `CellCultureSubject` can be stored in `NWBFile.subject`;
- `CultureExperimentContext` can be stored under `NWBFile.lab_meta_data`;
- `ExperimentContext` links to `CellCultureSubject`, `CellCulture`, and core NWB `Device`;
- repeated `Pharmacology` children round-trip;
- manual examples preserve their key biological identifiers.

The recursive provenance fields are present in the schema but are not asserted as release-ready examples yet. Their final representation should be confirmed with NWB maintainers.
