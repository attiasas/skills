---
name: setup-repo-skills
description: Prepare a GitHub repo's issue tracker config (GitHub issues or Jira) and, when labels are already in use, a triage label map.
disable-model-invocation: true
---

# Setup repo skills

Scaffold the per-repo configuration that the engineering skills assume.

- **Issue tracker**: where issues live (GitHub issues or Jira), how to search, how a body is written, where an estimate goes, how a blocking edge is recorded, and how a child issue is attached
- **Triage labels**: which existing label strings mean the five states and the types this repo actually uses

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

Invoke it when you want that config ready before another engineering skill reads it. `to-spec`, `wayfinder`, and `to-tickets` read `.agent-repo-config/issue-tracker.md`. When `.agent-repo-config/triage-label.md` exists, they also read that.

The config is local to the repo being set up. Write it under `.agent-repo-config/` and keep that directory gitignored. Do not commit it, and do not copy it into `docs/` or a steering file.

## Process

### 1. Explore

Look at the current repo. Read whatever exists. Don't assume.

- `git remote -v`: is `origin` a GitHub repo? Which one?
- `.agent-repo-config/issue-tracker.md`: does this skill's output already exist? If it does, note any seed section it lacks (Body, Estimate, search, blocking edge, child issue, triage label).
- `.agent-repo-config/triage-label.md`: does a map already exist? If it does, the map section is settled. Show it. Do not draft a replacement.
- `.gitignore`: is `.agent-repo-config/` already ignored?
- A Jira site or project key already written in the repo
- Labels, when the tracker can be queried. GitHub: `gh label list --limit 100 --json name`. For each name, `gh issue list --state all --limit 1 --label "NAME" --json number`. A result means the label is used. No result means the label is defined and unused. Jira has no label command in this version. Ask in Section B which labels exist and which issues carry them. Do not invent a CLI.

If no remote URL contains `github.com`, stop. This version only sets up GitHub repos. Ask for a GitHub `origin`. Write nothing.

### 2. Present findings and ask

Summarise what's present and what's missing, including which labels are used and which are only defined. Then take the sections in order. One section, one answer, then the next.

Lead with the recommended answer so the user can accept it in a word. Skip a section when exploration already settled it. When the issue tracker file exists and only lacks newer seed sections, offer to add those sections and leave the rest of the file as it is.

**Section A: Issue tracker.**

> Explainer: The issue tracker is where issues live for this repo. Later engineering skills read `.agent-repo-config/issue-tracker.md` when they create, fetch, block, or attach a ticket. Pick the place you actually track work.

Recommend **GitHub issues** when `origin` is GitHub. The only choices are:

- **GitHub**: issues live in this repo's GitHub Issues (uses the `gh` CLI)
- **Jira**: issues live in a Jira project. If the site host or project key is missing, ask for both. Do not invent a CLI.

Anything else (GitLab, Linear, local markdown) is not a choice in this version. Ask again for GitHub issues or Jira.

**Section B: Triage labels.** Skip when `.agent-repo-config/triage-label.md` already exists.

> Explainer: The map records label strings this repo already uses. It does not create labels. `to-spec` and `to-tickets` apply one type and the `needs-triage` string on a new issue. `wayfinder` applies `needs-triage` only. The other four states stay on the map for a later triage pass.

When no label is used, say so. Ask whether to write a map. Recommend **no**. On no, write nothing.

When some labels are used, propose a map from [triage-label.md](triage-label.md) and recommend accepting it.

- **State.** Keep these five rows: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Fill a row only from a used label that matches that role. A usual match: `triage` or `untriaged` for `needs-triage`; `needs-info`, `more-info`, or `waiting-for-reporter` for `needs-info`; `ready-for-agent` or `agent-ready` for `ready-for-agent`; `ready-for-human` or `ready-to-implement` for `ready-for-human`; `wontfix` or `not-planned` for `wontfix`. Two used labels for one role: recommend one string and name the other. No match: leave the cell empty.
- **Type.** One row per used label that names a kind of work. A usual match: `bug` or `defect` for `bug`; `enhancement` or `feature` for `enhancement`. `task`, `documentation`, `docs`, `chore`, `spike`, and `refactor`, when used, each get their own row. Drop a type row with no used label. Leave priority, team, and "good first issue" style labels unmapped, and list those names in the summary.
- **Defined, unused.** Name them in the summary. Leave them off the map.

On yes, the draft is the seed with their Tracker label cells filled. On no, write nothing. Do not create a label on the tracker. Creating one is a separate request. On GitHub, create only the name they named in that request.

### 3. Confirm and edit

Show a draft of:

- `.agent-repo-config/issue-tracker.md`, starting from the seed template
- `.agent-repo-config/triage-label.md`, when they accepted a map in Section B
- the `.gitignore` line `.agent-repo-config/`, when it is not already there

Let them edit the draft before writing.

### 4. Write

Write only what they accepted.

- `.agent-repo-config/issue-tracker.md`, from [issue-tracker-github.md](issue-tracker-github.md) or [issue-tracker-jira.md](issue-tracker-jira.md). For Jira, fill the site and project key. Keep the Body, Estimate, search, blocking-edge, child-issue, and triage-label notes from the seed. If they named a real command or tool, use that in the Commands section and leave the other sections as accepted. When the file already exists and they only accepted missing seed sections, add those sections and leave the rest of the file as it is.
- `.agent-repo-config/triage-label.md`, from [triage-label.md](triage-label.md), with the accepted Tracker label cells, unused type rows removed, and extra used type rows added. Keep the Applying labels section. If the file already exists, do not overwrite it unless they asked to replace it in this session.
- `.gitignore`: add `.agent-repo-config/` if it is missing. Do not add a second copy of it.

Leave every other file alone. In particular, do not create `docs/agents/`, and do not edit `AGENTS.md` or `CLAUDE.md`.

### 5. Done

Tell the user the setup is complete. `to-spec`, `wayfinder`, and `to-tickets` read `.agent-repo-config/issue-tracker.md`, which is gitignored. When a triage map was written, they also read `.agent-repo-config/triage-label.md` and apply the type and entry state from it. When no map was written, those skills publish with no triage label.

They can edit either file directly. Re-run this skill to switch trackers, or to copy in seed sections the issue tracker file does not have yet. Starting over replaces the issue tracker file with the current seed. Re-running leaves an existing triage map in place. Say "replace the triage map" to draft a new one. Re-running also adds the gitignore line if it is missing.
