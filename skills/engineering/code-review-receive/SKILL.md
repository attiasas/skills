---
name: code-review-receive
description: Evaluates code-review feedback before changing code, then closes with a triage of each item by severity and type. Use when review comments arrive, especially when they are unclear or technically questionable. Writes an HTML summary only when asked, and posts replies only after a yes in chat.
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
7. CLOSE: Triage in chat. HTML only if they asked. Then ask before posting replies
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit instruction-file violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From your human partner
- **Trusted** - implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**your human partner's rule:** "External feedback - be skeptical, but check carefully"

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**your human partner's rule:** "You and reviewer both report to me. If we don't need this feature, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
  5. Close with the triage
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with your human partner's architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Involve your human partner if architectural

**If you're uncomfortable pushing back out loud:** Name that tension, then tell your partner about the issue you've seen. They'll appreciate your honesty.

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |
| Close with a prose recap | The close is the triage, severity then type |
| Write the HTML page every time | The page is only when they asked for a summary |
| Put the reply question on the page | The question is in chat, after the triage |
| Post replies before they answer | Ask once. Post after a yes, and only the handled items |

## Real Examples

**Performative Agreement (Bad):**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## Close

After every item has a disposition, close in this order. The triage is the record of the run.

### 1. Triage in chat

One block per feedback item that has a disposition, including items you pushed back, declined, or left open.

Order: severity, then type, then the order the reviewer wrote them.

Severity, in this order: Critical, Important, Minor, Nit. Map Blocker to Critical and Suggestion to Nit. A comment with no severity is Important until the code shows a different one.

Type, one per item, in this order: security, regression, defect, design, spec, test, scope, question, style. When two fit, use the earlier one.

| Disposition | Meaning | Handled |
| --- | --- | --- |
| fixed | Code or tests changed to address it | yes |
| pushed back | Rejected for this codebase. Code unchanged | yes |
| declined | Out of scope or unused. Code unchanged | yes |
| already correct | Checked. The code already does this | yes |
| needs clarification | Stopped. Not implemented | no |
| deferred | Accepted, left for later | no |

Handled items are the ones a later yes may reply to. An understood item left unimplemented because something else was unclear is deferred, not fixed.

```
## Triage

<n> fixed · <n> pushed back · <n> declined · <n> already correct · <n> needs clarification · <n> deferred

Source: <PR or review URL, or "this conversation">

### <Severity> · <Type>

**<Item>** — <Disposition>
- Reporter: <who>, <thread URL or "no thread">
- Where: <file:line, or "no code site">
- Reproduce: <steps that show the original finding. After a fix, the result of those same steps now>
- Why: <the verified problem, or why the suggestion does not hold>
- What changed: <one sentence, or "No code change">
- Reasoning: <why the change takes this shape, or why the code stayed>
- Evidence: <command and result, or file:line that shows the claim>
```

Omit a count that is zero. Omit a severity and type heading that has no items. Evidence is a command plus its result, or a file and line. Reproduce names the command or steps. When you could not reproduce it, name the command you ran and the result.

Why is the verified problem. Reasoning is why the response takes this shape. They are different sentences.

### 2. HTML summary, when they asked

Write the page only when they asked for a summary, an HTML summary, or a page. Write `review-triage.html` in the current directory from [triage-template.html](triage-template.html). Replace every UPPERCASE placeholder. Leave the script in place. Do not commit the file.

`SUMMARY` is two to four sentences: what was fixed, what was pushed back or declined, and what is still open. It sits after Overview. The search and the Handled, severity, type, and disposition filters are already in the template.

Repeat the summary row and the item article once per item, in the same order as the chat triage. Give each item an id `item-1`, `item-2`, and so on. The summary row's `data-id` is that id, and its link points at it. Set `data-severity`, `data-type`, `data-disposition`, and `data-handled` on both the row and the article. `data-handled` is `yes` for fixed, pushed back, declined, and already correct, and `no` for needs clarification and deferred. `data-disposition` is `fixed`, `pushed-back`, `declined`, `correct`, `clarify`, or `deferred`. The disposition pill uses that class, and its text is the disposition name.

Inside an item, the order is Where, Reproduce, Why, What changed, Reasoning, Evidence. Reporter stays on the line under the title. `REPORTER_NAME` in the summary table is the short name. `REPORTER` is that name plus the thread.

Delete a severity section with no items, and its nav link.

Open it with `open` and give the path. The page carries the same items as the chat triage. The chat triage stays complete. The page has no question and no reply.

### 3. Ask about replies

After the chat triage, and after the page is open when you wrote one, ask once in the chat with `AskQuestion`:

- Post replies on the handled items
- Don't post

Silence is not a yes. "Post them" is a yes.

On a yes, post one reply per handled item that has a thread, on that thread. The reply is the disposition, what changed or why the code stayed, and the evidence. No greeting and no thanks. On GitHub, an inline review comment is a reply on that comment:

`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body='...'`

An inline thread does not get a new top-level PR comment. A handled item with no thread is named in chat and not posted. Needs clarification and deferred stay unposted.

On a no, stop.

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always. The run ends with the triage. Replies wait for a yes in chat.
