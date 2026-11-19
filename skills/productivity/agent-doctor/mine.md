# Mine

Read only the human's chats for this workspace, from the last N days.

## Sources

Try them in this order. Use every one that works, and dedupe a chat seen twice.

1. **Agent transcripts.** `~/.cursor/projects/<slug>/agent-transcripts/*.jsonl`, where the slug is the workspace path with `/` replaced by `-` and the leading `-` dropped (`/Users/me/code/app` becomes `Users-me-code-app`). One file per chat. Filter by file mtime.
2. **Cursor databases.** The user data folder is `~/Library/Application Support/Cursor/User/` on macOS, `~/.config/Cursor/User/` on Linux, and `%APPDATA%\Cursor\User\` on Windows.
   - Find this workspace: the `workspaceStorage/<hash>/workspace.json` whose `folder` is this workspace's URI. Its `state.vscdb` table `ItemTable` lists the workspace's composer ids.
   - Messages live in `globalStorage/state.vscdb`, table `cursorDiskKV`: `composerData:<composerId>` for each chat, and `bubbleId:<composerId>:<bubbleId>` for each message.
   - Copy each `state.vscdb` to a temp folder first. Read the copy with `sqlite3` or a short Python script. Schemas change between versions. When a key is missing, list the key prefixes and adapt. Do not stop.

Only the human's messages carry corrections and requests. Read the agent's replies only to tell what was done.

## Find

Each item is a fact the human would not see from one chat, plus the evidence: how many chats, and one short paraphrased example. Drop any secret, token, or customer data.

Then decide the action. A to-do exists only when a specific change follows: the file to add or edit, and what it should say. When the fact is already covered, or the right move is to do nothing, say so and name the thing that covers it. Do not invent a to-do to fill the section.

- **Knowledge (3-5).** A correction or explanation the human gave more than once. The line that belongs in a project rule under `.cursor/rules` or `AGENTS.md`, glob-scoped to a folder when it only applies there. Skip it when a rule or skill already says it, and name that file.
- **Skills (3-5).** A multi-step job asked for more than once. Name, when to use it, and the steps as they were actually done. When an installed skill already covers it, name that skill and give no to-do.
- **Subagents (3-5).** A part of those jobs that reads a lot or can run alone. Name, what it does, read-only or not, and whether a cheaper model is enough.
- **Surprising (3-5).** A pattern the human probably does not see: a time sink, a repeated mistake, something re-explained. Often this only adds context to an item above. Point at that item's to-do instead of making a second one.

Fewer than three real items in a section is fine. Do not pad.

Every item gets a priority (P1, P2, P3) and an impact (High, Medium, Low).
