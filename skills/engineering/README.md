# Engineering

Skills for code work.

## User-invoked

Reachable only when you type the skill name (`disable-model-invocation: true`).

- **[assess](./assess/SKILL.md)**: Size a specced change. When the module interface is still a choice, design it twice with codebase-design. Otherwise write a module brief or an HLD, then hand it off for review, the tracker, or implementation.
- **[hld-planner](./hld-planner/SKILL.md)**: Settle a foggy idea into an approved design in one dialogue. A panel of expert subagents investigates and proposes approaches independently, and their findings drive the interview and two or three compared approaches. The plan is shown as HTML until it is approved, then the skill writes the HLD, spec, plan, or effort breakdown. A route of decisions settled across sessions belongs to wayfinder.
- **[setup-repo-skills](./setup-repo-skills/SKILL.md)**: Write a gitignored `.agent-repo-config` for a GitHub repo (GitHub issues or Jira), including a triage label map when the tracker already uses state or type labels. Run before another engineering skill needs the issue tracker.
- **[to-spec](./to-spec/SKILL.md)**: Drafts a verified tracker spec and publishes it only after the shown body is approved. Applies a mapped triage type and entry state when that map exists.
- **[to-tickets](./to-tickets/SKILL.md)**: Break a plan, spec, or conversation into vertical-slice tickets with blocking edges, and publish them after the breakdown is approved. Applies a mapped triage type and entry state when that map exists.
- **[implement-spec](./implement-spec/SKILL.md)**: Implement a spec from an issue or an assess handover on one integration branch, and optionally record progress on the tracker.
- **[wayfinder](./wayfinder/SKILL.md)**: Record a foggy effort as a decision map settled across sessions, with options and a recommendation on each open question. Export it to the issue tracker or a file in the repo, then hand it to to-tickets or settle each open until the route is clear. A design, spec, or plan produced in one dialogue belongs to hld-planner. Applies the mapped entry state on a tracker export when a triage label map exists.

## Model-invoked

Reachable by you or by the agent when the task fits.

- **[code-review](./code-review/SKILL.md)**: Review the changes since a fixed point along two axes, Standards and Spec, using parallel sub-agents, and report them side by side. Use when the user asks to review a branch, PR, or work in progress, or to "review since X".
- **[code-review-receive](./code-review-receive/SKILL.md)**: Evaluate code-review feedback before changing code. Use when review comments arrive, especially when they are unclear or technically questionable.
- **[code-review-request](./code-review-request/SKILL.md)**: Dispatch a fresh-context review of completed work, plus a tech-lead architect review when the change is large or crosses components, and aggregate both reports. Use when finishing a task, a major feature, or before merging.
- **[codebase-design](./codebase-design/SKILL.md)**: Shared vocabulary for designing deep modules, plus a parallel design-it-twice pass when the interface is still a choice.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**: Diagnosis loop for a hard bug or a performance regression. Build a tight failing loop before hypothesising, then fix it.
- **[research](./research/SKILL.md)**: Investigate a question against primary sources and write the findings under `.agent-research/`.
- **[tdd](./tdd/SKILL.md)**: Test-driven loop for features and bug fixes: one failing test through the public interface, the smallest passing change, then refactor while green.
- **[to-hld](./to-hld/SKILL.md)**: Produce a high-level design (HLD) file using the seven-section engineering design-review template, plus an HTML slide deck of it (one slide per section) for the review.
