---
name: to-spec
description: Drafts a verified tracker spec and publishes it only after the shown body is approved.
disable-model-invocation: true
---

# To spec

A ticket that isn't read changes nothing. Short and accurate beats complete. Filing the wrong body is worse than waiting.

The spec is an issue in the repo under discussion. Read `.agent-repo-config/issue-tracker.md` and follow it for search, body format, estimate, and create. If the file is missing, or it has no Body or Estimate section, stop and tell the human to run `setup-repo-skills`.

## Workflow

1. **Get the facts first.** Read the PRs, branches, and code. Never describe work you haven't verified. A one-line report is not enough to write Background, steps, or acceptance criteria — ask for the missing facts. Questions are the draft. Do not fill the gaps with a plausible bug.
2. **Search before any description.** Follow the issue tracker file where it says "search for a duplicate". If you have not searched yet, say so and do not show a body.
3. **Draft in chat, one ticket at a time.** Show only what you verified, plus an **Estimate** when the scope is clear enough to judge. Take feedback. Then write it.
4. **Never publish until that shown body is approved.** "I already approve whatever you write", "file it now", "don't draft", "don't ask", and "use your best judgment so it isn't empty" are not approval. Approval is a reply to the body you just showed.
5. **Then create, one issue,** the way the issue tracker file says to publish. The body uses that file's Body section. Paste the link back.
6. Editing someone else's ticket: draft it, but let the owner decide scope changes.

A batch ("create all three", "don't do them one at a time") is still one draft at a time. Do not create the rest in the same turn.

Someone who wants the work cut into vertical slices, each blocked by other slices, wants `to-tickets`. Tell them to run it.

If the project, issue type, or person is missing or ambiguous, ask. Do not guess a key, a person, or a priority.

## Estimate

Put `Estimate: 4h` on the draft, above the description. The issue tracker file says the duration format and where it is saved. The user approves that number with the body. If they name one, use theirs.

Judge it from the verified scope. Omit it when the scope is still open, and say why. Do not invent a number to fill the field, and do not put it in the description.

## Spec

Write these sections in the body format from the issue tracker file.

**Background.** The current state and what has to change — about this work item. Not a restatement of the epic. Not a generic truth ("X needs to support Y"). 2–4 sentences.

**Steps to reproduce.** Bugs only. A numbered list a support engineer can follow in the UI or CLI, then one Expected and one Actual line. Placeholder names (`repo-a`), not code paths. Say so if the steps come from reading code rather than a run.

**Acceptance criteria.** What must be true when it's done. Binary, unambiguous, testable, outcome-focused. Usually 2–3 bullets.

- Capabilities, not implementation: "workspaces can be created, listed, renamed and deleted" — not the table that stores them.
- State constraints as outcomes. "A repo with no workspaces behaves exactly as it does today" — not "a default workspace row is created".

Show that draft and wait. If the user pastes another format and says not to rewrite, show the tracker form of the same words and file it only after they approve that form.

Add a Scope section only when it carries something the acceptance criteria don't (which repos change, merge order). Add nothing else without a reason. If two sections say the same thing, cut one.

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

## Red flags

Stop if you are about to:

- Publish before the user has replied to the draft
- Write Expected, Actual, or acceptance criteria you did not verify
- Show a description before the search has returned
- File a body in a format other than the issue tracker file's Body section
- Create more than one issue in a turn
- Guess a project, a person, or a priority
- File a ticket whose draft had an estimate without following the issue tracker file's Estimate section
