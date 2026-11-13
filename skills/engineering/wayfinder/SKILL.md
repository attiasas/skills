---
name: wayfinder
description: Record a foggy effort as a decision map settled across sessions, with options and a recommendation on each open question. Export it to the issue tracker or a file in the repo, then hand it to to-tickets or settle each open until the route is clear. A design, spec, or plan produced in one dialogue belongs to hld-planner. Applies the mapped entry state on a tracker export when a triage label map exists.
disable-model-invocation: true
---

# Wayfinder

Use this when an effort is too big and too unclear for one session. Find the route. Do not build the destination. Each open item is one decision. When nothing is left to decide, stop and hand the destination over.

When they want this session to produce a design, spec, HLD, or plan, tell them to run `hld-planner` and stop. Do not draft that design here.

The map lives where the human chooses after the draft: the repo issue tracker, or one file in the repo. A recommendation is a starting position. Charting resolves nothing. A yes writes the map. It does not settle any open question.

Refer to a tracker issue by its title, with the link inside the name. Refer to a local open by its question.

## Chart

The human brings a loose idea and no map.

1. Draft the map in chat. Wait for a yes before writing it anywhere. On an edit, apply it and show the draft again.
   - **Destination.** One or two lines. What done looks like: a spec, a locked decision, or a change someone else will make.
   - **Open.** Decisions you can already phrase as one question. Order them. Mark which are blocked by which. Each one has two or three options and one recommendation. The recommendation names the option and why, in one or two lines. A question you cannot give two real options is **Not yet specified**.
   - **Not yet specified.** In-scope areas you cannot phrase as a question yet.
   - **Out of scope.** Work this destination does not include.
   - **State.** When `.agent-repo-config/triage-label.md` maps `needs-triage`, the tracker string. Omit the line when it does not. A local file drops this line.

   Open item:

   ```markdown
   1. **<question>**
      - Blocked by: none | <earlier question>
      - Options:
        - A. <option>
        - B. <option>
      - Recommendation: A. <why>
   ```

2. If nothing is foggy and the route fits one session, do not create a map. Say so, and ask how they want to proceed.
3. Ask where to write it, unless the approval already said. Tracker, or a file in the repo. Then write that one.

### Tracker

Read `.agent-repo-config/issue-tracker.md` and follow it for create, read, comment, and close. To change a body, edit that same issue (`gh issue edit NUMBER --body` when the file says GitHub; otherwise update it the way that file says to create one). If the file is missing, stop and tell the human to run `setup-repo-skills`. When `.agent-repo-config/triage-label.md` maps `needs-triage`, apply that tracker string to every issue this skill creates. Apply no type unless the human names one. When the triage file is missing, create the issues with no triage label and do not ask. When the tracker file has no "apply a triage label" section, say so, tell the human to re-run `setup-repo-skills`, and create the issues with no triage label.

Create the map issue. Title: `Map: <short destination>`. Body:

```markdown
## Destination

<one or two lines>

## Decisions so far

## Open

## Not yet specified

- <area>

## Out of scope

- <work ruled out, and why>
```

Create one issue per open decision, with the same State label, then edit the map so **Open** lists them with real links. Ticket body:

```markdown
Map: #<map> <map title>

## Question

<the decision this ticket resolves>

## Options

- A. <option>
- B. <option>

## Recommendation

A. <why>

## Blocked by

- #<n> <title>
```

Write `None` when nothing blocks it. In **Open**, mark a ticket `ready` or `blocked by <title>`. The options stay on the decision issue. The map issue stays an index.

### Local

Write `.agent-docs/wayfinder-<slug>.md`. The slug is 2 to 4 kebab-case words from the destination. Create `.agent-docs/` if it is missing. If `.gitignore` does not already ignore `.agent-docs/`, add that line. If that file already exists, stop and ask. The body is the approved draft, headed `# Map: <short destination>`, without **State**. No tracker labels.

After it is written, name the path or the map link, then the two ways forward: hand it to `to-tickets`, or settle the opens. Copying the current map to the other home is a new write. Ask, then write. Do not close or delete the source.

## Next

They pick. Settle first when they want both.

- **Plan.** Tell them to run `to-tickets` and pass this map. Decisions so far are settled. Each recommendation is the working answer. Do not start `to-tickets`. Do not cut technical tickets here.
- **Settle.** Follow Continue. When they asked to settle everything, walk every ready open. Otherwise one open, then stop.

When no open decision remains, the plan handoff is the only next step.

## Continue

The human points at a map (number, URL, or path). An open item is optional.

1. Read the map. Re-read it before writing if it may have changed. A path is the local file. A number or URL is a tracker issue: read it the way the tracker file says.
2. Pick the open item. Use the one they named when it is open and every blocker is closed. Otherwise take the first ready entry under **Open**. Confirm a blocker is still open before skipping one. Read that item before settling. On the tracker, that is the decision issue.
3. Settle that one question with them. Show the options and the recommendation already on it. A short lookup or a rough sketch belongs in the same item when the question needs it. When the question is a preference, the answer is theirs. Wait for the reply before recording. Accepting the recommendation is a reply.
4. Record it.
   - **Tracker.** Comment the answer on the ticket, then close it. Move the line to **Decisions so far**: `- [<title>](link): <one-line gist>`. The gist is an index. The ticket holds the detail.
   - **Local.** Move the item to **Decisions so far**: `- <question>: <one-line gist>`. The gist is the answer. Drop the options.
   - Add an open item for each question the answer made precise, with options and a recommendation, and delete that line from **Not yet specified**. On the tracker, that item is a new issue with the same State label.
   - If an item sits past the destination, close it and add one line under **Out of scope** (gist, why, and the link when it is an issue). Leave it out of **Decisions so far**.
5. When they asked to settle everything, take the next ready open. Otherwise stop. Name the next ready open and the plan handoff.

Starting to build means the map has reached its edge, or this item is not a decision. Do not implement the destination here.
