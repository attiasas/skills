---
name: setup-repo-skills
description: Prepare a GitHub repo's issue tracker config (GitHub issues or Jira) and gitignore `.agent-research/`.
disable-model-invocation: true
---

# Setup repo skills

Scaffold the per-repo configuration that the engineering skills assume.

- **Issue tracker**: where issues live (GitHub issues or Jira), how to search, how a body is written, where an estimate goes, how a blocking edge is recorded, and how a child issue is attached
- **Research notes**: `.agent-research/` is where `research` writes its findings. Gitignore that directory. Do not create it here.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

Invoke it when you want that config ready before another engineering skill reads it. `to-spec`, `wayfinder`, and `to-tickets` read `.agent-repo-config/issue-tracker.md`. `research` writes under `.agent-research/`.

The config is local to the repo being set up. Write it under `.agent-repo-config/` and keep that directory gitignored. Keep `.agent-research/` gitignored too. Do not commit either, and do not copy them into `docs/` or a steering file.

## Process

### 1. Explore

Look at the current repo. Read whatever exists. Don't assume.

- `git remote -v`: is `origin` a GitHub repo? Which one?
- `.agent-repo-config/issue-tracker.md`: does this skill's output already exist? If it does, note any seed section it lacks (Body, Estimate, search, blocking edge, child issue).
- `.gitignore`: are `.agent-repo-config/` and `.agent-research/` already ignored?
- A Jira site or project key already written in the repo

If no remote URL contains `github.com`, stop. This version only sets up GitHub repos. Ask for a GitHub `origin`. Write nothing.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead with the recommended answer so the user can accept it in a word. Skip a section when exploration already settled it. When the file exists and only lacks newer seed sections, offer to add those sections and leave the rest of the file as it is.

**Section A: Issue tracker.**

> Explainer: The issue tracker is where issues live for this repo. Later engineering skills read `.agent-repo-config/issue-tracker.md` when they create, fetch, block, or attach a ticket. Pick the place you actually track work.

Recommend **GitHub issues** when `origin` is GitHub. The only choices are:

- **GitHub**: issues live in this repo's GitHub Issues (uses the `gh` CLI)
- **Jira**: issues live in a Jira project. If the site host or project key is missing, ask for both. Do not invent a CLI.

Anything else (GitLab, Linear, local markdown) is not a choice in this version. Ask again for GitHub issues or Jira.

### 3. Confirm and edit

Show a draft of:

- `.agent-repo-config/issue-tracker.md`, starting from the seed template
- the `.gitignore` lines `.agent-repo-config/` and `.agent-research/`, when they are not already there

Let them edit the draft before writing.

### 4. Write

Write only what they accepted.

- `.agent-repo-config/issue-tracker.md`, from [issue-tracker-github.md](issue-tracker-github.md) or [issue-tracker-jira.md](issue-tracker-jira.md). For Jira, fill the site and project key. Keep the Body, Estimate, search, blocking-edge, and child-issue notes from the seed. If they named a real command or tool, use that in the Commands section and leave the other sections as accepted.
- `.gitignore`: add `.agent-repo-config/` if it is missing. Add `.agent-research/` if it is missing. Do not add a second copy of either line.

Leave every other file alone. In particular, do not create `docs/agents/`, and do not edit `AGENTS.md` or `CLAUDE.md`.

### 5. Done

Tell the user the setup is complete and that `to-spec`, `wayfinder`, and `to-tickets` read `.agent-repo-config/issue-tracker.md`. `research` writes under `.agent-research/`, which is gitignored. They can edit the issue tracker file directly. Re-run this skill to switch trackers, or to copy in seed sections the file does not have yet. Starting over replaces the issue tracker file with the current seed. Re-running also adds either gitignore line that is missing.
