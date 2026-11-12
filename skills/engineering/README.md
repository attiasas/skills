# Engineering

Skills for code work.

## User-invoked

Reachable only when you type the skill name (`disable-model-invocation: true`).

- **[setup-repo-skills](./setup-repo-skills/SKILL.md)**: Write a gitignored `.agent-repo-config` for a GitHub repo (GitHub issues or Jira), and gitignore `.agent-research/`. Run before another engineering skill needs the issue tracker.
- **[to-spec](./to-spec/SKILL.md)**: Drafts a verified tracker spec and publishes it only after the shown body is approved.
- **[to-tickets](./to-tickets/SKILL.md)**: Break a plan, spec, or conversation into vertical-slice tickets with blocking edges, and publish them after the breakdown is approved.
- **[wayfinder](./wayfinder/SKILL.md)**: Chart a large, foggy effort as decision tickets on the repo issue tracker, and settle one decision per session until the route is clear enough to implement.

## Model-invoked

Reachable by you or by the agent when the task fits.

- **[research](./research/SKILL.md)**: Investigate a question against primary sources and write the findings under `.agent-research/`.
- **[to-hld](./to-hld/SKILL.md)**: Produce a high-level design (HLD) file using the seven-section engineering design-review template.
