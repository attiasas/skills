# Triage labels

This file maps role names to the label strings on this repo's tracker. An empty Tracker label cell is not applied. Do not create a label to fill a cell.

## State

A new issue takes at most the `needs-triage` string. The other four rows are later states. `to-spec`, `to-tickets`, and `wayfinder` do not set those four.

| Role | Tracker label | Meaning |
| --- | --- | --- |
| needs-triage | | A maintainer still has to evaluate the issue. New issues enter here. |
| needs-info | | Waiting on the reporter. |
| ready-for-agent | | Specified enough for an unattended agent. |
| ready-for-human | | A person has to do the work. |
| wontfix | | Will not be done. |

## Type

A new issue from `to-spec` or `to-tickets` takes at most one type string. `wayfinder` sets a type only when the human names one. One row per kind of work this repo uses.

| Role | Tracker label | Meaning |
| --- | --- | --- |
| bug | | Something is broken. |
| enhancement | | A change or an improvement. |

## Applying labels

On the draft, above the body:

- `Type:` the Tracker label of the one type row that fits
- `State:` the Tracker label of `needs-triage`

`to-spec` uses the bug row when the draft has steps to reproduce. Otherwise the human confirms the type. `to-tickets` names the type on each slice. `wayfinder` shows State only.

The human approves the lines with the draft. Publish applies those strings the way `.agent-repo-config/issue-tracker.md` says under "apply a triage label". Skip an empty cell. Apply no string that is not in this file. A triage type is a label. It is not a Jira issue type.
