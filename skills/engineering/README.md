# Engineering

Skills for code work.

## User-invoked

Reachable only when you type the skill name (`disable-model-invocation: true`).

- **[assess](./assess/SKILL.md)**: Size a specced change. When the module interface is still a choice, design it twice with codebase-design. Otherwise write a module brief or an HLD, then hand it off for review, the tracker, or implementation.
- **[setup-repo-skills](./setup-repo-skills/SKILL.md)**: Write a gitignored `.agent-repo-config` for a GitHub repo (GitHub issues or Jira), including a triage label map when the tracker already uses state or type labels. Run before another engineering skill needs the issue tracker.
- **[to-spec](./to-spec/SKILL.md)**: Drafts a verified tracker spec and publishes it only after the shown body is approved. Applies a mapped triage type and entry state when that map exists.
- **[to-tickets](./to-tickets/SKILL.md)**: Break a plan, spec, or conversation into vertical-slice tickets with blocking edges, and publish them after the breakdown is approved. Applies a mapped triage type and entry state when that map exists.
- **[wayfinder](./wayfinder/SKILL.md)**: Chart a large, foggy effort as decision tickets on the repo issue tracker, and settle one decision per session until the route is clear enough to implement. Applies the mapped entry state when a triage label map exists.

## Model-invoked

Reachable by you or by the agent when the task fits.

- **[codebase-design](./codebase-design/SKILL.md)**: Shared vocabulary for designing deep modules, plus a parallel design-it-twice pass when the interface is still a choice.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**: Diagnosis loop for a hard bug or a performance regression. Build a tight failing loop before hypothesising, then fix it.
- **[research](./research/SKILL.md)**: Investigate a question against primary sources and write the findings under `.agent-research/`.
- **[to-hld](./to-hld/SKILL.md)**: Produce a high-level design (HLD) file using the seven-section engineering design-review template.
