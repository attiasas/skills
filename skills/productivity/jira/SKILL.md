---
name: jira
description: Operates Jira issues for the current repo through the Jira integration already connected in the session. Searches, reads, creates, edits, comments, closes, and records task graphs, blocking links, child issues, estimates, and triage labels. Use when a skill or the user needs to read or write a Jira issue, or names a Jira key or a Jira URL.
---

# Jira

Issues for this repo are Jira issues. Use the Jira integration already connected in this session.

If the id is a GitHub issue number or the URL is a github.com issue, read the `github-issues` skill instead.

When no Jira integration is connected, stop and say so. Do not invent a CLI, a REST call, or a site. Do not use `gh` for issues.

## Which issue

- **Project key.** The letters before the hyphen in a Jira key. `ABC-123` is project `ABC`.
- **Site.** The host on a Jira URL, or the site the connected integration already uses.

Ask when either is still missing. Do not guess an assignee, a priority, an issue type, or a label. A triage label the human approved on the draft is applied under "apply a triage label" below. A triage type is a label, not the Jira issue type.

## Body

Jira wiki markup, not Markdown. A line starting with `#` is a numbered list, so a Markdown heading (`### Background`) renders as a nested `1. a. i.` list.

- `h3.` is a heading
- `#` is one numbered step
- `*` is a bullet
- `*Expected:*` is bold
- `{{name}}` is inline code

Do not file `###`, `**bold**`, or `-` bullets.

## Estimate

The duration goes on the original estimate field, not in the description. Use `30m`, `4h`, `1d`, `1d 2h`, or `1w`. If the project has no such field, or saving it fails, leave the ticket and say the estimate was not saved.

## When a skill says "search for a duplicate"

Search project KEY before showing a draft. A clear duplicate: show it and stop.

## When a skill says "publish to the issue tracker"

Create a Jira issue in project KEY. The description is wiki markup.

## When a skill says "fetch the relevant ticket"

Open that issue in project KEY on SITE. Read the description and the comments.

## When a skill says "fetch the task graph"

Open the issue in project KEY on SITE. Read its comments, its child issues, and each "is blocked by" link. A ticket can start when every blocker is done. An issue with no children is one ticket.

## When a skill says "record a blocking edge"

Add an issue link on the new issue: "is blocked by" each blocker. If that link type is missing, say so. The description's Blocked by section is then the edge.

A ticket can start when every blocker is done.

## When a skill says "attach as a child"

Set the source issue as the parent when this issue type allows a parent. If it does not, say so and put the parent key on the first line of the description. Do not guess an issue type. Do not change the parent's description. Do not close the parent.

## When a skill says "record progress"

Add a comment. Leave the description, the status, and the labels as they are.

## When a skill says "edit the body"

Replace the description. Leave the status and the labels as they are.

## When a skill says "propose triage labels"

Look up labels project KEY already uses. Do not create a label. When the integration cannot list labels, ask which of the candidate names below the project already uses on an issue. Do not invent a name. A label that exists and is unused is not proposed.

The calling skill says whether it wants a type, an entry state, or both.

- **State.** A used label named `needs-triage`, `triage`, or `untriaged`. When more than one of those is used, recommend one and name the other. None used: no State line.
- **Type.** The one used label that names the kind of work the calling skill describes, among `bug`, `defect`, `enhancement`, `feature`, `task`, `documentation`, `docs`, `chore`, `spike`, and `refactor`. When two used labels fit, recommend one and name the other. None used: no Type line.

Do not propose `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`. Return the label string, not a role name. A type is a label, not the Jira issue type.

## When a skill says "apply a triage label"

Set only the Type and State strings on the approved draft. Skip a line that was omitted. Do not create a label. A triage type is a label, not the Jira issue type.
