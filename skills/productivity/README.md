# Productivity

Skills for non-code work.

## User-invoked

Reachable only when you type the skill name (`disable-model-invocation: true`).

- **[agent-doctor](./agent-doctor/SKILL.md)**: Check this machine's and workspace's Cursor setup (CLI, rules, skills, MCP, hooks, permissions), and mine recent chats for repeated corrections, jobs, and time sinks worth turning into rules, skills, or subagents. Read-only. Writes one HTML page and a numbered fix list, and applies a fix only after its number is confirmed.

## Model-invoked

Reachable by you or by the agent when the task fits.

- **[github-issues](./github-issues/SKILL.md)**: Operate GitHub issues for the current repo with the `gh` CLI: search, read, create, edit, comment, close, task graphs, blocking edges, child issues, estimates, and triage labels. Load when a skill or the user needs a GitHub issue.
- **[jira](./jira/SKILL.md)**: Operate Jira issues for the current repo through the Jira integration already connected in the session: search, read, create, edit, comment, close, task graphs, blocking links, child issues, estimates, and triage labels. Load when a skill or the user needs a Jira issue.
