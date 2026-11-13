---
name: to-tickets
description: Break a plan, spec, or conversation into vertical-slice tickets with blocking edges, and publish them after the breakdown is approved. Applies a mapped triage type and entry state when that map exists.
disable-model-invocation: true
---

# To tickets

Cut the work into vertical slices. Each ticket is one narrow path a person can demo or check, and each ticket names the other tickets that block it. Publish only the breakdown the human has approved.

The tickets are issues in the repo under discussion. Read `.agent-repo-config/issue-tracker.md` and follow it for search, body format, publish, blocking edges, and child issues. If that file is missing, or it has no Body section, stop and tell the human to run `setup-repo-skills`. A file that has no "record a blocking edge" or "attach as a child" section still works: the fallback below covers it. Re-run `setup-repo-skills` when they want those native steps. When `.agent-repo-config/triage-label.md` exists, each slice names its Type and State from that file's Applying labels section, and publish applies those strings. When that file is missing, leave labels off and do not ask. When the tracker file has no "apply a triage label" section, say so, tell the human to re-run `setup-repo-skills`, and publish with no triage label.

One verified spec is `to-spec`. An effort that is still undecided questions is `wayfinder`. Tell the human to run that skill. Do not start it yourself. A wayfinder map is input: an issue titled `Map:`, or a file with Destination and Open. Decisions so far are settled. Each recommendation is the working answer for that question. An open question with no recommendation is still undecided.

## Gather

Work from the conversation. If they pass a path, an issue number, or a URL, read the whole thing, including comments. Fetch an issue the way the tracker file says under "fetch the relevant ticket".

When the work changes code that already exists, read that code and use its words. When it does not, the plan is enough. Leave file paths and implementation choices out of the ticket. A short fragment that records a decision a sentence would blur (a type, a state machine, a schema) may stay: keep the decision, note that it came from a prototype, and drop the rest.

## Slice

Each ticket:

- Crosses every layer that one path needs, and can be demoed or checked on its own.
- Fits in one fresh context window.
- Uses words the plan and the code already use.

A ticket that only prepares one layer, with the rest promised later, is not a slice. A prefactor that makes the other slices possible is its own first ticket.

**Blocked by** lists the tickets that must be done before this one can be checked. An empty list means it can start immediately. An edge is a real gate. If the later ticket can be verified while the earlier one is still open, it is not blocked.

### A change that cannot be a slice

A rename or a retype that every call site has to take in one edit will not stay green as a thin slice. Split that change into three waves:

1. **Add.** Put the new form beside the old one. Existing callers stay on the old form.
2. **Move.** One ticket per batch (one package, or one directory). Each batch is blocked by the add. Each batch can merge, because the old form is still there.
3. **Remove.** Delete the old form once every batch has moved. That ticket is blocked by all of the move tickets.

When a batch cannot merge on its own, the batches share one integration branch. They all block a final ticket that merges that branch and checks it. Only that final ticket has to be green.

## Quiz

Search each title the way the tracker file says under "search for a duplicate" before showing the list. Until that search has returned, do not show the list. A clear duplicate: show the existing issue and leave that slice off the list. The tracker's "stop" applies to that slice only.

Show a numbered list, blockers first. For each ticket:

- **Title**
- **Type**: the Tracker label from `.agent-repo-config/triage-label.md` for the one type row that fits, when that file maps one. Omit the line when the file is missing or the cell is empty.
- **State**: the `needs-triage` Tracker label, when that cell is filled. Omit the line otherwise.
- **Blocked by**: numbers from this list, or none
- **What to build**: the end-to-end behaviour, in one or two sentences
- **Acceptance criteria**: two or three checkable outcomes

Ask whether the size is right, whether each edge is a real gate, and whether any ticket should be merged or split. Apply the edit and show the list again.

Publish the list they replied to. "I already approve whatever you write", "file them now", or "use your best judgment", said before that list was shown, is not approval. A reply to the list you just showed is approval. Change a title, an edge, a criterion, a type, or a state after that reply, and show the list again.

## Publish

Search again when a title changed since the last search. Then create one issue per approved ticket, blockers first, so each edge can name a real id. Follow "publish to the issue tracker". The body is the approved "What to build" and acceptance criteria, in the tracker file's Body format.

- **Blocked by.** Follow "record a blocking edge" when that section exists, and leave this section out of the body. When the section is missing, or the native edge fails, include it: the blocking issues, or "None (can start immediately)". Say so when a native edge was not saved.
- **Parent.** Only when the source was an existing issue. Follow "attach as a child" when that section exists. When it is missing, or the attach fails, name the parent on the first line of the body and say the child link was not saved. Leave the parent open. Leave its body as it was.

Apply the approved Type and State the way the tracker file says under "apply a triage label". Add nothing else the approved list did not contain: no other label, no assignee, no estimate, no path, and no extra criterion. Do not set `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`.

Paste the links back. Name the tickets that can start now (every blocker done). On a straight chain, that is the first ticket. Stop. Implement only when the human asks.

## Don't

- Don't file the set as one issue.
- Don't file one layer at a time (schema, then API, then UI), except the add / move / remove sequence above.
- Don't publish a breakdown the human has not replied to.
- Don't close or rewrite a parent issue.
- Don't guess a project, a person, a priority, or a label string. The Type and State on the approved list are the labels publish applies.

## Red flags

Stop if you are about to:

- Create an issue before the human has replied to this breakdown
- Create more than the approved list, or fold two approved tickets into one issue
- Treat a preferred order as a blocking edge
- Force a whole-codebase rename or retype into one slice
- Add acceptance criteria after approval
- Edit or close the parent
- Apply a triage label that was not on the shown list
- Apply a triage state other than `needs-triage`
