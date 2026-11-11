# Agent notes

This repo holds personal skills. Edit skills here, then link them with `scripts/link-skills.sh`. Do not author skills directly under `~/.cursor/skills` or `~/.agents/skills`. Those directories are install targets.

## Where a skill goes

- `skills/engineering/`: daily code work
- `skills/productivity/`: daily non-code work

The skill directory name is the install name. It must be unique across both buckets, lowercase, hyphens only, 64 characters or fewer.

## SKILL.md

Required frontmatter:

```yaml
---
name: skill-name
description: What it does and when to use it.
---
```

- `description` is third person, states what the skill does and when to reach for it, and stays under 1024 characters.
- User-invoked: add `disable-model-invocation: true`. The description is a one-line summary for a person browsing commands. No "Use when the user says…" trigger list.
- Model-invoked: omit `disable-model-invocation`. Keep the trigger phrasing so the agent can select the skill.
- A user-invoked skill may tell the agent to call a model-invoked skill. It must not tell the agent to call another user-invoked skill. Tell the human to run that one.
- Keep `SKILL.md` short. Put long reference material in a sibling file and link it from `SKILL.md` (one level deep).
- The agent already knows general practice. Write only the steps, constraints, and formats it would not infer.

## When a skill changes

- Add, update, or remove the one-line entry in the bucket `README.md`. Link the name to `SKILL.md`.
- Group promoted skills as **User-invoked** or **Model-invoked**, matching the frontmatter.
- Re-run `scripts/link-skills.sh` after a rename or a new directory.

## Out of scope for this repo

Do not copy another author's skill text into here. Write original instructions, even when the workflow idea came from somewhere else.
