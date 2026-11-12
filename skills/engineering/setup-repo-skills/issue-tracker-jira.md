# Issue tracker: Jira

Issues for this repo are Jira issues.

- Site: SITE
- Project key: KEY

## Commands

Search, create, read, and close issues in project KEY on SITE through the Jira UI.

Do not use `gh` for issues. Do not invent a CLI. If the user names a specific command or tool, replace this section with those steps.

Do not guess the project key, an assignee, or a priority. Ask when any of those is missing.

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

Open that issue in project KEY on SITE.

## When a skill says "record a blocking edge"

In the Jira UI, add an issue link on the new issue: "is blocked by" each blocker. If that link type is missing, say so. The description's Blocked by section is then the edge. Do not invent a CLI.

A ticket can start when every blocker is done.

## When a skill says "attach as a child"

Set the source issue as the parent in the Jira UI when this issue type allows a parent. If it does not, say so and put the parent key on the first line of the description. Do not guess an issue type. Do not change the parent's description. Do not close the parent.
