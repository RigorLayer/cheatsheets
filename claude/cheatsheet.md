# Claude Code Cheat Sheet

## Models

Verified against official documentation on **September 17, 2026** (CLI v2.1.274).

Claude Code:
```text
/model [haiku|sonnet|opus|fable|best|opusplan]
```

Switch models on-the-fly without losing context.

| Model | Cost | Best For |
|-------|------|---------|
| **Haiku 4.5** | cheapest | Fast screening, data extraction, classification, simple coding tasks |
| **Sonnet 5** | balanced | Balanced coding, writing, code review, refactoring |
| **Opus 5** | advanced | Complex debugging, deep research, architectural decisions, advanced problem-solving |
| **Fable 5.1** | premium | Hardest long-horizon agentic work and the most demanding reasoning |

On the Anthropic API, `opus` selects Opus 5 and `sonnet` selects Sonnet 5; third-party provider aliases can lag. Pin a full model ID when version matters. `opusplan` plans with Opus, then executes with Sonnet.

`fable` selects **Fable 5.1** from v2.1.257, except through the Claude apps gateway, where it still selects Fable 5. Use `claude-fable-5-1` explicitly if your gateway serves it. `best` follows `fable` when available, otherwise `opus`.

**Tip:** `/model` saves your choice for future sessions. Press `s` in its picker for this session only, or launch with `claude --model fable`.

## Cost & Usage Control {: .page-break-before }

Claude Code:
```text
/usage   # Session cost, plan usage limits, activity stats
/cost    # Alias for /usage
```

`/usage` breaks the numbers down by what actually drives them — skill, subagent, plugin, and MCP server — which is usually how you find the surprise.

The three main cost levers: model, effort and context (see further).

**Tip:** Higher effort can increase token use. Check actual usage rather than assuming the same effort label has the same cost across models.

**Fable billing:** Some plans require usage credits. Interactive sessions ask for consent; `claude -p` and the Agent SDK can bill credits without that prompt. Check the model picker and your billing controls before automation.

Claude Code:
```text
/fast
```

Toggles fast mode (Opus 5 and Opus 4.8 only): up to 2.5x faster output at $10/$50 per MTok — same model, no downgrade. A `↯` icon marks it active.

**Tip:** On subscription plans fast mode bills from usage credits, not your plan allowance. Switching mid-session charges the full context at fast-mode uncached-input rates on the next request; earlier requests are not retroactively re-billed.

## Thinking Effort {: .page-break-before }

Claude Code:
```text
/effort [low|medium|high|xhigh|max|ultracode|auto]
```

Controls how much the model reasons before acting. Available levels depend on the model; `high` is the default on every model that supports effort, except Opus 4.7 which defaults to `xhigh`.

| Level | Examples |
|-------|---------|
| `LOW` | *“What's the node version?”, “Read this config file”* |
| `MEDIUM` | *“Add a helper function”, “Rename this variable across files”* |
| `HIGH` | *“Implement this feature”, “Debug this failing test”* |
| `XHIGH` | *“Refactor the entire auth module”* |
| `MAX` | *“Design the caching strategy”* |

`low` through `xhigh` persist across sessions. `max` and `ultracode` apply to the current session only — `ultracode` is not a model effort level but a Claude Code mode that sends `xhigh` and adds workflow orchestration (see *Dynamic Workflows*).

**Tip:** Include `ultrathink` anywhere in a prompt to request deeper reasoning for that one turn without changing the session's effort level.

## Headless Mode {: .page-break-before }

Run Claude Code without an interactive terminal:

```bash
claude -p "Write a commit message for these changes" < <(git diff --cached) 
claude -p "Convert this CSV to JSON" < data.csv > data.json
claude -p "Check this PR for security issues" < <(gh pr diff 42)
cat src/**/*.ts | claude -p "Find any TODO comments and list them" 
```

**Structured output** — use `--output-format json` for scripting:

```bash
claude -p "List imports in src/index.ts" --output-format json | jq '.result'
```

**Tips:**
* Output goes to `stdout` — use pipes and redirects
* `--output-format stream-json` — stream events in real time for long-running jobs
* `--allowedTools` — allow matching tools to run without approval; this is not a tool allowlist
* `--tools "Read,Grep,Glob"` — limit built-in tools to reads; add `--disallowedTools "mcp__*"` to exclude MCP tools too
* Combine with `-w` — headless + worktree keeps automation fully isolated from your working tree

## Context Management {: .page-break-before }

Claude Code:
```text
/context                 # Show current context usage
/clear                   # Start a new conversation (old one stays in /resume)
/compact [instructions]  # Summarize conversation to free up context
```

**Critical insight:** A large context window is capacity, not a guarantee that every detail gets equal attention. Keep important requirements easy to find.

* Keep active context tight — remove old conversation threads, unused MCPs, and dormant agents
* Use `/compact [instructions]` at a useful milestone to focus the summary
* Keep `CLAUDE.md` concise — cached instructions still occupy context

**Tip:** Automatic compaction helps long tasks continue. Keep durable decisions and next steps in plan files so you can also start a fresh session deliberately.

## Project Instructions {: .page-break-before }

Claude Code:
```text
/init      # Create or update CLAUDE.md
/memory    # Edit CLAUDE.md files; view and manage auto-memory entries
```

`CLAUDE.md` is like your project's README but for AI. Keep it under 150 lines. Place additional `CLAUDE.md` files in **subfolders** to scope instructions — Claude merges them hierarchically, applying only what's relevant to the files being edited.

**Auto memory** complements it: Claude records its own notes as it works — build commands, constraints, corrections — and reloads them in later sessions. Review or disable them from `/memory`.

**Tip:** Add the official `claude-md-improver` skill and use it.

**Tip:** Ask Claude explicitly to update `CLAUDE.md`, then review the change, or edit it through `/memory`.

```text
Add to CLAUDE.md: use pnpm and run tests after code changes.
```

**What belongs in CLAUDE.md**

| Include | Avoid |
|---|---|
| Tech stack and versions (`Node 22, pnpm, Vitest`) | Step-by-step tutorials or how-tos |
| Coding conventions (`snake_case` for DB columns) | Info already obvious from the code |
| Test and build commands | Full file listings or directory trees |
| Architectural decisions and their reasons | Duplicate content from README |
| What Claude must never do (`never edit migrations`) | More than ~150 lines total |
| Repo layout for non-obvious structures | Generic advice Claude already knows |

## Extensions & Automation {: .page-break-before }

Claude Code:
```text
/mcp       # Model Context Protocol (external tools & APIs)
/plugin    # Install & manage plugins (bundles of skills, agents, hooks)
```

**Skills** live in `.claude/skills/` and load into the session on demand. **Agents** (subagents) are defined in `.claude/agents/` and run isolated tasks in parallel.

| Aspect | Skills | Agents |
|--------|--------|--------|
| Session context | Shared (run in-session) | Isolated |
| Cost | Cheaper | Higher (separate context) |
| Feeds into session | Yes | Returns a summary |
| Parallelizable | No | Yes |
| Shields main context | No | Yes |

Custom commands are now skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Existing `commands/` files keep working — the skill form adds a folder for supporting files and lets Claude load it automatically when relevant.

**Bundled skills** ship with Claude Code and need no installation:

```text
/code-review      # Review the current diff for bugs and cleanups
/security-review  # Check the diff for security vulnerabilities
/simplify         # Apply clarity and reuse fixes to changed code
/batch            # Orchestrate large-scale changes across a codebase
/deep-research    # Fan out web searches into a cited report
/doctor           # Setup checkup that diagnoses and fixes issues
```

**Tip:** Explore public repositories like [skills.sh](https://skills.sh).

**Tip:** Use the official `skill-creator` skill to create and manage your own skills and agents.

## Review & CLI Updates {: .page-break-before }

```bash
claude --version           # Check the installed client
claude update              # Update Claude Code
claude ultrareview 123 --json  # Cloud review; findings to stdout
```

Claude Code:
```text
/code-review high          # Review without requesting fixes
/code-review --fix         # Apply review findings
/config --help             # Discover direct settings keys
```

Reviewing and publishing are separate actions: `/code-review --comment` posts findings; `claude ultrareview --post` posts to a GitHub PR. Omit posting flags when you only want a report.

**Recent changes:** v2.1.274 adds `CLAUDE_CODE_MCP_STARTUP_WAIT_MS` to bound the initial MCP wait in headless mode (`0` skips waiting). Use it only when the first turn can proceed without still-connecting tools. The release also fixes goals lost after resuming compacted sessions.

## Background Agents {: .page-break-before }

Claude Code:
```text
claude agents   # One screen for every session: running, blocked, done
/background     # Detach this session to the background (alias /bg)
/tasks          # List this session's background work
/fork [prompt]  # Copy this conversation into a new background session
/subtask        # Delegate a side task; its result returns here
```

Subagents run in the background by default, so Claude keeps working while they do. They can spawn their own subagents up to five levels deep, and their permission prompts surface in the main session instead of being auto-denied.

| `/fork` | `/subtask` |
|---|---|
| A new independent session | A subagent inside this conversation |
| Gets its own row in `claude agents` | Result returns to your context |
| Diverge and explore separately | Delegate one step and continue |

**Tip:** Use `/background` when a long build or migration no longer needs your terminal — reattach later from `claude agents` or `/resume`.

## Dynamic Workflows {: .page-break-before }

A workflow is a script Claude writes that orchestrates subagents deterministically — fan-out, loops, and verification stages instead of ad-hoc delegation. Reach for one when a task needs breadth (audits, migrations, sweeps) or confidence (independent review before you commit).

Claude Code:
```text
/effort ultracode   # Opt in for this session
/workflows          # Watch a running workflow's live progress
```

`ultracode` sends `xhigh` effort **and** has Claude author and run workflows for substantive tasks. Launch with it enabled via `claude --effort ultracode`.

**Tip:** A single workflow can spawn dozens of agents. Opt in deliberately, on tasks where thoroughness is worth the token cost.

## Checkpoints {: .page-break-before }

Claude Code:
```text
/rewind             # or ESC+ESC — roll back conversation + files
/branch [name]      # fork the conversation at this point
/diff               # interactive diff of uncommitted + per-turn changes
```

`/rewind` rolls back both file changes and conversation history to the state before a selected prompt. Use it when an approach goes wrong or before attempting something risky.

`/branch` saves the current conversation as a fork and switches you into it — return to the original anytime via `/resume`. Useful for what-if exploration without disturbing your main thread.

`/diff` opens an interactive viewer for uncommitted changes and per-turn edits. Left/right arrows step between turns, up/down browses files.

**Tip:** For persistent rollback across sessions, prefer git commits over relying on `/rewind`.

## Plan Mode

Claude Code:
```text
/plan
# or, Shift+TAB to cycle through modes
```

Planning mode **prevents the agent from making any code modifications** — use it to align on approach before writing code.

Claude creates a **markdown plan file** you can edit directly. It persists across sessions, making it useful for long or multi-phase tasks.

**Tip:** Before entering plan mode, ask Claude to interview you about requirements — prompt it with "ask me clarifying questions before creating the plan."

**Tip:** After the plan is created, stay in plan mode to iterate and refine it with new requirements.

## Side Questions

Claude Code:
```text
/btw <question>
```

Ask a quick question without adding the exchange to your main conversation history. Useful for *"what does this error mean?"* or *"is there a shortcut for X?"* while staying focused on your current task.

**Tip:** Pair with `/branch` for deeper exploration — `/btw` for one-off lookups, `/branch` when an answer might lead somewhere worth keeping.

## GitHub Integration

Have both `git` and `gh` tools installed if you work with GitHub.

```bash
gh auth login    # Authenticate once with your GitHub account
```

Claude Code can use `gh` commands to access PRs, issues, comments, and branches — more reliable than fetching GitHub pages via WebFetch.

**Tip:** Use `! gh <command>` to run GitHub commands inline and pull the output directly into context.

**Tip:** Ask Claude Code "Address all comments in PR #123."

## Running Bash Commands

```bash
! node --version      # Check node version
! npm install         # Run package manager
! git log --oneline   # View recent commits
```

**Tip:** Prefix any bash command with `!` to execute it in the session and pull output into context.

## Referencing Files & Context

Type `@` to open an interactive file picker and reference files, folders, or URLs directly in your message.

```text
Update my @README.md           # Reference a single file
Debug the issue in @src/       # Reference an entire folder
Implement this @https://...    # Pull web content into context
```

**Tip:** Explicit references prevent the agent from scanning unnecessary code and focus it on what actually matters.

## Hooks {: .page-break-before }

Configure `settings.json` to automate recurring behaviors. Key hook events: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Stop`, `SubagentStop`, `PreCompact`, `Notification` — 30+ events total covering sessions, subagents, files, and worktrees.

Hooks receive the event as JSON on `stdin`; exit code `2` blocks the action and feeds `stderr` back to Claude. Example — block reading `.env` files:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys; d=json.load(sys.stdin); sys.exit(2 if '.env' in d['tool_input'].get('file_path','') else 0)\""
          }
        ]
      }
    ]
  }
}
```

**Tip:** Use the `/update-config` skill to manage hooks safely. Powerful for enforcing code standards without manual intervention.

## Tool Permissions {: .page-break-before }

Claude Code:
```text
/permissions
```

Manage allow/ask/deny rules for tool calls, scoped per-project or globally. The interactive dialog lets you review rules, add or remove entries, manage working directories, and inspect recent auto-mode denials.

**Auto mode** is the middle ground between approving every prompt and `--dangerously-skip-permissions`: a classifier reviews each action, so safe ones run uninterrupted and risky ones are blocked. Cycle to it with Shift+Tab. Deny rules still apply unconditionally, and it refuses destructive git commands and `rm -rf` on unresolved variables.

Claude Code can also run **Bash in a sandbox**, restricting filesystem and network access so routine commands need no approval at all.

**Tip:** Run `/fewer-permission-prompts` (bundled skill) to scan recent transcripts and add safe read-only commands to your project allowlist automatically.

## Multi-Session Workflows {: .page-break-before }

Long projects span multiple sessions — context resets each time. Strategies to maintain continuity:

* Use `/plan` to create a plan file — it persists across sessions and serves as the source of truth
* Use `CLAUDE.md` to document decisions, conventions, and current state that Claude should always know
* End sessions with `/compact [instructions]` to preserve a focused summary before closing
* Use auto-memory (`~/.claude/projects/`) to store learnings, preferences, and past decisions
* Use `/resume [session]` to pick up a prior conversation by ID, name, or via the picker — or `claude --continue` to resume the most recent one from the CLI

Claude Code:
```text
/goal <condition>   # Keep working across turns until the condition holds
/goal clear         # Drop the current goal
```

A goal outlives individual turns: instead of stopping when a reply is done, Claude keeps going until the stated condition is met. Best paired with a condition you can actually check — *“the test suite passes”*, not *“the code is good”*.

**Tip:** At the start of a new session, reference the plan file explicitly: `@plan.md what's next?`

## Worktrees {: .page-break-before }

Run Claude in an isolated git worktree so it works on a separate branch without touching your working directory:

```bash
claude -w                     # auto-named worktree + branch
claude -w feature-auth        # named worktree "feature-auth"
```

**Why use worktrees?**

* **Keep working while Claude codes** — your editor stays on your branch, Claude works on its own
* **Parallel tasks** — spin up multiple Claude sessions on different features simultaneously
* **Safe experimentation** — Claude's changes are fully isolated; discard the branch if you don't like the result
* **Clean PRs** — each worktree produces a focused branch ready for review

**Tip:** Combine with background agents or a scheduled routine (see below) to let Claude work on a feature branch while you stay productive on `main`.

## Scheduling & Recurring Work {: .page-break-before }

For work that repeats — morning PR reviews, overnight CI triage, weekly dependency audits — run Claude on a schedule instead of remembering to.

| Option | Runs on | Use for |
|---|---|---|
| **Routines** | Anthropic infrastructure | Schedules that must fire with your machine off; also triggered by GitHub events or an API call |
| **Desktop scheduled tasks** | Your machine | Jobs that need local files, tools, or credentials |
| **`/loop`** | The current session | Quick polling while a session stays open |

```text
/schedule                 # Create or manage a routine
/loop 10m /babysit-prs    # Re-run a prompt or command on an interval
```

Routines are templated, and each firing starts a fresh cloud session — create them with `/schedule`, from the Desktop app, or on the web.

**Tip:** Omit the interval and `/loop` paces itself: `/loop check whether the deploy finished`.

## MCP (Model Context Protocol) {: .page-break-before }

MCP servers extend Claude's capabilities by giving it access to external tools, APIs, and data sources.

**Add an MCP server**

```bash
claude mcp add <name> -- <command> [args...]    # stdio (local process)
claude mcp add --transport http <name> <url>    # HTTP (remote server)
```

Examples:
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp remove context7
claude mcp list
```

**Tip:** Add `--scope project` to share configuration through `.mcp.json`. The default is `local` (only you, in this project); `--scope user` makes it available across your projects.

**Popular, battle-tested MCP servers**

| Server | What it gives Claude | Install |
|---|---|---|
| [Context7](https://github.com/upstash/context7) | Up-to-date library & framework docs | `npx -y @upstash/context7-mcp` |
| [GitHub](https://github.com/github/github-mcp-server) | Read/write issues, PRs, repos | `--transport http https://api.githubcopilot.com/mcp/` |
| [Playwright](https://github.com/microsoft/playwright-mcp) | Browser automation & scraping | `npx @playwright/mcp@latest` |
| [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | Sandboxed file access | `npx -y @modelcontextprotocol/server-filesystem <path>` |

**Tip:** Reference an MCP tool explicitly in your prompt — `use context7 to look up the Prisma API` — to ensure Claude reaches for it.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `@` | File picker (fuzzy search) |
| `!command` | Run shell command inline |
| Esc×2 | Clear a draft; with empty input, open rewind |
| Shift+Tab | Cycle modes (normal / plan / accept-edits / auto) |
| Ctrl+G | Open external editor |
| Ctrl+L | Clear screen |
| Ctrl+C | Interrupt; when idle, clear input, then press again to exit |
| Ctrl+O | Toggle detailed transcript |

**Tip:** Run `/keybindings` to open your shortcuts file and remap keys, including two-key chords.

## Prompt Techniques

Patterns that consistently produce better results:

* **"Show me your plan first"** — ask Claude to outline its approach before writing any code
* **"Don't change anything else"** — prevents scope creep on targeted fixes
* **"Think step by step"** — improves reasoning on complex or multi-part problems
* **"Ask me clarifying questions before starting"** — surfaces ambiguities early
* **"What are the risks of this approach?"** — prompts Claude to self-critique before committing
* **Narrow the scope** — "only modify `auth.ts`" is clearer than "fix the auth bug"
* **Provide examples** — "format the output like this: ..." produces more predictable results

## Beyond the Terminal {: .page-break-before }

Claude Code runs on multiple surfaces. Repository instructions travel with the repository; local settings, credentials, and MCP configurations may need separate setup in cloud environments.

| Surface | Best for |
|---|---|
| **Terminal** | The full CLI: scripting, headless automation, everything in this guide |
| **VS Code / JetBrains** | Inline diffs, @-mentions, and plan review inside the editor |
| **Desktop app** | Visual diff review, side-by-side sessions, scheduled tasks |
| **Web** | Long-running cloud tasks and repos you don't have locally |
| **Mobile** | Kicking off work and answering prompts away from your desk |

Move a session between them:

```text
/desktop          # Continue this session in the Desktop app
/teleport         # Pull a web session into this terminal
/remote-control   # Drive this local session from another device
claude --cloud    # Start local, hand off to web and mobile
```

**Tip:** Kick off a long task with `claude --cloud` before you leave, follow it from your phone, then pull it back into the terminal with `/teleport`.

## Useful Links {: .page-break-before }

**Documentation**

* [Claude Code Docs](https://code.claude.com/docs) — official Anthropic documentation
* [Models](https://code.claude.com/docs/en/model-config) — aliases, effort, and billing caveats
* [CLI reference](https://code.claude.com/docs/en/cli-reference) and [commands](https://code.claude.com/docs/en/commands)
* [Changelog](https://code.claude.com/docs/en/changelog) — client releases and fixes

**General**

* [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) — curated list of resources, tips, and projects

**Skills**

* [agentskills.io](https://agentskills.io) — the open Agent Skills standard
* [skills.sh](https://skills.sh) — public skill registry
* [anthropics/skills](https://github.com/anthropics/skills) — official Anthropic skills repository
* [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — community-curated skill collection

**Subagents**

* [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — curated subagent collection

**MCP**

* [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — official MCP server collection

---

Claude Code Cheat Sheet version 1.7
© 2026 Andrei Smirnov — [github.com/pinebit](https://github.com/pinebit)
