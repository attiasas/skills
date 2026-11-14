---
name: to-hld
description: Produce a high-level design (HLD) file using the seven-section engineering design-review template, plus an HTML slide deck of it for the review. Use when the user asks for an HLD, high-level design, feature design review, DR deck/doc, or to write design-review sections (Why, system diagram, sequence, schema/ERD, API, NFR, testing, open questions).
---

# Creating an HLD

Write one markdown HLD file. The source of truth is the engineering design-review template: **seven required sections**, then **open questions**. Each section has a format (what reviewers expect) — fill it for *this* feature; do not copy the back-in-stock example unless the user asked for that feature.

Template rule: **one section is the floor, not the ceiling**. Split a section if it needs more room. **Never drop a section.**

## Workflow

1. Gather the feature: problem, services, flow, data, API, scale, tests, decisions needed.
2. Pick an output path: `.agent-docs/hld-<feature-slug>.md` unless the user named a file.
3. Draft all eight headings below (seven sections + open questions). Use real names from the codebase.
4. Draw diagrams in mermaid. Keep **the same box names** in the system diagram, sequence diagram, schema, tests, and NFRs.
5. Run the [Before you book the review](#before-you-book-the-review) checklist. Fix gaps before presenting the file.
6. Put anything longer than a tight section in an **appendix** and link it — do not dump it into the main sections.
7. Write the review deck next to the markdown, same name with `.html` (see [HTML review deck](#html-review-deck)). Open it for the user (`open <path>` on macOS) and give both paths.

For a worked example, see [examples.md](examples.md). For a blank file skeleton, copy [template.md](template.md). For the deck, copy [template.html](template.html).

## HTML review deck

The markdown is the source of truth. The deck is a view of it for the review: one full-screen slide per section, a side rail to jump between them, arrow keys and PageUp/PageDown to step, and one slide per page when printed.

- Copy `template.html` and replace every UPPERCASE placeholder. Repeat a block (gap card, table row, migration step, question card) once per item; delete blocks the HLD has no content for, but keep every slide.
- Carry the content over, do not summarise it away and do not add claims the markdown lacks. Shorten prose to fit a slide; tables, numbers, payloads and diagrams go over whole.
- Map each section to its visual:
  - 01 Why: one card per gap, its measured figure as the metric. Goal in the callout.
  - 02 System diagram: the same mermaid, plus `class <id> new|changed|ext` lines using the template's `classDef`s, so the legend matches the boxes.
  - 03 Sequence: the same mermaid; one warning callout per short-circuit.
  - 04 Schema & ERD: one `pill new|reuse|alter` per table; migration order as `.steps`, with blocking and rollback under each step.
  - 05 API usage: request and response panes side by side; errors, partial success and idempotency in the behaviour table.
  - 06 NFR & sizing: the headline numbers as tiles, then the full table.
  - 07 Testing: one band row per band, its cases under it.
  - Open questions: one card per question; the recommended option gets class `rec`.
  - Appendices: one extra slide each, after open questions.
- Escape `<`, `>` and `&` in payloads and table text. Mermaid blocks keep the markdown's source verbatim.
- When the markdown changes, regenerate the deck so the two never disagree.

## File shape

```markdown
# HLD: <feature name>

- Status: draft | in review | accepted
- Author:
- Date:
- Related tickets:

## 01 Why
## 02 System diagram
## 03 Sequence
## 04 Schema & ERD
## 05 API usage
## 06 NFR & sizing
## 07 Testing
## Open questions
```

---

## 01 Why

Describe today's behaviour and its cost. **No solution language on this section** — if the room disagrees with the problem, the rest of the review is wasted.

**Must include**

- The behaviour that exists today
- Its cost, in a number
- Who is blocked, and on what
- Why now rather than next quarter

**Shape it as**

- Two or three gaps, each one line
- One measured figure per gap
- A closing line naming the goal

**Red flags:** “Improve performance” with no baseline. Architecture described before the gap. A gap nobody has ever reported.

---

## 02 System diagram

One picture of every subsystem this feature touches and every edge between them. Sections 03–07 all refer back to this map — **draw it once and keep the names stable**.

**Must include**

- Every service, store and queue involved
- Direction on every arrow
- A label on each edge: what crosses it
- Which boxes are new or changed

**Conventions**

- Cylinders for stores, boxes for services (in mermaid: `[(store)]` vs `[service]`)
- Call out **owned/changed** vs **external or shared** in a short legend under the diagram

**Red flags:** Boxes the feature never touches. Undirected lines. Names that differ from the codebase.

---

## 03 Sequence

One flow, in time order, over the **exact boxes from section 02** — same names, same set. Choose the flow whose ordering is hardest to guess from the system diagram alone.

**Must include**

- Lifelines matching the system diagram
- Numbered messages in order
- Batch sizes on the wire, not just verbs
- Where the flow can short-circuit

**Pick the flow that**

- Exercises the most subsystems
- Is the hot path in production
- Reviewers are most likely to challenge

**Red flags:** A lifeline that never appeared in 02. Per-item messages drawn as one arrow. No return arrows — only requests.

---

## 04 Schema & ERD

An ERD of **only the tables this feature reads or writes**, marked up so a reviewer can see the migration surface at a glance.

**Must include**

- Every table tagged `NEW`, `REUSE` or `ALTER`
- Cardinality and cascade on each relation
- New indexes and uniqueness constraints
- Migration order, and what blocks what

**Also state**

- Backfill volume and how long it runs
- Whether the migration is online
- The rollback for each step

**Red flags:** A full existing schema pasted in. New table, no index story. Dedup or backfill left as “TODO”.

If the feature has no schema change, still include the section: list the tables **REUSE**d and state “no DDL / no backfill”.

---

## 05 API usage

A real call with real values, **request and response side by side**. Field tables belong in an appendix; this section shows the shape a caller will actually send and receive.

**Must include**

- Method, path, and one real payload
- The matching response, same case
- Values from a package / resource people know
- What changed versus today's contract

**Behaviour to state**

- Error codes and what triggers them
- Partial success: what comes back
- Idempotency and ordering guarantees

**Red flags:** “foo” / “bar” placeholder values. Request shown without its response. Only the happy path.

If there is no HTTP API, show the equivalent contract (event, RPC, CLI) with a real payload pair.

---

## 06 NFR & sizing

The scale you commit to support, as **numbers with units**. Every figure needs a source: measured today, projected from growth, or a target you are choosing.

**Must include**

- Throughput and peak concurrency
- Latency targets at p50 / p95 / p99
- Data volume and growth per year
- Availability and degradation mode

**Per row, give**

- Today's measured value
- The target, with headroom
- Where the number came from

Use this table:

| Dimension | Today | Target | Source of the number |
| --- | --- | --- | --- |
| | | | |

**Red flags:** “Should scale horizontally”. Averages instead of percentiles. A target with no known baseline.

Lead the section with 3–4 headline numbers (value + unit + what it measures).

---

## 07 Testing

Four bands, and each one names the thing it proves. Write a table where **every row points back at a claim made earlier in the file**.

| Band | What it proves |
| --- | --- |
| Completeness | Every path in the sequence diagram has at least one test that walks it end to end |
| Edge cases | Empty, malformed, conflicting and duplicate inputs — name the specific ones for this feature |
| Error handling | Each dependency in the system diagram, taken down in turn: what the caller sees |
| Non-functional | One load run per NFR row, at increasing sizes, with the pass criterion written down first |

Table columns: `BAND | CASE | PASS CRITERION`.

**Red flags:** “unit tests will be added”. A load test with no pass criterion. Error handling covered only by a retry mention.

---

## Open questions

Decisions you want from the room. Write each as a **decision with options**, not as unfinished work.

```markdown
### Q<n>: <decision>
- Options: A … / B …
- Recommendation:
- Needed from: <role>
```

---

## Before you book the review

- [ ] The why section contains at least one measured number.
- [ ] Every box in the sequence diagram exists in the system diagram, under the same name.
- [ ] Every table in the ERD is tagged NEW, REUSE or ALTER, and the migration order is stated.
- [ ] The API example uses a real package (or real resource) and shows a response, not just a request.
- [ ] Every NFR row has a unit, a target and a source.
- [ ] Every test row names the claim it defends and its pass criterion.
- [ ] Open questions are written as decisions with options, not as unfinished work.
- [ ] Anything longer than a section lives in an appendix that is linked, not inlined as the main read.
- [ ] The HTML deck exists beside the markdown, has every slide, and matches the markdown's current content.
