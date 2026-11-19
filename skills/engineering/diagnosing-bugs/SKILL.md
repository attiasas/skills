---
name: diagnosing-bugs
description: Finds the cause of a hard bug or a performance regression with a failing loop before any theory, then fixes it and writes a report whose manual replication and manual validation are the fewest steps that show the bug and the fix, each with the command and its output. Use when the user says "diagnose" or "debug this", or reports something broken, throwing, failing, or slow.
---

# Diagnosing bugs

A hard bug or a slow path. Get one command that fails on this symptom, find which change makes that command pass, then show the human the shortest way to see the bug and the shortest way to see the fix.

Dispatch a general-purpose subagent, one seat at a time, and wait for it. Start each with a fresh context window. Use the model the human named. Otherwise use the default model. Fill the brief in [seats.md](seats.md). Send the symptom and the inputs that brief names.

Fix unless the human asked only for the cause. Write the report either way.

## Redact

Commands, outputs, and captured files get shown. Replace every secret with `<REDACTED>` before it appears in chat or on the page. Quote the lines that carry the signal. When the redacted output is not enough, say so and ask.

## 1. Symptom

Write the failure in the human's words, one line: what they did, what they saw, what they expected. That line is what the loop must catch. A nearby error is a different bug.

## 2. Loop

Dispatch **Loop**. It builds and runs one command that goes red on this symptom, then shrinks the repro until every remaining part is load-bearing.

The next step waits until that command has gone red in this session, and it is:

- **This bug.** It drives the failing path and the output contains the symptom in the human's words. "It ran" is not red.
- **Steady.** Same verdict each run. For a flake, a pinned rate high enough to debug against.
- **Fast.** Seconds.
- **Unattended.** You can run it. A person clicks only through a copy of [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh), and only while the loop is being built.

When no such command exists, status is Still open. List what Loop tried, each command with its output. Ask for an environment that reproduces it, a redacted capture, or permission to instrument production. Stop.

## 3. Cause

Dispatch **Cause** with the symptom and the red command. It returns 3 to 5 ranked hypotheses. Each one states the prediction: if this is the cause, this change makes the loop go green, or this other change makes it worse.

Show the ranked list. Apply a re-rank if the human sends one. When the human is away, probe the ranking Cause returned.

Dispatch **Probe** with that list and the red command. One variable at a time. Each probe maps to one prediction. A slow bug is a timing command and a bisection.

Tag every debug log `[DEBUG-` plus four letters. Cleanup greps that prefix.

## 4. Fix

Skip this step when the human asked only for the cause.

A correct seam exercises the bug the way the caller hits it. When no correct seam exists, say so in the report under Checks and leave the test unwritten.

When a seam exists and Loop has not already left a red test there, call `tdd`. The one behaviour is the minimised repro. The test name and the assertion use the human's words for the symptom, so the test output is readable as the bug. Watch it fail for this symptom, then pass.

When Loop already left that red test, run it, confirm the failure is this symptom, and make it pass.

Loop records the command from before the shrink. Step 6 runs that original command again.

## 5. Cleanup

Before validation:

- Grep every `[DEBUG-` prefix and remove those lines.
- Delete throwaway prototypes. Keep the red-then-green test, and keep a one-command wrapper only when the manual steps need it.
- The confirmed hypothesis is the Cause section of the report. When the human asks to commit, the message uses that sentence.

## 6. Validate

Dispatch **Validation**. It re-runs the Loop command and the regression test. It writes **Manual replication** and **Manual validation**. It does not edit source and it does not commit.

Copy those two lists into the report. Send the list back when it breaks a rule below. One return.

Both lists follow these rules:

- One pasteable block when one command can show the result. The block starts with `cd` to the directory. The same block exits non-zero while the bug is present and zero once it is gone. Its output contains the symptom, or the fixed result, in the human's words (the message, the status, the number, or the time).
- Manual validation is that same block. A second procedure means send it back.
- More than one step only when one command cannot show the result. Then the fewest actions, one action per step: one command, one click, or one line to paste.
- The first step names the directory. Every command is complete. A value the human would have to invent means send it back.
- Drop a step that is not load-bearing. If the result still shows without it, it is not on the list.
- A click path is numbered, one click per step, with the URL in the step. The report names the hitl script only as how the loop was built.

A person with the repo and nothing else can follow the list.

## 7. Report

Write the report in chat, in this order.

1. **Status.** `Fixed`, `Cause found`, or `Still open`.
2. **Symptom.** The line from step 1.
3. **Cause.** The confirmed hypothesis, the file and line, and the prediction that held. When none is confirmed, "No cause yet."
4. **Manual replication.** The steps, what the bug looks like, and the redacted output from when it was red.
5. **Manual validation.** The same steps, what fixed looks like, and the output of the run after the fix. When the fix is not in, the steps stay and the result is Not run.
6. **Loop.** The command, the directory, who ran it, and the redacted output.
7. **Triage.** Each hypothesis: confirmed, ruled out, or open, with the evidence.
8. **Checks.** Each command: pass, fail, or gap, the output, and who ran it.
9. **Cleanup.** The grep and its result.

Then write `.agent-docs/diagnosis-<slug>.html` in the repo under diagnosis, following [report-example.html](report-example.html). The slug is 2 to 4 kebab-case words from the symptom. Do not edit the example. Self-contained, no external assets. Each section is a collapsible block, open to start. The status pill uses `fixed`, `found`, or `open`. Each paste block has a Copy button. Before the first write, add `.agent-docs/` to `.git/info/exclude` when no ignore rule already covers it. Do not touch `.gitignore`. Open the page with `open`. There is no server.

The page carries the same sections as the chat. The chat stays complete.

## Triage

| Disposition | Meaning |
| --- | --- |
| confirmed | The prediction held. The loop moved the way that hypothesis said. |
| ruled out | The prediction failed. |
| open | Not tested, or the evidence does not decide. |

One confirmed hypothesis is the cause. Two confirmed means Probe has not separated them; probe again before the report. Evidence is a command and its output, or a file and line.

## Checks

| Result | Meaning |
| --- | --- |
| pass | The command ran and the output is the fixed result, or the test passed. |
| fail | The command ran and the bug is still there. |
| gap | The command has not been run. Manual replication or manual validation is that command. |

`Fixed` requires the original loop to pass and, when a seam exists, the regression test to pass. A gap or a fail on either one keeps the status at `Cause found`.

## Never

- Dispatch Cause before a red command exists
- Send Cause or Probe this session's theory
- Probe before the ranked list was shown
- Treat a nearby failure as this bug
- Add a test that cannot catch this symptom
- Leave a `[DEBUG-` line in the tree
- Leave a placeholder, a secret, or "check that it works" in either manual list
- Write manual validation as a different procedure
- Treat a sentence with no command as a pass
- Skip the page
- Touch `.gitignore` to hide the page

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "I can see the cause, so skip the loop." | The loop is what makes the cause checkable. No red command, no Cause seat. |
| "They want the fix now." | The same command that goes red is what shows the fix. |
| "A unit test nearby is close enough." | The command has to catch this symptom, in the human's words. |
| "The steps are obvious." | Manual replication is the fewest actions, written out, with the exact thing they see. |
| "I'll describe how to tell it's fixed." | Manual validation is those same steps and the exact green result. |
| "One hypothesis is enough." | Rank 3 to 5 and show them before Probe. |
| "The logs will show it." | Tag `[DEBUG-` and grep the prefix out before the report. |
| "The test output is enough for the human." | The manual output contains the symptom they reported. When the test output would not, the manual command is the one-command wrapper that prints it. |
