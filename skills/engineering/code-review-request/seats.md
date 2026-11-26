# Seat briefs

Fill one brief per seat. Send the description, the requirements or plan, the base, and the head. Send the mode (`task checkpoint` or `before merge`) to validation only. On a follow-up, also send the previous head and each prior finding, disagreement, and failed or gap check.

Reviewer seats are read-only on this checkout. Do not commit, edit source, or move HEAD. Inspect with `git show`, `git diff`, and `git log`. Use a temporary worktree for another revision.

Validation may run tests and the one-command checks below. It still must not commit, edit source, or move HEAD.

Stay in the lens. Cite a file and line for every claim. Return only the output shape.

## Code reviewer

Defects, quality, and plan alignment. Missing behavior, a wrong behavior, a test that does not assert the criterion, a plan item with no code, and a change in the diff that maps to no requirement and no plan item (an unlogged deviation) are in this lens. Leave system shape to the tech lead and leave security, data, contract, and concurrency to those seats when they are running.

## Tech lead

Whether the design holds across components. Name the components, the direction of each new dependency, and the seam. A boundary or contract that cannot ship or roll back independently is in this lens. Do not restate a line-by-line review.

## Security

Auth, secrets, personal data, permissions, and untrusted input. Name the trust boundary. A finding is in this lens only when the diff crosses it.

## Data

Schema, migration, and backfill. Consistency, rollback of the migration, and what old rows do after the change are in this lens.

## Contract

A public HTTP, RPC, event, or CLI contract. Callers, compatibility, and the error a caller sees are in this lens. An internal function is not a contract.

## Concurrency

Shared mutable state, locking, and async coordination. The interleaving and the state it corrupts are in this lens.

## Validation

Run the checks. Do not judge design.

On a task checkpoint, run the tests that cover the diff. A criterion that needs the full system, and cannot be run yet, is a gap. On the before-merge bar, every observable acceptance criterion needs a real command and its output. A unit test counts only for the criterion it asserts. A sentence with no command is a gap.

Add a manual validation for an observable criterion the tests do not exercise. One command, the directory, what it covers, and what a pass looks like. If you ran it, include the output and your seat name. If you did not, say nobody has run it.

## Reviewer output

```
### Findings
- severity: critical | important | minor
  type: defect | spec gap | design | security | data | contract | test gap
  file:
  title:
  wrong:
  suggestion:

### Assessment
Ready: Yes | No | With fixes
Reasoning: one or two sentences

### Prior
- title:
  status: fixed | still open | gone
  evidence:
```

Include Prior only on a follow-up. `fixed` means the current tree no longer has the defect. `gone` means the code it cited is gone. `still open` means it remains. Do not file a fixed or gone item again under Findings.

`critical` is a break, a security hole, or lost data. `important` should be fixed before the next task or the merge. `minor` can wait. A plan item with no code is a spec gap. A missing test is a test gap.

## Validation output

```
### Checks
- criterion:
  result: pass | fail | gap
  command:
  output:
  who:

### Manual
- title:
  covers:
  directory:
  command:
  pass:
  ran:
  output:
```
