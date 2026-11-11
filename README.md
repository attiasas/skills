# Skills

Personal agent skills for me and my agents.

Skills are small, composable instructions an agent can follow. This repo is the source of truth. Harness skill directories hold symlinks back here, so a pull updates what the agents see.

Layout follows the bucket idea in [mattpocock/skills](https://github.com/mattpocock/skills): group skills by the kind of work, and keep each skill in its own directory.

## Buckets

| Path | What belongs here |
| --- | --- |
| `skills/engineering/` | Code work: implementation, review, debugging, design, repo workflow |
| `skills/productivity/` | Non-code work: writing, planning, communication, personal workflow |

Each bucket has a `README.md` that lists its skills. Update that list when you add, rename, or remove one.

## Skill directory

A skill is a directory with a `SKILL.md`. The directory name is the skill name, and it must be unique across the whole repo (the installer links by that name).

```
skills/engineering/review-pr/
├── SKILL.md          # required
├── references/       # optional, read only when the skill points at them
└── scripts/          # optional utilities the skill runs
```

`SKILL.md` starts with YAML frontmatter:

```markdown
---
name: review-pr
description: Review a pull request against this repo's standards. Use when the user asks for a PR review or code review.
---
```

User-invoked skills (slash-command only) also set `disable-model-invocation: true`. Leave that out when the agent should be able to reach for the skill on its own. See `AGENTS.md` for the rules this repo follows when adding a skill.

## Install

Link every skill into the local agent directories:

```bash
./scripts/link-skills.sh
```

Destinations:

- `~/.cursor/skills` for Cursor
- `~/.agents/skills` for other Agent Skills harnesses

Each entry is a symlink into this repo. Re-run the script after adding, renaming, or removing a skill. The script will not replace a real directory that is already at the destination.

## Add a skill

1. Pick a bucket.
2. Create `skills/<bucket>/<skill-name>/SKILL.md`.
3. Add a one-line entry to that bucket's `README.md`, under **User-invoked** or **Model-invoked**.
4. Run `./scripts/link-skills.sh`.
