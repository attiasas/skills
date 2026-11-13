# Expert panel

## Roster

Pick only the experts whose lens the idea touches. Two to five is the usual panel.

| Role | Pick when the idea | Investigates |
| --- | --- | --- |
| `architect` | spans modules or services, or changes boundaries | Which modules change, where the seams go, coupling, how it fits the existing architecture |
| `domain` | changes user-facing behaviour or business rules | Who uses it, today's flow, the rules and edge cases in the code, what success means |
| `data` | touches schemas, stores, migrations, or data volume | Tables and stores involved, migration and backfill, consistency, retention |
| `api` | adds or changes a contract (HTTP, RPC, event, CLI) | Current contracts and callers, compatibility, versioning, error behaviour |
| `integrations` | depends on an external service, library, or protocol | The dependency's real behaviour and limits, from its official docs or source |
| `security` | handles auth, secrets, user data, or untrusted input | Trust boundaries, permissions, data exposure, abuse cases |
| `performance` | has scale, latency, or cost stakes | Today's load and hot paths, sizing, bottlenecks, cost |
| `operations` | runs in production or changes deployment | Rollout, feature flags, observability, failure modes, rollback |
| `frontend` | changes UI or client behaviour | Affected screens and components, state, accessibility |
| `testing` | is risky to verify or lacks test coverage | Existing coverage, what must be tested, how to test it end to end |
| `delivery` | is large enough to need phasing | Dependencies between parts, what can ship alone, sequencing, team ownership |

## Investigation brief

Send each expert this, filled in:

```markdown
You are the <role> expert on a design panel. Investigate only through the <role> lens.
Other experts cover the other lenses. Work independently.

## The idea
<the two-line restatement the human confirmed>

## Starting points
<modules, files, docs, tickets the orchestrator found>

## Your lens
<the "Investigates" cell for this role, plus anything specific to this idea>

## Rules
- Read the code and primary sources (official docs, source, specs). Cite a file:line or URL for every fact.
- Do not edit any file except your output file.
- Separate what you verified from what you infer.

## Output
Write <work-dir>/experts/<role>.md with these sections:
- **Facts.** Verified, each with its source.
- **Inferences.** What you believe but could not verify, and why.
- **Risks.** Each with likelihood, impact, and the evidence.
- **Questions for the human.** Only what the code and sources cannot answer. For each, give two to four options when you can name them.
- **Constraints.** What any design must respect, from your lens.

Return a three-line summary and the path.
```

## Approach brief

Send each re-dispatched expert this, filled in:

```markdown
You are the <role> expert on a design panel. Propose and critique approaches through the <role> lens only.
Work independently.

## Open design choices
<each choice still open>

## Settled
<decisions from the interview, and the path to findings.md>

## Rules
- Ground every approach in the current code. Cite file:line.
- Do not edit any file except your output file.

## Output
Write <work-dir>/experts/<role>-approaches.md. Per open choice:
- One to three approaches: how it works here, cost, risk, when it is the right pick.
- Objections, from your lens, to any approach you expect another expert to propose.
- Your pick and the deciding reason.

Return a three-line summary and the path.
```
