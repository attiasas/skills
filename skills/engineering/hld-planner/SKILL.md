---
name: hld-planner
description: Settle a foggy idea into an approved design in one dialogue. A panel of expert subagents investigates and proposes approaches independently, and their findings drive the interview and two or three compared approaches. The plan is shown as HTML until it is approved, then the skill writes the HLD, spec, plan, or effort breakdown. A route of decisions settled across sessions belongs to wayfinder.
disable-model-invocation: true
---

# HLD Planner

The human brings an idea that is too big or too vague to build. Clear the fog with them, one question at a time, and finish a design in this session. Do not implement anything here.

This skill finishes in one session. When the open items are a route of decisions to settle later, tell the human to run `wayfinder` and stop. Do not draft that map here.

Everything this skill writes goes under `.agent-docs/hld-planner-<slug>/`, where the slug is 2 to 4 kebab-case words from the idea. Create the directory if it is missing. If `.gitignore` does not already ignore `.agent-docs/`, add that line.

## 1. Assess

Restate the idea in two lines: what it is and what "done" looks like. Ask the human to correct it before going further.

Then size it, and say which case applies in one line:

- **Clear and small.** It fits one session and nothing is undecided. Say so. Skip the planner and ask how they want to proceed.
- **Several independent efforts.** Name them. Ask which one to plan first. Plan only that one.
- **Across sessions.** The decisions will not be settled now. Tell the human to run `wayfinder`. Stop.
- **Foggy, this session.** Continue.

## 2. Investigate with an expert panel

You orchestrate. The experts investigate. Do not run their investigations yourself.

1. Skim the code, docs, and tickets the idea touches. Read only enough to choose the panel and to name the modules, services, and stores involved, using their real names.
2. Pick two to five experts from [experts.md](experts.md). Pick only the ones whose lens the idea actually touches. Add a role that is not listed when the idea needs one. Tell the human the panel and one line on why each expert is on it. Do not wait.
3. Dispatch every expert as a subagent, in parallel, each with a fresh context window. Use the model the human named. Otherwise use the default model. Each one gets the brief from [experts.md](experts.md) and writes only `experts/<role>.md` in the work directory. Experts work independently: none of them sees another's file.
4. When all have returned, read every file and write `findings.md`:
   - **Facts.** What the panel established, each with its source.
   - **Conflicts.** Where experts disagree. Keep both positions and who holds them. Do not settle a conflict yourself.
   - **Risks.** Merged and de-duplicated, highest first.
   - **Questions for the human.** Merged from every expert, de-duplicated, sorted so the questions that block others come first. This list seeds the interview.

When a fact still matters and no expert could answer it (an external API, a library's behaviour, a protocol, a limit), call the `research` skill with that one question. Keep interviewing while it runs. Read its file under `.agent-research/` before relying on the answer.

## 3. Interview

Start from the questions and conflicts in `findings.md`. Keep a running list. Sort it so the questions that block others come first. Put an expert conflict to the human as a question: both positions, who holds each, and your recommendation.

- Ask **one question per message.** Prefer the `AskQuestion` tool with two to four options. Use an open question only when you cannot name the options.
- Ask about intent, constraints, users, scale, and what success is measured by. Do not ask for facts the panel or research already gave you.
- When a question is a preference, the answer is theirs. When it is a fact, find it.
- After each answer, update the list: drop what it settled, add what it made precise.
- Stop interviewing when every remaining question either has an answer or is a design choice between approaches.
- If an answer shows the rest are decisions for later sessions, stop. Tell the human to run `wayfinder` and pass what this session settled.

## 4. Approaches

For each design choice that is still open, propose two or three approaches. Skip this when only one approach is viable, and say why.

Run the panel again for this round. Re-dispatch, in parallel and with fresh context, the experts whose lens the open choices touch. Give each one the approach brief from [experts.md](experts.md): the choices, the decisions the interview settled, and `findings.md`. Each writes `experts/<role>-approaches.md`. Then merge their proposals into two or three distinct approaches per choice. Credit each approach to the experts who proposed it, and attach every expert's objection to the approach it targets.

Per approach: one-line summary, how it works in this codebase, what it costs, what it risks, and when it would be the right pick. Close with your recommendation and the deciding reason. Lead with the recommendation.

Wait for the human to pick. Accepting the recommendation is a pick.

## 5. Plan as HTML

Write the plan to `plan.html` in the work directory, starting from [template.html](template.html). Open it with `open <path>` and give the path in chat.

The plan holds:

- **Goal.** What done looks like.
- **Context.** What exists today, in the codebase's own names.
- **Decisions.** Each settled question, its answer, and the approach chosen with its trade-off.
- **Design.** The shape of the solution: parts, flow, data, contracts. Diagrams as Mermaid when a picture helps.
- **Phases.** Ordered steps, each shippable or verifiable on its own.
- **Risks and open questions.** What is still unknown, and who decides it. Include expert objections the chosen approach did not answer.
- **Out of scope.** What this plan does not include.

Present each section in chat as you draft it, and ask whether it looks right before moving to the next. On every edit, update `plan.html` and tell them to refresh. Do not write any other output format until the human approves the plan.

## 6. Produce the output

After approval, ask which output they want. They may pick more than one:

- **HLD.** Call `to-hld` with the output path `.agent-docs/hld-planner-<slug>/hld.md`. The HLD uses the decisions in the plan and does not reopen them.
- **Implementation plan.** Write `plan.md`: the approved plan as markdown, phases as a checklist.
- **Spec.** Write `plan.md`, then tell the human to run `to-spec` with it.
- **Tickets or effort breakdown.** Write `plan.md`, then tell the human to run `to-tickets` with it.
- **Decision map.** When open questions remain that need more than one session, tell the human to run `wayfinder` with `plan.md`.

Name each file written. Leave `plan.html` in place.

## Red flags

Stop if you are about to:

- Investigate the idea yourself instead of dispatching the panel
- Dispatch an expert whose lens the idea does not touch
- Settle an expert conflict without asking the human
- Ask more than one question in a message
- Ask the human something the panel or research already answers
- Present a single approach as the only option without saying why
- Write the HLD, spec, or tickets before the HTML plan is approved
- Keep planning a route of decisions that will not be settled this session
- Start implementing
