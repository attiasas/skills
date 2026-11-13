---
name: implement-spec
description: Use when implementing a spec from an issue or an assess handover, including when a run would close those tickets before a pull request is merged.
disable-model-invocation: true
---

# Implement spec

Implement the whole spec on a single **integration branch**, then open a pull request. Tickets stay open until that pull request merges. Do not close a ticket in this session.

The tickets are a **task graph** with blocking edges. There is always a **frontier**: tickets whose blockers are already done.

Start every subagent with a fresh context window. Run **implementer subagents** in the background where possible.

Talk to subagents through pointers: the spec, the tickets, research notes, and earlier commits. Leave out text those pointers already hold.

## Input

The input is an issue (number, key, or URL) or a path to an assess `handover.md`.

- **Issue.** Read `.agent-repo-config/issue-tracker.md`. If that file is missing, stop and tell the human to run `setup-repo-skills`. Follow "fetch the task graph". Child issues are the tickets. Blocking edges decide the frontier. An issue with no children is one ticket: itself.
- **Handover.** That file is the spec. Issue ids named in it are the tickets. A parent id named in it is the parent. When it names no issue and describes one slice, the file is the only ticket and there is no graph. A handover with no issue ids does not need the tracker file.

Leave ticket creation to `to-tickets`. A multi-slice change that has no tickets yet goes back to the human to run that skill.

## Progress

Before step 3, ask once whether to record progress on the tracker. Ask only when at least one issue id is in hand. With no ids, skip the question and write nothing to a tracker.

A yes covers the whole run. Post each note below without showing it first. A no means no progress comments.

Follow "record progress". Leave the description, the status, and the labels as they are. If that section is missing, say so once and continue with no comments. Progress comments are not a close, and they do not change status.

This session posts the notes. Implementer and merger subagents do not.

The parent is the source issue, or the parent named in the handover. A lone issue is its own parent. With several tickets and no parent, post merge notes on each ticket, and keep the started and review notes in the chat.

1. **Started.** After the integration branch exists. On the parent: `Started on <branch>.`
2. **Merged.** After each merge onto that branch. On that ticket: `Landed on <branch> at <sha>.` When the parent is a different issue, also comment there: `Landed <ticket> on <branch> at <sha>. Ready now: <ids, or none>.`
3. **Review fixes landed.** After a code-review fix-up merges. On the parent: `Review fixes landed on <branch> at <sha>.` When the review finds nothing to fix, skip this note.

## Steps

1. Read the spec and the tickets and build the task graph.

2. (optional) Use an **exploration subagent** for codebase or external reading the tickets depend on. It saves markdown notes in a directory outside the repo, where later subagents can read them.

3. Create the integration branch. When progress is on, post **Started**.

4. Use a fresh **implementer subagent** for each frontier ticket, each in its own worktree on its own branch. Each implementer:
   - confirms its worktree is based on the integration branch before starting, and resets onto it when it is not;
   - calls the `tdd` skill to build the ticket;
   - merges the integration branch tip into its own branch before reporting done.

5. When an **implementer subagent** finishes, merge its branch into the integration branch with a **merger subagent**. When progress is on, post **Merged**. After the first merge, push the integration branch and open a draft pull request. A branch with no commits ahead of the base cannot open one. The body has one closing line per ticket id (`Closes #N` on GitHub) so the host closes those tickets when the pull request merges. With no ticket ids, the body names the spec path and closes nothing. Open that pull request even when the human did not ask, and even when the tracker file only documents a close command.

6. When that merge opens new frontier tickets, start **implementer subagents** for them.

7. When every ticket is done, call the `code-review` skill with two arguments: the fixed point is the base branch the integration branch was cut from, and the spec is the issue number or the `handover.md` path from Input. Pass the spec explicitly, so `code-review` does not depend on commit messages. Fix what it raises in one fresh **implementer subagent**, then merge that fix to the integration branch. When progress is on, post **Review fixes landed**.

8. Mark the draft pull request ready for review. Leave every ticket open. Report the pull request URL. Do not run the tracker's close command. Merging the pull request is what closes the tickets.

9. Remove every **implementer subagent** worktree.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "No draft PR exists, so step 8 closes the tickets." | Step 5 opens the pull request. Step 8 only marks it ready. |
| "The human did not ask for a pull request." | The pull request is how this run finishes. |
| "The tracker file only shows a close command." | Do not run it. The pull request body closes the tickets on merge. |
| "Closing is allowed once step 8 is reached." | This session never closes a ticket. |
| "Nothing is pushed, so report the branch and stop." | Push, then open the pull request. |

## Red flags

Stop if you are about to:

- Create a ticket
- Start from `design.md` when a `handover.md` was given
- Record progress with no yes, or after a no
- Edit an issue body, transition it, or apply a label as a progress note
- Close a ticket in this session, including at step 8
- Finish on a local branch with no pull request
- Skip the push because the human did not ask
