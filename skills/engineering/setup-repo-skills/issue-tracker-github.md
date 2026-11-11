# Issue tracker: GitHub

Issues for this repo are GitHub issues. Use the `gh` CLI from inside the clone. `gh` infers the repo from `origin`.

## Commands

- Create: `gh issue create --title "..." --body "..."` (use a heredoc for a multi-line body)
- Read: `gh issue view NUMBER --json number,title,body,labels,comments`
- List open: `gh issue list --state open --json number,title,labels`
- Comment: `gh issue comment NUMBER --body "..."`
- Close: `gh issue comment NUMBER --body "..."`, then `gh issue close NUMBER`

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Read it with `gh issue view`.
