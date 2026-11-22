---
name: github-issues
description: Operates GitHub issues for the current repo with the gh CLI. Searches, reads, creates, edits, comments, closes, and records task graphs, blocking edges, child issues, estimates, and triage labels. Use when a skill or the user needs to read or write a GitHub issue, or names a GitHub issue number or a github.com issue URL.
---

# GitHub issues

Issues for this repo are GitHub issues. Use the `gh` CLI from inside the clone. `gh` infers the repo from `origin`.

If the id is a Jira key (`ABC-123`) or the URL is a Jira URL, read the `jira` skill instead.

If `origin` is not a GitHub repo, say so and stop. Do not guess another host.

## Commands

- Search: `gh issue list --state all --search "..." --json number,title,state`
- Create: `gh issue create --title "..." --body "..."` (use a heredoc for a multi-line body)
- Read: `gh issue view NUMBER --json number,title,body,labels,comments`
- List open: `gh issue list --state open --json number,title,labels`
- Comment: `gh issue comment NUMBER --body "..."`
- Edit the body: `gh issue edit NUMBER --body "..."`
- Close: `gh issue comment NUMBER --body "..."`, then `gh issue close NUMBER`

Do not guess an assignee or a label the user did not name. A triage label the human approved on the draft is applied under "apply a triage label" below.

## Body

Markdown. `###` is a heading. A numbered list is steps. `-` is a bullet. `**bold**` is bold. `` `name` `` is inline code.

## Estimate

This tracker has no estimate field. Do not put a duration in the body. If a draft showed one, say it was not saved on the issue.

## When a skill says "search for a duplicate"

Run the search command before showing a draft. A clear duplicate: show it and stop.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. The description is Markdown.

## When a skill says "fetch the relevant ticket"

Read it with `gh issue view`, comments included.

## When a skill says "fetch the task graph"

Read the issue with `gh issue view NUMBER --json number,title,state,body,comments,parent,subIssues,blockedBy,blocking`.

`subIssues` are the child tickets. `blockedBy` are the blockers. A ticket can start when every blocker is closed. When a blocker's state is missing from that payload, fetch it with "fetch the relevant ticket". An issue with no `subIssues` is one ticket.

If `gh` does not recognize a field, say so. Use a `Part of #PARENT` line and a Blocked by section in the bodies. Do not invent an API call.

## When a skill says "record a blocking edge"

Native issue dependency. On create: `gh issue create --blocked-by NUMBER`. After create: `gh issue edit CHILD --add-blocked-by BLOCKER`. Numbers or URLs both work. Repeat for each blocker.

If `gh` does not recognize the flag, say so. The ticket body's Blocked by section is then the edge. Do not invent an API call.

A ticket can start when every blocker is closed.

## When a skill says "attach as a child"

`gh issue create --parent PARENT`, or `gh issue edit CHILD --parent PARENT`.

If `gh` does not recognize the flag, the child body starts with `Part of #PARENT`. Do not invent an API call. Do not change the parent's body. Do not close the parent.

## When a skill says "record progress"

Comment with `gh issue comment NUMBER --body "..."`. Leave the body, the state, and the labels as they are.

## When a skill says "edit the body"

`gh issue edit NUMBER --body "..."`. Leave the state and the labels as they are.

## When a skill says "propose triage labels"

Look up labels this repo already uses. Do not create a label.

1. `gh label list --limit 100 --json name`
2. For each candidate below that appears in that list, `gh issue list --state all --limit 1 --label "NAME" --json number`. A result means the label is used. No result means it is defined and unused. Do not propose an unused label.

The calling skill says whether it wants a type, an entry state, or both.

- **State.** A used label named `needs-triage`, `triage`, or `untriaged`. When more than one of those is used, recommend one and name the other. None used: no State line.
- **Type.** The one used label that names the kind of work the calling skill describes, among `bug`, `defect`, `enhancement`, `feature`, `task`, `documentation`, `docs`, `chore`, `spike`, and `refactor`. When two used labels fit, recommend one and name the other. None used: no Type line.

Do not propose `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`. Return the label string, not a role name.

## When a skill says "apply a triage label"

Add only the Type and State strings on the approved draft. Skip a line that was omitted. On create, repeat `--label "name"` once per string. On an existing issue, `gh issue edit NUMBER --add-label "name"`.

Do not create a label. Quote a name that contains spaces.
