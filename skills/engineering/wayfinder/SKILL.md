---
name: wayfinder
description: Chart a large, foggy effort as decision tickets on the repo issue tracker, and settle one decision per session until the route is clear enough to implement.
disable-model-invocation: true
---

# Wayfinder

Use this when an effort is too big and too unclear for one session. Find the route. Do not build the destination. Each ticket is one decision. When nothing is left to decide, stop and hand the destination over.

The map and its tickets are issues in the repo under discussion. Read `.agent-repo-config/issue-tracker.md` and follow it for create, read, comment, and close. To change a body, edit that same issue (`gh issue edit NUMBER --body` when the file says GitHub; otherwise update it the way that file says to create one). If the file is missing, stop and tell the human to run `setup-repo-skills`.

Refer to every issue by its title, with the link inside the name.

## Chart

The human brings a loose idea and no map.

1. Draft the map in chat. Wait for a yes or an edit before creating any issue.
   - **Destination.** One or two lines. What done looks like: a spec, a locked decision, or a change someone else will make.
   - **Open.** Decisions you can already phrase as one question. Order them. Mark which are blocked by which.
   - **Not yet specified.** In-scope areas you cannot phrase as a question yet.
   - **Out of scope.** Work this destination does not include.
2. If nothing is foggy and the route fits one session, do not create a map. Say so, and ask how they want to proceed.
3. Create the map issue. Title: `Map: <short destination>`. Body:

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

4. Create one issue per open decision, then edit the map so **Open** lists them with real links. Ticket body:

```markdown
Map: #<map> <map title>

## Question

<the decision this ticket resolves>

## Blocked by

- #<n> <title>
```

Write `None` when nothing blocks it. In **Open**, mark a ticket `ready` or `blocked by <title>`. Charting resolves nothing.

## Continue

The human points at a map (number or URL). A ticket is optional.

1. Read the map. Re-read it before writing if it may have changed.
2. Pick the ticket. Use the one they named when it is open and every blocker is closed. Otherwise take the first ready entry under **Open**. Confirm a blocker is still open before skipping a ticket.
3. Settle that one question with them. A short lookup or a rough sketch belongs in the same ticket when the question needs it. When the question is a preference, the answer is theirs.
4. Record it:
   - Comment the answer on the ticket, then close it.
   - Move the line to **Decisions so far**: `- [<title>](link): <one-line gist>`. The gist is an index. The ticket holds the detail.
   - Add a ticket for each question the answer made precise, and delete that line from **Not yet specified**.
   - If a ticket sits past the destination, close it and add one line under **Out of scope** (gist, why, link). Leave it out of **Decisions so far**.
5. Stop. One ticket per session.

Starting to build means the map has reached its edge, or this ticket is not a decision. Do not implement the destination here. When no open decision remains, tell the human to run `to-tickets` to cut the destination into implementation tickets.
