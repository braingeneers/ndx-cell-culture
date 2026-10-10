The `legacy_rc2` schema is frozen from tag `v1.0rc2`. The `legacy_rc3` schema
is frozen from commit `8f46379`, before the single-parent constraint was added.

Parent-line compatibility tests create NWB files with these schemas in separate
Python processes, without importing the current extension package. Keep the
snapshots unchanged so regenerated current schemas cannot hide compatibility
regressions. No binary NWB fixtures are committed.
