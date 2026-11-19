# Checkup

`<ws>` is the workspace root. Run every section. Record the command you ran for each finding.

## Installation

- `cursor --version`, and `agent --version` or `agent about`. `which -a cursor` and `which -a agent`. Warn on a PATH entry that appears twice or points at two different binaries.
- `agent status` or `agent whoami`. Fail when not signed in.
- Whether a newer CLI exists. Read it from the CLI's own output or release info. Do not run `agent update`.
- Parse as JSON and Fail on any that does not parse, with the parser's error:
  - `~/.cursor/cli-config.json`, `<ws>/.cursor/cli.json`
  - `~/.cursor/mcp.json`, `<ws>/.cursor/mcp.json`, and any other `mcp.json` the CLI reports
  - `~/.cursor/hooks.json`, `<ws>/.cursor/hooks.json`

A missing file is not a failure. Say it is absent.

## Always-loaded instructions

Find: `<ws>/.cursor/rules/**`, `~/.cursor/rules/**`, every `AGENTS.md`, `CLAUDE.md`, and `CLAUDE.local.md` in the tree, legacy `.cursorrules`, and user rules stored as files under `~/.cursor`.

For each: path, bytes, lines, and whether it is always applied, glob-scoped, or on request (from the rule frontmatter). Warn on:

- A file over about 200 lines, or an always-loaded total that is large next to a typical context window. Give the total.
- A local file that repeats a checked-in one.
- Content the agent can derive from the repo: directory trees, dependency lists, architecture tours. Content that must stay: pitfalls, and conventions that differ from defaults.
- Instructions that contradict each other, name a file or command that does not exist (check it), or target an older tool.

Do not rewrite. Propose trims, or moves into an on-demand skill or a path-scoped rule.

## Skills

Inventory: `<ws>/.cursor/skills`, `<ws>/.agents/skills`, `~/.cursor/skills`, `~/.cursor/skills-cursor`, `~/.agents/skills`, and skills shipped by installed plugins (under `~/.cursor/plugins/`). Resolve symlinks and report the target.

For each: name, path, description length, `SKILL.md` body size. Warn on:

- Missing or invalid frontmatter.
- A folder name that differs from `name`.
- A description over 1024 characters, or one too vague to say when to use it.
- A body over about 5000 tokens (about 20 KB).
- The same name in more than one scope. Say which copy wins.

Estimate the per-turn cost of the skill listing: the sum of names and descriptions of every model-invocable skill. Name the five largest contributors. Do not disable anything.

## MCP

- `agent mcp list`. Include the error for any server that fails.
- For each server: name, scope (user or project), transport, connected or not. For a required env var, say set or unset only.
- Fail on a server that does not connect. Warn on a tool name exposed by two servers, and on a server with a very large tool list.
- Call nothing on a server except a list or status call.

## Hooks

- From both `hooks.json` files: event, command, scope.
- Fail on a script that is missing or not executable. Warn on an obvious syntax error, found by reading or by `bash -n` / `python -m py_compile`. Do not run the script.
- When a hooks log or terminal output is available, note failures and any hook with a multi-second startup.

## Permissions and sandbox

From `~/.cursor/cli-config.json` and `<ws>/.cursor/cli.json`:

- Permission mode, and allow and deny lists, summarised.
- Warn on an empty allowlist, which prompts on every read-only command.
- Warn on an allow rule broad enough to cover writes or network with no clear reason.
- The sandbox and network mode, when set.
