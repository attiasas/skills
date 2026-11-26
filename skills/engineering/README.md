# Engineering

Skills for code work.

## User-invoked

Reachable only when you type the skill name (`disable-model-invocation: true`).

- **[assess](./assess/SKILL.md)**: Size a specced change. When the module interface is still a choice, design it twice with codebase-design. Otherwise write a module brief or an HLD, then hand it off for review, the tracker, or implementation.
- **[hld-planner](./hld-planner/SKILL.md)**: Settle a foggy idea into an approved design in one dialogue. A panel of expert subagents investigates and proposes approaches independently, and their findings drive the interview and two or three compared approaches. The plan is shown as an HTML deck until it is approved, then the skill writes the HLD, spec, plan, or effort breakdown. A route of decisions settled across sessions belongs to wayfinder.
- **[to-spec](./to-spec/SKILL.md)**: Drafts a verified spec and publishes it to GitHub issues or Jira, or writes it locally when asked or when it is for implement-spec, only after the shown body is approved. A local file is the input implement-spec takes. Applies a triage label only when that label is already in use and the human approved it.
- **[to-tickets](./to-tickets/SKILL.md)**: Break a plan, spec, or conversation into vertical-slice tickets with blocking edges, and publish them to GitHub issues or Jira after the breakdown is approved. Applies a triage label only when that label is already in use and the human approved it.
- **[implement-spec](./implement-spec/SKILL.md)**: Implement any spec (issue, file, or conversation). Validate and size it, require an approved HLD for large changes, plan, implement with subagents, then review and QA. Before anything lands on the integration branch, show an HTML summary of the implementation and of each change and validation traced to the spec with evidence, and wait for commit or adjust. Push when a check needs it. Open a pull request when asked. It never merges or closes tickets. Optionally records the plan, changes, and testing on the tracker.
- **[wayfinder](./wayfinder/SKILL.md)**: Record a foggy effort as a decision map settled across sessions, with options and a recommendation on each open question. Export it to GitHub issues, Jira, or a file in the repo, then hand it to to-tickets or settle each open until the route is clear. A design, spec, or plan produced in one dialogue belongs to hld-planner.

## Model-invoked

Reachable by you or by the agent when the task fits.

- **[code-review](./code-review/SKILL.md)**: Review the changes since a fixed point along two axes, Standards and Spec, using parallel sub-agents, and report them side by side. Use when the user asks to review a branch, PR, or work in progress, or to "review since X".
- **[code-review-receive](./code-review-receive/SKILL.md)**: Evaluate code-review feedback before changing code, then close with a triage of each item by severity and type. Use when review comments arrive, especially when they are unclear or technically questionable. An HTML summary is written only when asked, and replies are posted only after a yes in chat.
- **[code-review-request](./code-review-request/SKILL.md)**: Dispatch a fresh-context review of completed work, adding a specialist only when the diff matches that lens, and run a validation pass that records each command and its output. Use when finishing a task, a major feature, before merging, or when reviewing again after an earlier review. A follow-up accounts for the previous report and writes the HTML page without asking. A first review writes HTML only when asked. Pull-request comments are posted only after a yes in chat.
- **[codebase-design](./codebase-design/SKILL.md)**: Shared vocabulary for designing deep modules, plus a parallel design-it-twice pass when the interface is still a choice.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**: Find the cause of a hard bug or a performance regression with a failing loop before any theory, then report the fewest steps to replicate the bug and to validate the fix.
- **[research](./research/SKILL.md)**: Investigate a question against primary sources and write the findings under `.agent-research/`.
- **[tdd](./tdd/SKILL.md)**: Test-driven loop for features and bug fixes: one failing test through the public interface, the smallest passing change, then refactor while green.
- **[to-hld](./to-hld/SKILL.md)**: Produce a high-level design (HLD) file using the ten-section engineering design-review template (Why, How, system diagram, sequence, schema, API, NFR, testing, risk, monitoring, plus open and ship questions), and an HTML slide deck of it (one slide per section) for the review.
