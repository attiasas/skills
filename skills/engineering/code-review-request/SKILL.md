---
name: code-review-request
description: Dispatch a fresh-context review of completed work before it cascades, and add a tech-lead architect review when the change is large or crosses components. Use when finishing a task, implementing a major feature, or before merging.
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. When the change is large or touches more than one component, also dispatch a tech lead (system and code architect) and aggregate both reports. Every reviewer gets a fresh context and the work product only — never this session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Decide who reviews**

Always dispatch the code reviewer.

Also dispatch a tech lead when the change is risky. Read `git diff --stat "$BASE_SHA".."$HEAD_SHA"` and `git diff --shortstat "$BASE_SHA".."$HEAD_SHA"`. Risky means either:

- Files land in two or more components (separate packages, services, modules, or top-level areas). If you cannot tell whether two paths are one component, they are two.
- The diff is large: 8 or more files, or 400 or more changed lines.

**3. Dispatch**

Dispatch a `general-purpose` subagent with a fresh context, filling [code-reviewer.md](code-reviewer.md).

When step 2 says the tech lead is required, dispatch a second `general-purpose` subagent in the same turn, also with a fresh context, filling [tech-lead.md](tech-lead.md). The tech lead is a system and code architect. They review the same range. They do not see this session's history, your implementation reasoning, or the code reviewer's prompt or output.

**Placeholders (both templates):**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**4. Aggregate**

Wait for every reviewer you dispatched. Act on the combined result, not on whichever report returns first.

If the tech lead was not required, the result is the code reviewer's report plus one line: `Tech lead skipped: one component, <N> files, <M> lines.`

If both ran, write:

```
## Review

### Code review
<code-reviewer report>

### Tech lead
<tech-lead report>

### Combined
Verdict: Yes | With fixes | No

#### Critical
#### Important
#### Minor

### Disagreements
```

- List each issue once, under its severity. When both reports describe the same issue, keep the sharper write-up and name both sources.
- A disagreement stays as two lines under `### Disagreements`. Do not merge it into one milder issue.
- Verdict, first match: **No** if any issue is Critical or any assessment is No. **With fixes** if any issue is Important or any assessment is With fixes. **Yes** only when every report that ran says Yes and nothing above Minor remains.

**5. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if a reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: With fixes

Tech lead skipped: one component, 2 files, 80 lines.

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each task or at natural checkpoints
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Skip the tech lead because the code reviewer already has an architecture section
- Show the tech lead the code reviewer's findings
- Collapse a disagreement into one softer finding
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

Templates: [code-reviewer.md](code-reviewer.md), [tech-lead.md](tech-lead.md)
