---
name: setup-repo-skills
description: Use when preparing a GitHub repo before another engineering skill needs to know where issues live (GitHub issues or Jira).
disable-model-invocation: true
---

# Setup repo skills

Scaffold the per-repo configuration that the engineering skills assume.

- **Issue tracker**: where issues live (GitHub issues or Jira)

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

Invoke it when you want that config ready before another engineering skill reads it. This version has issue tracker only. Later sections get added here as those skills arrive.

The config is local to the repo being set up. Write it under `.agent-repo-config/` and keep that directory gitignored. Do not commit it, and do not copy it into `docs/` or a steering file.

## Process

### 1. Explore

Look at the current repo. Read whatever exists. Don't assume.

- `git remote -v`: is `origin` a GitHub repo? Which one?
- `.agent-repo-config/issue-tracker.md`: does this skill's output already exist?
- `.gitignore`: is `.agent-repo-config/` already ignored?
- A Jira site or project key already written in the repo

If no remote URL contains `github.com`, stop. This version only sets up GitHub repos. Ask for a GitHub `origin`. Write nothing.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead with the recommended answer so the user can accept it in a word. Skip a section when exploration already settled it.

**Section A: Issue tracker.**

> Explainer: The issue tracker is where issues live for this repo. Later engineering skills read `.agent-repo-config/issue-tracker.md` when they create or fetch a ticket. Pick the place you actually track work.

Recommend **GitHub issues** when `origin` is GitHub. The only choices are:

- **GitHub**: issues live in this repo's GitHub Issues (uses the `gh` CLI)
- **Jira**: issues live in a Jira project. If the site host or project key is missing, ask for both. Do not invent a CLI.

Anything else (GitLab, Linear, local markdown) is not a choice in this version. Ask again for GitHub issues or Jira.

### 3. Confirm and edit

Show a draft of:

- `.agent-repo-config/issue-tracker.md`, starting from the seed template
- the `.gitignore` line `.agent-repo-config/`, when it is not already there

Let them edit the draft before writing.

### 4. Write

Write only what they accepted.

- `.agent-repo-config/issue-tracker.md`, from [issue-tracker-github.md](issue-tracker-github.md) or [issue-tracker-jira.md](issue-tracker-jira.md). For Jira, fill the site and project key. If they named a real command or tool, use that in the commands section.
- `.gitignore`: add `.agent-repo-config/` if it is missing. Do not add a second copy of the line.

Leave every other file alone. In particular, do not create `docs/agents/`, and do not edit `AGENTS.md` or `CLAUDE.md`.

### 5. Done

Tell the user the setup is complete and that later engineering skills will read `.agent-repo-config/issue-tracker.md`. They can edit that file directly. Re-run this skill only to switch trackers or start over.
