# Summary page guide

How to fill [summary-template.html](summary-template.html). Read it once, then write `summary.src.html` and build it. The template holds markup only. Do not copy comments, and do not inline CSS or JS: leave the `<link rel="stylesheet" href="summary.css">` and `<script src="summary.js"></script>` tags as they are.

## Build

```
python3 <skill-dir>/build-summary.py .agent-docs/implement-spec-<slug>/summary.src.html
```

It writes `summary.html` beside the source, with the CSS and JS inlined. It exits 1 and lists every problem: a placeholder left in, a `#id` link with no target, a `file:///` link that is not absolute or points at nothing, a link that is not `#id`, `file:///`, or `https://`. Fix `summary.src.html` and run it again. Open `summary.html`.

## Links

Every path, branch, commit, ticket, test, and criterion is a link. The link text is the short name (`spec.md`, `abc1234`, `T2`). The href is the full target.

| Target | href |
| --- | --- |
| On this page | `#ac-ID`, `#mt-ID`, `#task-ID`, `#change-ID`, `#val-ID`. Give the target that id. |
| File on disk | `file:///ABSOLUTE/PATH/file.ext`, add `#L42` for a line |
| Directory on disk | `file:///ABSOLUTE/PATH/dir/` |
| Ticket, pull request, branch, commit | the full `https://` URL |

## Numbers

Each count is the output of a command or a count of rows on this page. Never estimate or round. Delete a card or a count you cannot measure and name it in chat. Put the commands in the `src` lines of their section.

## Evidence

Write each command's full output to `.agent-docs/implement-spec-<slug>/evidence/<id>.log` (`<id>` is the change, validation, or manual test id) and link it as "full output". On the page show the command and at most five lines of its output. Output appears once, in Validations. Other tables link to it.

## Rows to repeat

Repeat once per item and delete the example row.

- Overview: one card per status you can measure, one `li` per open item the human should act on (a fail, a gap, a deviation needing a decision, a manual test to run, a Minor finding to accept; say what to do and link to it), one line per task branch. With nothing open, keep only `li.none`.
- Definition of done: the four rows stay. Pill is `pass`, `fail`, or `gap`, taken from the review verdicts. Basis is a short count or reason that links to the table that shows it, for example "5 of 5 criteria pass", "0 unlogged deviations, 1 logged", "no flag or dependency added", "12 tests, all run". Safe to run is `pass` with the reason "nothing to operate" when the change adds no dependency call, queue, flag, or metric.
- Spec: one row per acceptance criterion and per validation in `spec.md`. Status pill: `pass`, `fail`, `gap`. Test: `Existing test` with a link to it, or `New` when the change added the first test. Evidence is a few links or counts. Delete the HLD row for a small change.
- Manual tests: one article each. Delete the whole group and say so in chat when `testing.md` has none. A manual test the agent did not run is a gap.
- Test suites: one row per suite run. Reviews: one row per review (code review, each expert lens, QA).
- Validations: one row per item. Pill: `pass`, `fail`, `gap`.
- Implementation: one row per task and per deviation. Triage pill: `planned`, `deviation`, `fix`. Task done pill: `pass` when finished, `gap` when not.

## Manual acceptance tests

Written for the human to run and see the change work.

- **Scenario.** Gherkin, per [Gherkin for PMs](https://github.jfrog.info/pages/JFROG/jfs-quality-hub/library/gherkin/): one behaviour, concrete values (10,000 artifacts, not "many"), what the user sees and not how the code works, a `Then` someone can check. Split a flow that configures and runs into two. Order the tests happy path first, then failure, then edge cases (timeout, partial data, permissions, scale, a silent failure such as zero results where there were results).
- **Already prepared.** Do the setup yourself: the directory, the build, the seed data, the process to start. The human only acts and looks. A setup action the human must take is step 1.
- **Steps.** The fewest that run the scenario. One action each. A command is optional when the step is a click or a look. Each has what to expect.
- **Pass and fail.** State what counts as each.
