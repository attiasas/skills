---
name: implement-spec
description: Implement any spec (issue, file, or conversation). Validates and sizes it, requires an approved HLD for large changes, plans, implements with subagents, then reviews. Pushes when a check needs it, and opens a pull request when asked. Never merges or closes tickets. Optionally records the plan, changes, and testing on the tracker.
disable-model-invocation: true
---

# Implement spec

Take a spec from validation through review. The run ends on the integration branch, with the testing summary written. Open a pull request when the human asks. Do not merge it, close a ticket, or move a ticket's status in this session.

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

- **Valid.** It states a goal and acceptance criteria that a test can check. When there are no acceptance criteria, stop and tell the human to run `to-spec`. Do not write them yourself.
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

When `plan.md` was provided, check that every acceptance criterion maps to a task and that it agrees with `hld.md`. Fix the gaps and say what you changed.

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
3. Merge each finished branch into the integration branch with a **merger subagent**. Dispatch implementers for any tasks the merge unblocks.
4. Add every deviation to `changes.md` with its source (implementation, review, QA), what changed, and why. Update `plan.md` to match. When progress is on, post a **Change** note. When a deviation changes the approved HLD's decisions, stop and ask the human before continuing.

Push the integration branch when a check needs the remote, such as CI or a test suite that runs only there. Say why you are pushing. A draft pull request is allowed for the same reason, and not required. Do not mark a draft ready in this step, and do not open a pull request for any other reason.

## 7. Review and QA

When every task is merged, review the integration branch against the base branch:

- **Code review.** Always. Call the `code-review` skill with the base branch as the fixed point and `spec.md` as the spec.
- **Expert review.** When the diff touches a lens that a generalist reviewer would miss, such as security, data migration, concurrency, performance, or a public contract. Dispatch one reviewer subagent per lens with the diff range, `spec.md`, and `hld.md`.
- **QA.** When the spec has behaviour a user or caller can observe. Dispatch a QA subagent that checks each acceptance criterion end to end, beyond the unit tests: run the app, the CLI, or the integration suite. It reports pass or fail per criterion, with the command and the output.

Wait for every reviewer you dispatched. Fix Critical and Important findings and QA failures in a fresh **implementer subagent**, then merge. Each fix that changes behaviour or the plan is a deviation (step 6.4). Re-run the reviews that raised findings until none is Critical or Important. Write Minor findings you did not fix into `testing.md`.

Write `testing.md`: tests added, suites run and their results, the QA result per acceptance criterion, the review verdicts, and any known gaps.

## 8. Finish

Only after step 7 has no open Critical or Important finding:

1. Open a pull request only when the human asks. Push first if the branch is not on the remote. If a draft from step 6 exists, mark that one ready instead of opening a second. The body has a summary, the plan's tasks, the deviations from `changes.md`, and the testing summary from `testing.md`. Add one line per ticket id (`Closes #N` on GitHub, the issue key on Jira). With no ticket ids, name the spec's source.
2. When they do not ask, do not open one. Leave a draft from step 6 as a draft.
3. When progress is on, post the **Testing summary** note.
4. Remove every implementer worktree.
5. Report the branch, the pull request URL when one exists, and the files under `.agent-docs/implement-spec-<slug>/`.

Stop there. Do not merge the pull request, close a ticket, or run the tracker's close command.

## Progress

Follow "record progress" in the tracker file, formatted the way its Body section says. Leave the description, the status, and the labels as they are. If that section is missing, say so once and continue with no notes. Only this session posts. Implementer, merger, reviewer, and QA subagents do not.

Post on the parent: the source issue, or the parent the input names. With several tickets and no parent, post each note on every ticket it concerns.

`.agent-docs/` is not in the repo, so inline the content. Do not link to local paths.

1. **Plan.** After the integration branch exists. The branch name, the base branch, the size and why, the HLD summary (large only), and the task list from `plan.md` with the acceptance criterion each task covers.
2. **Change.** After each deviation is recorded, from implementation, review, or QA. The source, what changed against the plan, why, and the task it affects. A blocker that needs the human's answer is also a Change note.
3. **Testing summary.** After review and QA are done. The branch, the pull request URL when one exists, tests added, suites run with results, the QA result per acceptance criterion, review verdicts, unfixed Minor findings, and known gaps.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "The spec is clear enough, skip validation." | Step 2 runs every time. It is what finds missing context. |
| "It is large, but the design is obvious." | Large needs an approved HLD. Write it with `to-hld` and get the approval. |
| "Push now so people can watch." | Push when a check needs the remote, such as CI. A draft is optional. A ready pull request waits until the human asks, after review. |
| "The pull request is approved, so merge it." | This skill never merges. |
| "The work is done, close the ticket." | Never close or transition a ticket here. |
| "The deviation was small, skip the note." | Every deviation goes to `changes.md`, and to the tracker when progress is on. |

## Red flags

Stop if you are about to:

- Write acceptance criteria yourself
- Plan or implement a large change before the human approved the HLD
- Open a ready pull request before review and QA findings are fixed
- Open a ready pull request the human did not ask for
- Merge the pull request, close a ticket, or change a ticket's status, labels, or description
- Post progress with no yes, or after a no
- Post a link to a local `.agent-docs/` path instead of the content
- Let a subagent post to the tracker
- Continue after a deviation that changes an approved HLD decision without asking the human
