# Issue tracker: GitHub

Issues for this repo are GitHub issues. Use the `gh` CLI from inside the clone. `gh` infers the repo from `origin`.

## Commands

- Search: `gh issue list --state all --search "..." --json number,title,state`
- Create: `gh issue create --title "..." --body "..."` (use a heredoc for a multi-line body)
- Read: `gh issue view NUMBER --json number,title,body,labels,comments`
- List open: `gh issue list --state open --json number,title,labels`
- Comment: `gh issue comment NUMBER --body "..."`
- Edit the body: `gh issue edit NUMBER --body "..."`
- Close: `gh issue comment NUMBER --body "..."`, then `gh issue close NUMBER`

Do not guess an assignee or a label the user did not name.

## Body

Markdown. `###` is a heading. A numbered list is steps. `-` is a bullet. `**bold**` is bold. `` `name` `` is inline code.

## Estimate

This tracker has no estimate field. Do not put a duration in the body. If a draft showed one, say it was not saved on the issue.

## When a skill says "search for a duplicate"

Run the search command before showing a draft. A clear duplicate: show it and stop.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. The description is Markdown.

## When a skill says "fetch the relevant ticket"

Read it with `gh issue view`.

## When a skill says "record a blocking edge"

Native issue dependency. On create: `gh issue create --blocked-by NUMBER`. After create: `gh issue edit CHILD --add-blocked-by BLOCKER`. Numbers or URLs both work. Repeat for each blocker.

If `gh` does not recognize the flag, say so. The ticket body's Blocked by section is then the edge. Do not invent an API call.

A ticket can start when every blocker is closed.

## When a skill says "attach as a child"

`gh issue create --parent PARENT`, or `gh issue edit CHILD --parent PARENT`.

If `gh` does not recognize the flag, the child body starts with `Part of #PARENT`. Do not invent an API call. Do not change the parent's body. Do not close the parent.
