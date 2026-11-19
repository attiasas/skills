---
name: agent-doctor
description: Check this machine's and workspace's Cursor setup (CLI, rules, skills, MCP, hooks, permissions), and mine recent chats for repeated corrections, jobs, and time sinks worth turning into rules, skills, or subagents. Read-only. Writes one HTML page and a numbered fix list, and applies a fix only after its number is confirmed.
disable-model-invocation: true
---

# Agent doctor

Two passes over how the agent is set up and used here. **Checkup** inspects the setup. **Mine** reads past chats. Run both unless the human names one.

Arguments, all optional: `checkup` or `mine`, a day window (default 30), and a line about the human (team, role, areas). When the about line is missing, infer the areas from the paths in `git log --author="$(git config user.email)"` and say that you inferred them. Do not ask.

## Ground rules

- Read-only. Do not edit, delete, install, update, or rewrite any file until the human replies with a fix number. The only writes are under `.agent-docs/agent-doctor/`.
- Before the first write, add `.agent-docs/` to `.git/info/exclude` when no ignore rule already covers it. Do not touch `.gitignore`.
- Work from the filesystem and the CLI. A check you cannot run is reported as not run, with the reason. Do not guess a result.
- Never print a secret, token, env value, or customer data. Say only whether a required value is set.

## 1. Checkup

Follow [checkup.md](checkup.md). Classify every check as OK, Warn, or Fail:

- **Fail:** broken now. Unparseable config, MCP server down, missing hook script, not signed in.
- **Warn:** works, but worth changing. Name the file or command.
- **OK:** passed. One line each.

## 2. Mine

Follow [mine.md](mine.md). Copy every database before reading it. Never open a live `state.vscdb`.

When no chats can be found or read, say so and which paths you tried. Then mine `git log --author="$(git config user.email)" --since="<N> days ago" -p` and any pull-request review comments you can reach.

## 3. Report

Write `.agent-docs/agent-doctor/report.html`, following [report-example.html](report-example.html). Do not edit the example. Self-contained, no external assets. Length is whatever the findings need. Each section is a collapsible block, open to start, with the section name and a count in the summary.

Each item is something to know: the fact, then the evidence. Add a numbered to-do only when there is a concrete change, and say "just know" when there is not. Number to-dos T1, T2, … across the whole page. The opening "this week" list is the three to-dos that pay off first, linking to the items they come from. It is not a second set of findings.

Open it with `open`. There is no server.

Then, in chat, the same to-dos by number: what you would change, why, and the exact file. Stop and wait. Apply only the numbers the human replies with, one at a time, and show the diff after each.

## Never

- Write outside `.agent-docs/agent-doctor/` before a fix number is confirmed
- Read a live `state.vscdb` instead of a copy
- Run a hook script, update the CLI, or call an MCP tool other than a list or status call
- Report a check as OK when it did not run
- Quote a secret, a token, an env value, or customer data, even inside an example
- Apply a fix the human did not name by number
