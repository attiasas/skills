---
name: implement-spec
description: Implement any spec (issue, file, or conversation). Validates and sizes it, requires an approved HLD for large changes, plans, implements with subagents, then reviews. Before anything lands on the integration branch, shows an HTML summary of the implementation and of each change and validation traced to the spec with evidence, and waits for commit or adjust. Pushes when a check needs it, and opens a pull request when asked. Never merges or closes tickets. Optionally records the plan, changes, and testing on the tracker.
disable-model-invocation: true
---

# Implement spec

Take a spec from validation through review. Task branches hold the work until the human has seen the HTML summary and chosen to commit. That choice updates the integration branch. Open a pull request when the human asks, and only after that commit. Do not merge the pull request, close a ticket, or move a ticket's status in this session.

Everything this skill writes, apart from code, goes under `.agent-docs/implement-spec-<slug>/`, where the slug is 2 to 4 kebab-case words from the spec. Create the directory if it is missing. If `.gitignore` does not already ignore `.agent-docs/`, add that line.

Start every subagent with a fresh context window. Talk to subagents through pointers (`spec.md`, `hld.md`, `plan.md`, research notes, commits) and leave out text those files already hold. Use the model the human named. Otherwise use the default model.

## 1. Gather

The input is anything that holds a spec:

- **Issue** (number, key, or URL). Read `.agent-repo-config/issue-tracker.md`. If it is missing, stop and tell the human to run `setup-repo-skills`. Follow "fetch the task graph", comments included. Child issues are tickets. A lone issue is its own ticket and its own parent.
- **Path** to a file (spec, `handover.md`, HLD, plan). Read the whole file and every file it links to. Issue ids it names are tickets.
- **Conversation.** Use what the chat settled.

Write the spec, as found, to `spec.md`. Put its source on the first line. When the input already holds an HLD or a plan, copy it to `hld.md` or `plan.md`.

## 2. Validate and size

Check the spec before any design or code. Tell the human the result in a short list.

- **Valid.** It states a goal and acceptance criteria that a test can check. Each item under **Validations** is an acceptance criterion. When there are no acceptance criteria and no validations, stop and tell the human to run `to-spec`. Do not write them yourself.
- **Context.** List what an implementer would need and cannot find: an undecided behaviour, a missing error case, an unknown external API, a referenced doc or ticket that is not reachable. Look up what the code, the tracker, or the `research` skill can answer. Ask the human the rest in one message, with `AskQuestion` when the options are clear. Record the answers in `spec.md` under `## Clarifications`.
- **Undiagnosed bug.** The input is a failure and nothing settles the cause. Call `diagnosing-bugs` first. Do not plan a fix for a cause you have not reproduced.
- **Several features** that ship independently, with no tickets yet. Tell the human to run `to-tickets`. Stop.

Then size it. When the context or the size depends on code you have not read, and that reading is more than a quick look, dispatch an **exploration subagent** with a fresh context. It writes `exploration.md` in the work directory: the modules the spec touches, the existing patterns, and anything the spec leaves out. Size from that file. Skip the subagent when you can already name what changes and where, and say so.

State the size and the fact that decided it:

- **Small.** One module changes, no schema change, no contract change (API, event, file format), and no scale or latency target.
- **Large.** Anything else, including a change that touches two or more modules, services, or top-level areas.

## 3. HLD (large only)

A large change needs an approved HLD before a plan. Skip this step for a small change.

- **Provided.** Use `hld.md`. Ask the human to confirm it is the approved version, unless the input already records that approval.
- **Not provided.** When the design is still foggy (several viable approaches, open product questions), tell the human to run `hld-planner` and come back with its HLD. Stop. Otherwise call `to-hld` with the output path `.agent-docs/implement-spec-<slug>/hld.md`.

Show the HLD path and a short summary. Apply the human's edits. Continue only after they approve it. "Looks fine, go" counts. Silence does not.

## 4. Plan

When `plan.md` was provided, check that every acceptance criterion and every validation maps to a task and that it agrees with `hld.md`. Fix the gaps and say what you changed.

Otherwise write `plan.md` from [plan-template.md](plan-template.md), built from `spec.md` and `hld.md`. Show the path and a one-line summary per task, then continue. Do not wait.

The plan's tasks and their `Blocked by` lines are the **task graph**. The **frontier** is the set of tasks whose blockers are all done. When the input has tickets, each ticket maps to one or more tasks.

## 5. Progress question

Ask once whether to record progress on the tracker. Ask only when at least one issue id is in hand. With no ids, skip the question and write nothing to a tracker. A yes covers the whole run, and you post each note without showing it first. A no means no notes. See [Progress](#progress).

## 6. Implement

1. Create the **integration branch** from the base branch. When progress is on, post the **Plan** note.
2. For each frontier task, dispatch an **implementer subagent** in its own worktree on its own branch, in the background where possible. When the plan is one task, dispatch one. Each implementer:
   - confirms its worktree is based on the integration branch tip, and resets onto it when it is not;
   - calls the `tdd` skill to build its task;
   - merges the integration branch tip into its branch before reporting;
   - reports commits, the tests it added and ran with their results, and every **deviation**: a place where it did something other than the plan says, or hit something the plan missed. It gives what changed and why.
3. Leave each finished branch unmerged. The integration branch stays at the base tip until step 8. When a blocker has reported done, dispatch the tasks it unblocks. Each of those implementers merges the blocker task branches into its own branch, in task order, before building. It does not merge into the integration branch.
4. Add every deviation to `changes.md` with its source (implementation, review, QA), what changed, and why. Update `plan.md` to match. When progress is on, post a **Change** note. When a deviation changes the approved HLD's decisions, stop and ask the human before continuing.

Push a task branch when a check needs the remote, such as CI or a test suite that runs only there. Say why you are pushing. Do not push the integration branch in this step. A draft pull request of a task branch is allowed for the same reason, and not required. Do not mark a draft ready in this step, and do not open a pull request for any other reason.

## 7. Review and QA

When every task has reported done, review the combined diff against the base branch. Do that in a review worktree whose HEAD is the finished task branches merged together. It is not the integration branch. Run code review, expert review, and QA there, so `HEAD` is that combined diff. After a fix, rebuild the worktree from the task branches before the next pass. Delete it when step 7 is finished. Do not update the integration branch:

- **Code review.** Always. Call the `code-review` skill with the base branch as the fixed point and `spec.md` as the spec.
- **Expert review.** When the diff touches a lens that a generalist reviewer would miss, such as security, data migration, concurrency, performance, or a public contract. Dispatch one reviewer subagent per lens with the diff range, `spec.md`, and `hld.md`.
- **QA.** When the spec has behaviour a user or caller can observe. Dispatch a QA subagent that checks each acceptance criterion and each validation end to end, beyond the unit tests: run the app, the CLI, or the integration suite. It reports pass or fail per criterion and per validation, with the command and the output.

Wait for every reviewer you dispatched. Fix Critical and Important findings and QA failures in a fresh **implementer subagent** on the task branch the finding belongs to. Do not merge into the integration branch. Each fix that changes behaviour or the plan is a deviation (step 6.4). Re-run the reviews that raised findings until none is Critical or Important. Write Minor findings you did not fix into `testing.md`.

Write `testing.md`: tests added, suites run and their results, the QA result per acceptance criterion and per validation, the review verdicts, and any known gaps. A check outside the automated suite is a manual test. Record each one: the spec item it validates, the directory, the command or the steps, what pass looks like, who ran it, the result, and the output.

## 8. Summary, then commit

Only after step 7 has no open Critical or Important finding.

Write `summary.html` from [summary-template.html](summary-template.html). Replace every UPPERCASE placeholder. Repeat a marked row, tile, or article once per item. The page is the record, not a digest: carry `spec.md`, `plan.md`, `changes.md`, and `testing.md`. Do not drop the Metrics section, the Changes table, or the Validations table. Drop Manual tests when `testing.md` has none, remove its nav link, and say so.

- **Metrics.** One tile per count: commits, files, lines added, lines removed, tests added, passed, failed, skipped, validations passed, validations failed, validation gaps, deviations, open important findings. Each number is the output of a command or a count of rows on this page. `git diff --stat` and `git rev-list --count` against the base give the diff counts. The suite output gives passed, failed, and skipped. Put those commands in `METRIC_COMMANDS`. Delete a tile you cannot measure and name it in chat. Do not round a number and do not invent one.
- **Changes.** One row per task, plus one row per deviation. Triage is `planned`, `deviation`, or `review fix`. A review fix is that deviation's row, not a second row. Set the pill class to `planned`, `deviation`, or `fix`. Spec is the acceptance criterion or validation the change serves, or `none`. Evidence is the task branch, the commit, and the test or command, with its result. Paste the command and the output. A row with spec `none` stays on the page.
- **Validations.** One row per acceptance criterion and per validation in `spec.md`. Result is `pass`, `fail`, or `gap`, and the pill class matches. Evidence is the command and the output, or the test name and its result. Change names the Changes row that covers it. A fail or a gap means step 7 is not finished. Go back and fix it before asking.
- **Manual tests.** One article per manual test in `testing.md`. Name the spec item it validates, the directory, the command or the steps, what pass looks like, who ran it, and the output. The pill is `pass`, `fail`, or `gap`. A manual test that was not run is a gap. A fail or a gap means step 7 is not finished.

Open `summary.html` with `open` and give the path in chat. There is no server.

Ask once, with `AskQuestion`:

- **Commit.** Merge the finished task branches into the integration branch with a **merger subagent**, then go to step 9.
- **Adjust.** They say what to change. Do not merge. Do the adjustment in a fresh implementer on the task branch it belongs to, re-run the validations it touches, rewrite `summary.html`, open it, and ask again.

Silence is not a commit. "Looks fine, commit" is a commit. Apply an adjustment they already named without asking them to repeat it. When they choose Adjust and do not say what to change, ask what to change. Do not commit.

## 9. Finish

Only after they chose Commit in step 8:

1. Open a pull request only when the human asks, from the integration branch. Push that branch first if it is not on the remote. A draft from step 6 is of a task branch. Leave it as a draft. The body has a summary, the plan's tasks, the deviations from `changes.md`, and the testing summary from `testing.md`. Add one line per ticket id (`Closes #N` on GitHub, the issue key on Jira). With no ticket ids, name the spec's source.
2. When they do not ask, do not open one. Leave a draft from step 6 as a draft.
3. When progress is on, post the **Testing summary** note.
4. Remove every implementer worktree.
5. Report the branch, the pull request URL when one exists, and the files under `.agent-docs/implement-spec-<slug>/`.

Stop there. Do not merge the pull request, close a ticket, or run the tracker's close command.

## Progress

Follow "record progress" in the tracker file, formatted the way its Body section says. Leave the description, the status, and the labels as they are. If that section is missing, say so once and continue with no notes. Only this session posts. Implementer, merger, reviewer, and QA subagents do not.

Post on the parent: the source issue, or the parent the input names. With several tickets and no parent, post each note on every ticket it concerns.

`.agent-docs/` is not in the repo, so inline the content. Do not link to local paths.

1. **Plan.** After the integration branch exists. The branch name, the base branch, the size and why, the HLD summary (large only), and the task list from `plan.md` with the acceptance criterion or validation each task covers.
2. **Change.** After each deviation is recorded, from implementation, review, or QA. The source, what changed against the plan, why, and the task it affects. A blocker that needs the human's answer is also a Change note.
3. **Testing summary.** After they chose Commit and step 9 has run. The branch, the pull request URL when one exists, tests added, suites run with results, the QA result per acceptance criterion and per validation, review verdicts, unfixed Minor findings, and known gaps.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "The spec is clear enough, skip validation." | Step 2 runs every time. It is what finds missing context. |
| "It is large, but the design is obvious." | Large needs an approved HLD. Write it with `to-hld` and get the approval. |
| "Push now so people can watch." | Push when a check needs the remote, such as CI. A draft is optional. A ready pull request waits until the human asks, after review. |
| "The pull request is approved, so merge it." | This skill never merges the pull request. The only merge it does is task branches into the integration branch, after they choose Commit. |
| "The work is done, close the ticket." | Never close or transition a ticket here. |
| "The deviation was small, skip the note." | Every deviation goes to `changes.md`, and to the tracker when progress is on. |
| "The task branches already committed, so merge them." | Those commits save the work. The integration branch changes only after they choose Commit. |
| "Show the summary after the merge." | The page is how they choose commit or adjust. The merge follows Commit. |
| "QA passed, skip the page." | Step 8 runs every time. Open the page and wait. |
| "The diff is small, so skip the counts." | The tiles are the counts. Measure them. |
| "QA tried it, so there is no manual test to write down." | A check outside the suite is a manual test. Record the spec item, the steps, and the output. |

## Red flags

Stop if you are about to:

- Write acceptance criteria or validations yourself
- Plan or implement a large change before the human approved the HLD
- Open a ready pull request before review and QA findings are fixed
- Open a ready pull request the human did not ask for
- Merge the pull request, close a ticket, or change a ticket's status, labels, or description
- Post progress with no yes, or after a no
- Post a link to a local `.agent-docs/` path instead of the content
- Let a subagent post to the tracker
- Continue after a deviation that changes an approved HLD decision without asking the human
- Merge into the integration branch, or commit the change onto the branch the human is on, before they choose Commit
- Open the summary with an acceptance criterion or validation missing, or with evidence that is only a claim
- Put a metric on the page that you did not count from a command or from the rows
- Leave a manual test from `testing.md` off the page, or leave the Manual tests section up when there are none
- Treat a task-branch commit as the commit they accepted
- Commit when they chose Adjust, or when they have not answered
