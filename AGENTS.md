Use `trash` instead of `rm`.

Maintain a concise `CHANGELOG.md` when working in this repository. Add entries
for major work iterations and for documentation or workflow updates that change
how users, operators, or developers use the repo. Use one-line entries in
`YYYY-MM-DD HH:MM | area | summary` format, focused on the broad work area
rather than implementation detail.

Public documentation should describe the current user-facing model. Do not add
workbook history, version-planning history, internal rationale sections, or
architecture-decision logs to Read the Docs or other public user docs.

If historical rationale is useful for future agents, keep it in `AGENTS.md`,
maintainer notes, or other internal planning notes. Review any material copied
from `docs/*` before adding it to the Sphinx docs to make sure it is appropriate
for external labs and NWB reviewers.

PyNWB/HDMF compatibility note: CI runs Python 3.8 through 3.12, and readback
behavior can differ by Python/PyNWB/HDMF combination. If Python 3.8/3.9 fail
while 3.12 passes, reproduce serially with
`uv run --python 3.9 --extra test --extra docs bash scripts/check_release.sh`.
Do not run multiple `uv run --python ...` commands in parallel because they
share and rewrite `.venv`. A recurring failure mode is duplicate construction
when an object is represented both as a contained child group and as a link to
that same child, e.g. `CellCultureSubject.culture` plus the generated
`cell_cultures` collection. Fix this in the Python compatibility shim by
de-duplicating by object identity/name before calling the generated constructor,
then verify at least Python 3.8, 3.9, and 3.12.
