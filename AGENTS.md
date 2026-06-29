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
