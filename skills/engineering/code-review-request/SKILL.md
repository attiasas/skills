---
name: code-review-request
description: Dispatches a fresh-context review of completed work, adding a specialist only when the diff matches that lens, and runs a validation pass that records each command and its output. Use when finishing a task, a major feature, or before merging. Writes the HTML report only when asked, and posts pull-request comments only after a yes in chat.
---

# Request a code review

Review completed work before it cascades. Dispatch fresh-context seats, run the checks, and write one report. A seat sees the diff and the requirements. It does not see this session's history or another seat's findings.

## When

Use a **task checkpoint** after a task, and when the review is because you are stuck, before a refactor, or after a complex bug.

Use the **before-merge** bar after a major feature and before a merge.

## Range

Pin the base and the head. Read `git diff --stat <base>..<head>` and `git rev-list --count <base>..<head>`. Record the branch, the base it comes from, and the commit count. Record a pull request link when one exists, and an issue link when the work names one.

## Seats

Dispatch every matching seat in one turn, plus validation. Use a general-purpose subagent and a fresh context. Fill [seats.md](seats.md).

| Seat | Dispatch when |
| --- | --- |
| Code reviewer | Always. Defects, quality, plan alignment. |
| Tech lead | Two or more components, or 8 or more files, or 400 or more changed lines. If you cannot tell whether two paths are one component, they are two. |
| Security | Auth, secrets, personal data, permissions, or untrusted input. |
| Data | Schema, migration, or backfill. |
| Contract | A public HTTP, RPC, event, or CLI contract changes. |
| Concurrency | Shared mutable state, locking, or async coordination. |
| Validation | Always. It runs the checks. It does not review. |

A skipped seat is one line: the lens and the predicate that failed. Domain, frontend, performance, and operations are not seats.

## Evidence

Validation executes. It does not commit and it does not edit source.

On a task checkpoint, run the tests that cover the diff. Record the command and the output. An observable criterion that needs the full system, and cannot be run yet, is a `gap`. A gap does not block the next task. A check that ran and failed is a `fail`, and a fail blocks.

On the before-merge bar, every observable acceptance criterion needs a real command and its output. A gap or a fail blocks a Yes. A unit test counts only for the criterion it asserts.

A sentence with no command is a gap. A manual validation is one command from a named directory, what it covers, what a pass looks like, and who ran it. A run includes the output.

## Aggregate

Wait for every seat you dispatched.

One finding per issue. When two seats describe the same issue at the same severity, keep the sharper write-up and name both. When they judge the same change differently, keep both items under Disagreements. The verdict uses the stronger one.

Verdict, first match:

- **No** when any finding is critical, any seat says No, or a fail is open. On the before-merge bar a gap is also No.
- **With fixes** when anything important remains.
- **Yes** when every seat that ran says Yes and nothing above minor remains.

The status line is `Not ready for merge`, `Ready with fixes`, or `Ready for merge`.

## Report

Write the report in chat, in this order: mode and status, range, a two-or-three-line summary with strengths and risks, roster, acceptance status, manual validations, disagreements, findings. Group findings critical, then important, then minor. Omit an empty severity.

Each finding and each disagreement has severity, type, the seat it is from, a title, the file, what is wrong, and a suggestion. Types are defect, spec gap, design, security, data, contract, and test gap.

Write the HTML page only when they ask. Put it at `.agent-docs/code-review-<short-sha>.html` in the repo under review, following [report-example.html](report-example.html). Do not edit the example. Open the page with `open`. There is no server.

## Act

Fix a critical finding before anything else. Fix an important finding before the next task, or before the merge. Record a minor finding and leave it. Push back when a finding is wrong, and show the code or the output that shows it.

When the review is a pull request, ask whether to post the findings as review comments. Post each finding and each disagreement as its own comment, and only after a yes.

## Never

- Skip a seat whose predicate matches
- Show one seat another's findings
- Treat a sentence with no command as a pass
- Collapse a disagreement into one milder finding
- Write the HTML page when they did not ask
- Post pull-request comments before a yes
