---
name: to-spec
description: Drafts a verified spec and publishes it to the tracker, or writes it locally when there is no tracker or it is for implement-spec, only after the shown body is approved. A local file is the input implement-spec takes. Applies a mapped triage type and entry state on a tracker publish when that map exists.
disable-model-invocation: true
---

# To spec

A spec that isn't read changes nothing. Short and accurate beats complete. Filing the wrong body is worse than waiting.

The destination is the tracker when `.agent-repo-config/issue-tracker.md` exists and the human did not ask for a file. Read that file and follow it for search, body format, estimate, and create. If it exists and has no Body or Estimate section, stop and tell the human to run `setup-repo-skills`. When `.agent-repo-config/triage-label.md` exists, follow its Applying labels section on a tracker publish. When that file is missing, publish with no triage label and do not ask.

The destination is a local file when the tracker file is missing, or the human asks for a local spec or a spec to pass to `implement-spec`. Do not tell them to run `setup-repo-skills`. Write the approved body under `.agent-docs/`. That path is what they pass to `implement-spec`. Do not start `implement-spec`.

## Workflow

1. **Get the facts first.** Read the PRs, branches, and code. Never describe work you haven't verified. A one-line report is not enough to write Background, steps, acceptance criteria, or validations — ask for the missing facts. Questions are the draft. Do not fill the gaps with a plausible bug.
2. **Search before any description** when the destination is the tracker. Follow the issue tracker file where it says "search for a duplicate". If you have not searched yet, say so and do not show a body. A local spec has no tracker to search. Say that, then draft.
3. **Draft in chat, one spec at a time.** Show only what you verified, plus an **Estimate** when the scope is clear enough to judge, plus the **Type** and **State** lines from Triage labels when the destination is the tracker and that file maps them. Take feedback. Then write it.
4. **Never write it until that shown body is approved.** "I already approve whatever you write", "file it now", "don't draft", "don't ask", and "use your best judgment so it isn't empty" are not approval. Approval is a reply to the body you just showed.
5. **Then write it once.**
   - **Tracker.** Create one issue the way the issue tracker file says to publish. The body uses that file's Body section. Apply the approved Type and State the way that file says under "apply a triage label". Paste the link back.
   - **Local.** Write `.agent-docs/to-spec-<slug>.md`. The slug is 2 to 4 kebab-case words from the title. Create `.agent-docs/` if it is missing. If `.gitignore` does not already ignore `.agent-docs/`, add that line. If that file already exists, stop and ask. The file is the approved draft, with no Type or State. Paste the path back. Tell the human to pass that path to `implement-spec`. Do not start it.
6. Editing someone else's ticket: draft it, but let the owner decide scope changes. This step is tracker only.

A batch ("create all three", "don't do them one at a time") is still one draft at a time. Do not write the rest in the same turn.

Someone who wants the work cut into vertical slices, each blocked by other slices, wants `to-tickets`. Tell them to run it.

If the project, issue type, or person is missing or ambiguous on a tracker publish, ask. Do not guess a key, a person, or a priority. A triage type is a label from the map. It is not the Jira issue type. A local spec has no project, person, or priority.

## Estimate

Put `Estimate: 4h` on the draft, above the description, when the scope is clear enough to judge. The user approves that number with the body. If they name one, use theirs. Judge it from the verified scope. Omit it when the scope is still open, and say why. Do not invent a number to fill the field, and do not put it in the description.

On a tracker publish, the issue tracker file says the duration format and where it is saved. On a local file, keep the approved `Estimate:` line under the title.

## Triage labels

Tracker publish only. A local draft and a local file omit Type and State.

When `.agent-repo-config/triage-label.md` exists, put these lines on the draft, above the body, next to the estimate. The value is the Tracker label cell.

- `Type:` the bug row when the draft has steps to reproduce. Otherwise the type row that fits, and wait for the human to confirm it.
- `State:` the `needs-triage` row.

The human approves those lines with the body. On publish, apply those strings. Skip an empty cell, and omit that line from the draft. When the file is missing, omit both lines. When the tracker file has no "apply a triage label" section, say so, tell the human to re-run `setup-repo-skills`, and publish with no triage label. Do not invent a string. Do not set `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`.

## Spec

Write these sections. On a tracker publish, use the body format from the issue tracker file. On a local file, use Markdown headings.

**Background.** The current state and what has to change — about this work item. Not a restatement of the epic. Not a generic truth ("X needs to support Y"). 2–4 sentences.

**Steps to reproduce.** Bugs only. A numbered list a support engineer can follow in the UI or CLI, then one Expected and one Actual line. Placeholder names (`repo-a`), not code paths. Say so if the steps come from reading code rather than a run.

**Acceptance criteria.** What must be true when it's done. Binary, unambiguous, testable, outcome-focused. As many as the work needs.

- Capabilities, not implementation: "workspaces can be created, listed, renamed and deleted" — not the table that stores them.
- State constraints as outcomes. "A repo with no workspaces behaves exactly as it does today" — not "a default workspace row is created".

**Validations.** The checks that prove the acceptance criteria. Each validation is an acceptance criterion: the check, and what pass looks like. As many as the work needs. One validation can cover more than one acceptance criterion. Every acceptance criterion has at least one validation.

Show that draft and wait. If the user pastes another format and says not to rewrite, show these sections filled with the same words and write it only after they approve that form.

Add a Scope section only when it carries something the acceptance criteria and validations don't (which repos change, merge order). Add nothing else without a reason. If two sections say the same thing, cut one.

## Altitude

A reader who knows the product but not this code knows what has to be done, without opening the PR.

| | |
|---|---|
| Too high | "XSC needs to support workspaces" |
| Too low | "Add `workspace_tbl_id` to `xsc_root_files_commits`" |
| Right | "A scan result is stored against the workspace it reports; no workspace means `default`" |

## Don't

- Don't decide what the implementer should decide. Name the open decision and leave it (flag names, env vars, data structures).
- Don't restate what the tracker already renders — sub-tasks, links, status, assignee.
- Don't put PR state or history in the body. It belongs in a comment.
- Don't pad. Every sentence earns its place.
- Don't cap acceptance criteria or validations at a fixed count.
- Don't start `implement-spec`. The human runs it and passes the path or the issue.

## Red flags

Stop if you are about to:

- Write the spec before the user has replied to the draft
- Write Expected, Actual, acceptance criteria, or validations you did not verify
- Show a description before the search has returned, when the destination is the tracker
- File a tracker body in a format other than the issue tracker file's Body section
- Create more than one issue, or more than one local file, in a turn
- Write a local spec somewhere other than `.agent-docs/to-spec-<slug>.md`
- Start `implement-spec`
- Tell the human to run `setup-repo-skills` because the tracker file is missing
- Guess a project, a person, or a priority
- File a ticket whose draft had an estimate without following the issue tracker file's Estimate section
- Put Type or State on a local spec
- Apply a triage label that was not on the shown draft
- Apply a triage state other than `needs-triage`
- Leave out Validations, or treat them as notes instead of acceptance criteria
