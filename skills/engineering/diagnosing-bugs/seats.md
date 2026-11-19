# Seat briefs

One seat at a time: Loop, then Cause, then Probe, then Validation. Wait for the seat before dispatching the next. Paste the brief below and the inputs it names. The seat returns only the output shape.

Loop may add a throwaway script or one red test. It must not change production code to hide or create the bug, and it must not commit. Cause is read-only. Probe may add `[DEBUG-` logs and a measurement. It must not apply the fix. Validation is read-only: it runs commands, and it must not commit, edit source, or move HEAD.

## Loop

Build one command that goes red on the symptom. Shrink it until every remaining part is load-bearing. Return the command and the output. Do not name a cause.

Inputs: the symptom line, the repo, and a command the human already gave, when they gave one.

When a command was given, run it. When it goes red on this symptom, shrink it. When it does not, build one.

Stop at the first command that goes red on this symptom:

1. A failing test at the seam the caller hits.
2. An HTTP call against a running dev server.
3. A CLI call with a fixture, diffed against known-good output.
4. A headless browser script that asserts on the DOM, the console, or the network.
5. A saved request, payload, or event log, replayed through the failing path.
6. A tiny harness: one service, mocked deps, one call.
7. Many inputs, when the bug is "sometimes wrong". Keep the one input that fails.
8. A script that boots a state and checks, when the bug appeared between two known states, so `git bisect run` can drive it.
9. The same input through the old version and the new one, then a diff.
10. A copy of this skill's `scripts/hitl-loop.template.sh`, when a person must click. Last.

Then make it faster, assert the symptom itself, and pin time, seed, filesystem, and network where the result depends on them.

For a flake, the goal is a higher reproduction rate. Loop the trigger, add stress, narrow the timing window. Return the pinned rate. A rate high enough to debug against is steady enough.

For a slow path, the command prints a duration and exits non-zero over the baseline.

Shrink by cutting inputs, callers, config, data, and steps one at a time. Re-run after each cut. Keep a cut when the command stays red. Stop when removing any one remaining part makes it go green.

When the command's output would not contain the symptom in the human's words, also leave one wrapper command that prints that symptom, and name it as the manual command. The manual command exits non-zero while the bug is present and zero once it is gone, so the same paste validates. The test, when you add one, stays red. Its name and assertion use the human's words.

```
### Command
directory:
command:
original command:
manual command:
red: yes | no
steady: yes | flake <rate>
seconds:
output:

### Minimal
- kept: <why it is load-bearing>
- cut: <what was removed, and that the command stayed red>

### Tried
- command:
  output:
  why it was not the loop:
```

## Cause

Rank hypotheses for the symptom. Do not test them. Do not read a theory the parent believes.

Inputs: the symptom line, the red command, its output, and the kept parts.

Return 3 to 5 hypotheses, strongest first. Each prediction names a change: this change makes the loop go green, or this other change makes it worse. Drop a hypothesis with no prediction.

When two hypotheses are the only predictions that name a different change, return those and name the restatement you refused.

```
### Hypotheses
- rank:
  hypothesis:
  prediction:
  file:
```

## Probe

Test the ranked predictions. One change at a time. Map each probe to one rank. Do not apply the fix. Do not add a hypothesis the list does not have. When a prediction is not falsifiable, drop it and say so.

Inputs: the symptom, the red command, the ranked list, and a re-rank from the human when there is one.

Prefer a debugger or a REPL when the environment has one. Otherwise log at the boundary that separates two hypotheses. Tag every log `[DEBUG-` plus four letters.

A slow bug: record a baseline duration, then bisect. The probe is a measurement.

```
### Probes
- rank:
  disposition: confirmed | ruled out | open
  change:
  command:
  output:
  file:
```

`confirmed` means the loop moved the way the prediction said. `ruled out` means it did not. `open` means this probe does not decide.

## Validation

Re-run the checks. Write the two manual lists. Do not edit source.

Inputs: the symptom line, the Loop command and its red output, the original command from before the shrink, the manual command when Loop named one, the regression test command when a test exists, and whether a fix has been applied.

Run the Loop command, the original command when it differs, and the regression test. Record each output.

Manual replication shows the bug. Manual validation is the same steps and shows the fix.

- One pasteable block when one command can show the result. It starts with `cd` to the directory. It exits non-zero while the bug is present and zero once it is gone. The output contains the symptom, or the fixed result, in the human's words: the message, the status, the number, or the time.
- Use the manual command Loop named when the Loop command's output would not show that symptom.
- Manual validation repeats that same block. Do not invent a second procedure.
- Add a step only when one command cannot show the result. One action per step.
- Every command is complete. No placeholder and no secret.
- A click path is numbered, one click per step, with the URL in the step.
- The red output in Manual replication is the output Loop captured. The output in Manual validation is the run you just did. When no fix has been applied, set `ran: no` and leave the green output empty.

```
### Replicate
directory:
bug looks like:
block: |
  <pasteable block>
output:

### Validate
fixed looks like:
same block: yes
ran: yes | no
output:

### Checks
- name:
  result: pass | fail | gap
  command:
  output:
  who: Validation
```
