---
name: assess
description: Size a specced change. When the module interface is still a choice, design it twice with codebase-design. Otherwise write a module brief or an HLD, then hand it off for review, the tracker, or implementation.
disable-model-invocation: true
---

# Assess

A spec comes in. You decide whether the module interface is already settled. When it is not, `codebase-design` explores it. Then you write the smallest design that fits, and hand it off.

There is no review panel and no vote. `codebase-design` already runs fresh agents on different interface constraints and has you compare them. Do not add a second pass.

Use its words: module, interface, seam, adapter. Not component, service, API, or boundary.

Everything this skill writes goes under `.agent-docs/assess-<slug>/`, where the slug is 2 to 4 kebab-case words from the change. Create the directory if it is missing. If `.gitignore` does not already ignore `.agent-docs/`, add that line.

## 1. Gather

The input is an issue (number or URL), a file path, or the current conversation.

- An issue: read `.agent-repo-config/issue-tracker.md` and fetch it the way that file says, comments included. If the file is missing, stop and tell the human to run `setup-repo-skills`.
- A path: read the whole file.
- The conversation: use what it settled.

Find the spec: background and acceptance criteria. When there is none, stop and tell the human to run `to-spec`. Do not write acceptance criteria yourself.

Write the spec, as found, to `spec.md`. Note its source on the first line.

## 2. Classify

Read the code the spec touches. Tell the human one line which case, and the fact that decided it. Do not wait.

- **Fog.** You cannot name the module, because what changes is still undecided. Tell the human to run `wayfinder`. Stop.
- **Undiagnosed.** The input is a failure, and neither the spec nor the code settles the cause. Tell the human to run `diagnosing-bugs`. Stop. Do not design a fix for a cause you have not reproduced.
- **Several features** that ship independently. Tell the human to run `to-tickets`. Stop.
- **Open interface.** The spec does not settle what a caller must know, where the seam goes, or what the implementation hides.
- **Settled.** The spec or the code already fixes those. Skip `codebase-design`.

Then the artifact, either way:

- **Brief** when one module changes, and there is no schema change, no contract change, and no scale or latency target.
- **HLD** otherwise.

## 3. Research

Research only when the next step depends on a fact the repo cannot answer: an external API, a library's behaviour, a protocol, a limit. Call the `research` skill with that question. Wait for its file under `.agent-research/`. Skip this step and say so when nothing is unknown.

## 4. Design

When the case is **open interface**, follow `codebase-design`'s design-it-twice. Subagents start with a fresh context window. Use the model the human named. Otherwise use the default model. Write the comparison and your recommendation to `decision.md`.

Then write the artifact:

- **Brief:** `design.md` from [brief.md](brief.md).
- **HLD:** call `to-hld` with the output path `.agent-docs/assess-<slug>/design.md`. When `decision.md` exists, the HLD uses that interface and does not reopen it.

Every acceptance criterion in `spec.md` maps to a test in the brief, or to a row in the HLD's testing section.

## 5. Hand off

Show `decision.md` when it exists, and the path to `design.md`. Ask what to do next. They may pick more than one:

- **Human review.** Show the design and take their edits. Write the edits into `design.md` and, when the edit changes the recommendation, into `decision.md`.
- **Record on the issue.** Only when the input was an issue. Draft a comment: the recommendation and the design summary. Show the exact body and wait for a reply to it. Then post it the way the tracker file says to comment. "Post whatever you write" said before the body was shown is not approval.
- **Implementation handover.** Write `handover.md`: the spec, `decision.md` when it exists, the design inlined, and the acceptance criteria as a checklist. A fresh implementer must be able to start from that file alone. When the change spans more than one shippable slice, tell the human to run `to-tickets` with that file.

Do not implement the change here.

## Red flags

Stop if you are about to:

- Write a design without a spec
- Design a fix for a bug you have not reproduced
- Run design-it-twice when the interface is already settled
- Add a review panel, a vote, or a second pass over the design
- Reopen the interface inside the HLD after `decision.md`
- Post to the tracker before the human replied to the shown comment
- Start implementing
