# Codex CLI Cheat Sheet

## Install & Login

Install Codex CLI:
```bash
npm i -g @openai/codex
# or
brew install --cask codex
```

Start Codex in the current repository:
```bash
codex
```

The first run prompts you to sign in with ChatGPT or use an API key. ChatGPT Plus, Pro, Business, Edu, and Enterprise plans include Codex access.

**Tip:** Keep the CLI current:
```bash
npm i -g @openai/codex@latest
codex update
codex --version
```


## Models & Reasoning

Codex CLI:
```text
/model      # Change model and, for supported models, reasoning level
/status     # Confirm active model, reasoning level, context, sandbox, approvals
/fast       # Toggle fast mode on supported models
```

Switch models and reasoning effort mid-session without losing context.

Command line:
```bash
codex --model gpt-5.6
codex -m gpt-5.6-terra "Review this repository"
codex -m gpt-5.6-sol -c model_reasoning_effort='"high"'
codex exec -m gpt-5.6-luna -c model_reasoning_effort='"low"' "Review this diff"
```

| Model | Cost | Best For |
|-------|------|----------|
| **GPT-5.6 Sol** (`gpt-5.6-sol`, alias `gpt-5.6`) | highest | Complex coding, computer use, research, cybersecurity, polished deliverables |
| **GPT-5.6 Terra** (`gpt-5.6-terra`) | balanced | Everyday implementation, debugging, review, and tool-heavy work |
| **GPT-5.6 Luna** (`gpt-5.6-luna`) | lowest in family | Fast, repeatable tasks such as extraction, classification, and transformation |
| **GPT-5.5** (`gpt-5.5`) | previous generation | Existing complex coding and research workflows |
| **GPT-5.3 Codex Spark** (`gpt-5.3-codex-spark`) | preview | Near-instant, text-only coding iteration; ChatGPT Pro only |
| **GPT-5.4 / GPT-5.4 Mini** | lower-cost alternatives | Professional work or responsive coding and subagents |

**Tip:** Start with Sol when unsure, use Terra as the everyday workhorse, and choose Luna when the task is clear and repeatable. Availability depends on your plan, workspace, and model provider.

Configure the default in `~/.codex/config.toml`:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
model_reasoning_summary = "auto"
```

| Setting | Values | Notes |
|---------|--------|-------|
| `model_reasoning_effort` | `minimal`, `low`, `medium`, `high`, `xhigh` | Responses API only; supported models only; `xhigh` is model-dependent |
| `model_reasoning_summary` | `auto`, `concise`, `detailed`, `none` | Controls visible reasoning summaries, not how much reasoning the model does |
| `plan_mode_reasoning_effort` | `none`, `minimal`, `low`, `medium`, `high`, `xhigh` | Overrides reasoning only for Plan Mode |

| Effort | Use For |
|--------|---------|
| `minimal` | Fast formatting, small lookups, trivial edits |
| `low` | Reading config, simple fixes, command output summaries |
| `medium` | Default everyday coding and review work |
| `high` | Debugging, multi-file implementation, careful refactors |
| `xhigh` | Hard design/debugging work when the selected model supports it |

GPT-5.6 also exposes two top-end choices in the model picker:

| Mode | Behavior |
|------|----------|
| **Max** | Gives one model more time to reason about the hardest tasks |
| **Ultra** | Uses subagents to split a complex task into parallel workstreams |

**Tip:** Use the lowest effort that produces the result you need. Most tasks do not need Max or Ultra, and Ultra can increase usage quickly.



## Cost & Usage Control

Codex CLI:
```text
/usage        # Token activity, account usage, and available reset credits
/status       # Model, context, token usage, sandbox, approvals, writable roots
/fast         # Toggle fast service tier when the selected model supports it
```

Main cost levers:

| Lever | Lower Cost | Higher Capability |
|-------|------------|-------------------|
| Model | GPT-5.6 Luna / GPT-5.4 Mini | GPT-5.6 Sol |
| Reasoning | `minimal`, `low`, or `medium` | `high`, `xhigh`, Max, or Ultra |
| Context | Compact and reference fewer files | Large repo scans and long history |
| Subagents | Single-threaded run | Parallel workers and explorers |

**Tip:** Subagents do their own model and tool work. They are useful for parallel review or implementation, but they cost more than a comparable single-agent run.

Open a specific usage view directly:
```text
/usage daily
/usage weekly
/usage cumulative
```



## Headless Mode

Run Codex without the interactive terminal UI:

```bash
codex exec "Write a commit message for these changes" < <(git diff --cached)
codex exec "Convert this CSV to JSON" < data.csv > data.json
codex exec "Summarize the last 10 commits" | tee release-notes.md
cat logs.txt | codex exec "Find the likely root cause"
```

**Structured output** - use `--json` for JSONL events:

```bash
codex exec --json "Summarize the repo structure" | jq
```

**Final response file** - save the last agent message:

```bash
codex exec -o summary.md "Summarize open risks in this repo"
```

**Tips:**
* `codex exec` streams progress to `stderr` and writes the final message to `stdout`
* Default sandbox for `codex exec` is read-only
* Use `--sandbox workspace-write` when automation must edit files
* Use `--ephemeral` when you do not want session files persisted
* Use `--output-schema schema.json` when a script needs a structured final answer



## Context Management

Codex CLI:
```text
/status    # Context and token usage
/compact   # Summarize conversation to free tokens
/clear     # Clear terminal and start a fresh chat
/new       # Start a new conversation inside the same CLI session
```

**Critical insight:** Large contexts create the same "lost in the middle" failure mode in coding agents as in chat. Keep the working set tight.

* Use `/compact` before the context is nearly full
* Reference exact files with `@` or `/mention` instead of asking Codex to scan the whole repo
* Move durable project facts into `AGENTS.md`
* Use `/status` to watch context and token usage during long runs
* Use `/side` for quick side questions that should not derail the main thread

**Tip:** When a task gets long, ask Codex to write a short handoff plan into a repo file, then start a fresh session that references that file.



## Project Instructions

Codex CLI:
```text
/init       # Generate an AGENTS.md scaffold
/status     # Confirm loaded configuration and working root
```

`AGENTS.md` is the persistent instruction file Codex reads before doing work.

| Scope | Location | Notes |
|-------|----------|-------|
| **Global** | `~/.codex/AGENTS.md` | Personal defaults for every repo |
| **Global override** | `~/.codex/AGENTS.override.md` | Temporary global override |
| **Repository** | `./AGENTS.md` | Team conventions and project setup |
| **Nested override** | `path/to/AGENTS.override.md` | More specific rules for a subfolder |

Discovery order:
1. Global `AGENTS.override.md`, otherwise global `AGENTS.md`
2. Repo root down to current directory
3. Per-directory `AGENTS.override.md`, otherwise `AGENTS.md`, otherwise configured fallback names

Codex concatenates instructions from broad to specific. Files closer to the current directory appear later and override earlier guidance.



**What belongs in AGENTS.md**

| Include | Avoid |
|---|---|
| Build, lint, test commands | Full tutorials |
| Package manager and runtime versions | Obvious repo facts |
| Coding conventions | Huge directory listings |
| Known risky files or boundaries | Secrets or credentials |
| Review and PR expectations | Generic AI advice |
| Non-obvious architecture decisions | Stale project history |

**Tip:** Keep instructions concise. Codex stops loading project docs once the combined instruction size reaches `project_doc_max_bytes` (32 KiB by default).



## Memories

Control cross-session memory from the TUI:

```text
/memories    # Use existing memories, generate new ones, or disable memory
```

Memories can retain useful preferences, recurring workflows, tech stacks, and repository conventions. They complement `AGENTS.md`: memory is personal and adaptive, while `AGENTS.md` is explicit, reviewable, and shareable with the repository.

**Tip:** Keep build commands, safety rules, and team conventions in `AGENTS.md`. Memory is off by default in the European Economic Area, the United Kingdom, and Switzerland.



## Configuration

Codex configuration lives in TOML:

```toml
# ~/.codex/config.toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
approval_policy = "on-request"
default_permissions = ":workspace"
```

Configuration precedence, highest first:

| Priority | Source |
|----------|--------|
| 1 | CLI flags and `--config` overrides |
| 2 | `--profile <name>` values |
| 3 | Project `.codex/config.toml` files, closest wins |
| 4 | User `~/.codex/config.toml` |
| 5 | System `/etc/codex/config.toml` |
| 6 | Built-in defaults |

One-off overrides:

```bash
codex --model gpt-5.6-terra
codex --config model='"gpt-5.6-terra"'
codex --add-dir ../shared
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

Profiles:
```toml
[profiles.deep-review]
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
approval_policy = "on-request"

[profiles.quick-fix]
model = "gpt-5.6-luna"
model_reasoning_effort = "low"
approval_policy = "untrusted"
```

```bash
codex --profile deep-review
```

**Tip:** Use `/debug-config` when a setting does not behave the way `config.toml` suggests. It prints active config layers and policy constraints.

**Tip:** `default_permissions` is the current profile-based permissions setting (`:read-only`, `:workspace`, or `:danger-full-access`). Do not combine it with legacy `sandbox_mode` or `[sandbox_workspace_write]` settings in the same config.



## Sandbox & Approvals

Start Codex with explicit safety settings:

```bash
codex --sandbox read-only --ask-for-approval untrusted
codex --sandbox workspace-write --ask-for-approval on-request
codex --sandbox danger-full-access --ask-for-approval never
```

Interactive control:
```text
/permissions
/approve       # Retry one recent action denied by automatic review
/status
```

| Sandbox | Behavior |
|---------|----------|
| `read-only` | Inspect files; edits and most commands need approval |
| `workspace-write` | Write inside the workspace and approved writable roots |
| `danger-full-access` | No sandbox. Use only in external isolation |

| Approval Policy | Behavior |
|-----------------|----------|
| `untrusted` | Only trusted/read-only commands run without asking |
| `on-request` | Codex decides when to ask for approval |
| `never` | No approval prompts; failures are returned to the model |

**Tip:** The practical default for local coding is:
```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

**Warning:** `--dangerously-bypass-approvals-and-sandbox` skips both approval prompts and sandboxing. Use it only inside a throwaway container, VM, or CI runner.



## Plan Mode

Codex CLI:
```text
/plan [prompt]
```

Plan mode asks Codex to propose an execution plan before implementation work starts. Use it when requirements are ambiguous, blast radius is high, or the work touches shared architecture.

**Tips:**
* Ask Codex to interview you before creating the plan
* Use `/plan` before broad refactors, migrations, and production-sensitive fixes
* Exit plan mode only after the scope and verification steps are concrete



## Goal Mode

Attach a durable objective to the active task:

```text
/goal Finish the migration and keep tests green
/goal          # View the current goal
/goal edit     # Revise it
/goal pause    # Pause goal progress
/goal resume   # Continue working toward it
/goal clear    # Remove it
```

Goal mode is for work that should continue toward a concrete outcome across long runs. Objectives can be up to 4,000 characters; put longer instructions in a file and point the goal at that file.

**Tip:** Keep the goal outcome-focused. Put detailed constraints and checklists in `AGENTS.md` or a referenced task file.



## Checkpoints & Session Control

Codex CLI:
```text
/diff       # Show Git diff, including untracked files
/review     # Ask a separate Codex agent to review local changes
/fork       # Branch the conversation into a new thread
/resume     # Resume a saved conversation
/side       # Start an ephemeral side conversation
/rename     # Give the current task a recognizable name
/archive    # Archive the session and exit; keep its transcript
/delete     # Permanently delete the session and descendant sessions
/app        # Continue this session in the ChatGPT desktop app
/copy       # Copy latest completed Codex output
/quit       # Exit the CLI
```

Shell commands:
```bash
codex resume             # Open session picker
codex resume --last      # Continue most recent session
codex fork               # Fork from a previous session
codex archive <SESSION>  # Hide a saved session without deleting it
codex unarchive <SESSION>
codex app .              # Open this workspace in the ChatGPT desktop app
codex apply              # Apply the latest diff from a Codex agent
```

**Tip:** Use `/diff` before every commit. For persistent rollback, prefer small git commits over relying on session history.



## Code Review

Interactive:
```text
/review
```

Headless:
```bash
codex review --uncommitted
codex review --base main
codex review --commit abc123
codex review --base main "Focus on auth, data loss, and missing tests"
```

`codex review` runs a non-interactive review agent against local changes, a base branch, or a commit.

**Tip:** Review after implementation but before cleanup. The second agent is best at catching behavioral risks while the diff still reflects the actual change.



## Running Bash Commands

Inside the TUI, ask Codex to run commands naturally:

```text
Run npm test
Check the current branch
Start the dev server and inspect the console output
```

Or prefix a line with `!` to run it directly under the current approval and sandbox settings:

```bash
! npm test
! git status --short
```

Useful session commands:
```text
/ps       # Show background terminals
/stop     # Stop background terminals
```

Command-line sandbox helper:
```bash
codex sandbox <command>
```

**Tip:** Prefer asking Codex to run the exact verification command, for example "run `pnpm test -- --runInBand` and fix only failures caused by this change."



## Referencing Files & Context

Type `@` or use `/mention` to attach files and folders.

```text
Update @README.md
Debug the issue in @src/auth/
Compare @old-api.md and @new-api.md
Use @screenshot.png to implement the UI
```

Command line image input:
```bash
codex -i screenshot.png "Implement this design"
codex exec -i error.png "Explain this stack trace"
```

**Tip:** Explicit references reduce unnecessary repo scanning and make the agent's first turn much more reliable.



## Web Search

Codex CLI:
```bash
codex --search "Check the latest migration guide and update this dependency"
```

Codex can use cached web search for local tasks and live browsing when enabled. Treat web results as untrusted input, especially when they influence shell commands or dependency installation.

**Tip:** Mention the source you want, for example "use official React docs" or "use the OpenAI docs MCP server."



## Desktop, Cloud & Remote

Move between the terminal and the ChatGPT desktop app:

```bash
codex app .       # Launch the desktop app for this workspace
```

```text
/app              # Continue the current saved task in the desktop app
```

The desktop app can edit Markdown and code directly, annotate selections, review GitHub pull requests beside the diff, and group multiple repositories in one project.

Browse or submit Codex cloud tasks from the terminal (experimental):

```bash
codex cloud
codex cloud exec --env ENV_ID --attempts 2 "Fix the failing integration tests"
codex cloud list --json
codex apply       # Apply the latest cloud-task diff locally
```

Experimental remote control for managed mobile and SSH workflows:

```bash
codex remote-control start
codex remote-control pair
codex remote-control stop
```

**Tip:** Pairing codes are short-lived. Update both Codex and the ChatGPT mobile or desktop app before troubleshooting a failed connection.



## Extensions & Automation

Codex CLI:
```text
/skills      # Browse and insert a reusable skill
/apps        # Browse connectors and insert an $app-slug mention
/plugins     # Browse installed and discoverable plugins
/hooks       # Inspect, trust, enable, or disable lifecycle hooks
/mcp         # List active MCP servers and tools; add verbose for diagnostics
/agent       # Switch active agent thread; alias /subagents
```

Shell:
```bash
codex plugin list
codex plugin add <plugin@marketplace>
codex plugin marketplace list
codex mcp list
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

| Aspect | Skills | Subagents | Apps | MCP |
|--------|--------|-----------|------|-----|
| Purpose | Reusable workflows | Parallel specialized agents | Authorized workspace connectors | External tools and context |
| Invocation | `$skill-name`, `/skills`, or automatic | Explicit request to spawn agents | `$app-slug` or `/apps` | Tool selected by Codex |
| Context | Loaded progressively | Separate agent context | Private connected data and actions | External server context |
| Best For | Repeatable project workflows | Parallel review or implementation | Slack, Google Drive, Notion, and similar services | Docs, GitHub, browser, Figma, databases |
| Cost | Low overhead | Higher token usage | Depends on actions | Depends on tools called |

**Tip:** Use skills for repeatable procedures, subagents for parallel work, apps for authorized workspace data, and MCP for custom external systems.


**Common layout**

```text
<repo>/
  .agents/
    skills/
      my-skill/
        SKILL.md
        scripts/
        references/
        assets/
  .codex/
    agents/
      api-reviewer.toml
    config.toml
    hooks.json
  AGENTS.md
```



## Apps (Connectors)

Browse connected apps and insert one into your prompt:

```text
/apps
$app-slug Find the source document and summarize the open decisions.
```

Apps provide authorized access to private workspace data and actions. Availability depends on your ChatGPT plan, app authorization, workspace policy, and the current surface.

App tools can use these approval modes: `auto`, `prompt`, `writes`, or `approve`. The `writes` mode allows declared read-only actions and prompts before writes.

**Tip:** If an app is missing, check that it is authorized and allowed by your workspace before debugging MCP or model settings.



## Skills

Create with the built-in skill:
```text
$skill-creator
```

Invoke explicitly:
```text
/skills
$documents Create a polished one-page brief from @notes.md
$skill-creator Create a skill for our release process
```

Common locations:

| Scope | Location |
|-------|----------|
| Repository | `.agents/skills/` |
| User | `~/.agents/skills/` |
| Plugin | Bundled inside an installed plugin |

**Tip:** The `description` in `SKILL.md` is the trigger. Make it concrete: say when the skill should and should not be used.



## Subagents

Ask Codex explicitly to spawn subagents:

```text
Review this PR with parallel agents:
one for security, one for correctness, one for tests.
Wait for all results and summarize.
```

Built-in agent roles:

| Agent | Best For |
|-------|----------|
| `default` | General work |
| `explorer` | Read-heavy codebase investigation |
| `worker` | Implementation and bug fixes |

Required fields:
```toml
name = "api-reviewer"
description = "Reviews API changes for compatibility and migration risks."
developer_instructions = "Focus on request/response compatibility, auth, and versioning."
```

**Tip:** Subagents inherit the parent sandbox and approval settings. Approval prompts can surface from inactive agent threads.



## MCP (Model Context Protocol)

MCP gives Codex access to external tools and context.

Add servers:
```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
codex mcp get context7
codex mcp remove context7
```

In the TUI:
```text
/mcp
```

Config shape:
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.docs]
url = "https://developers.openai.com/mcp"
```

Popular MCP servers:

| Server | What it gives Codex | Install |
|---|---|---|
| [Context7](https://github.com/upstash/context7) | Up-to-date library docs | `npx -y @upstash/context7-mcp` |
| [GitHub](https://github.com/github/github-mcp-server) | Issues, PRs, repositories | `npx -y @github/github-mcp-server` |
| [Playwright](https://github.com/microsoft/playwright-mcp) | Browser automation | `npx -y @playwright/mcp@latest` |
| [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | Sandboxed file access | `npx -y @modelcontextprotocol/server-filesystem <path>` |
| [Postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | Query Postgres | `npx -y @modelcontextprotocol/server-postgres <conn-string>` |

**Tip:** Use OAuth-enabled servers with `codex mcp login <server-name>`.



## Hooks

Hooks run deterministic scripts during Codex lifecycle events.

Common locations:
```text
~/.codex/hooks.json
~/.codex/config.toml
<repo>/.codex/hooks.json
<repo>/.codex/config.toml
```

Manage in the TUI:
```text
/hooks
```

Example - run a check after each turn stops:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "npm test",
            "statusMessage": "Running tests"
          }
        ]
      }
    ]
  }
}
```

Useful hook events include `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, and `Stop`.

**Tip:** Project-local hooks load only after you trust the project. Non-managed command hooks must be reviewed and trusted before they run.



## GitHub Workflows

Use the GitHub CLI for best results:

```bash
gh auth login
gh pr checkout 123
codex review --base main
```

Prompt examples:
```text
Review PR #123 using gh and focus on security regressions.
Address all review comments on the current branch.
Summarize the diff against main and write a PR description.
```

**Tip:** Give Codex permission to use `gh` rather than asking it to scrape GitHub pages. CLI output is more reliable and easier to verify.



## Multi-Session Workflows

Long projects span multiple Codex sessions. Keep continuity explicit:

* Use `AGENTS.md` for durable repo conventions
* Keep a `PLAN.md` or task file for multi-day work
* Use `/goal` when Codex should keep driving toward a durable objective
* Use `/compact` before context gets noisy
* Use `/resume` or `codex resume --last` to continue prior work
* Use `/fork` for what-if exploration
* Commit small checkpoints in git

**Tip:** At the start of a new session, reference the plan file directly: `@PLAN.md continue with the next unchecked item`.



## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Open slash command menu |
| `@` | Mention files, folders, or images |
| `$` | Mention a skill or app |
| `!` at start of line | Run a local shell command under current permissions |
| Up / Down | Restore draft history |
| Ctrl+R | Search prompt history |
| Tab while a turn runs | Queue a slash command or follow-up |
| Enter while a turn runs | Inject instructions into the current turn |
| Esc twice on empty input | Edit the previous prompt and fork from it |
| Ctrl+O | Copy latest completed Codex output |
| Ctrl+C | Exit when input is empty |

**Tip:** Use `/keymap` to inspect and customize TUI shortcuts. Bindings persist to `tui.keymap` in `config.toml`.

TUI customization:

```text
/statusline   # Pick and reorder footer fields
/title        # Configure terminal title fields
/theme        # Preview and save syntax-highlighting theme
/vim          # Toggle Vim editing in the composer
/raw          # Toggle raw scrollback for easier selection and copying
/personality  # Choose friendly, pragmatic, or none when supported
```



## Prompt Techniques

Patterns that consistently produce better results:

* **"Show me the plan first"** - useful before risky edits
* **"Only modify `path/to/file.ts`"** - limits blast radius
* **"Run the existing tests and fix only regressions from this change"** - keeps cleanup focused
* **"Use subagents: explorer for codebase mapping, worker for implementation"** - parallelizes large tasks
* **"Ask clarifying questions before editing"** - good for ambiguous product requirements
* **"Review the risks before applying changes"** - forces a design check
* **"Use official docs only"** - reduces stale or low-quality web results
* **"Do not add dependencies without asking"** - prevents unnecessary package churn



## Migrate From Claude

Most Claude Code habits transfer directly, but the filenames and extension layout differ.

Use the guided importer from a local TUI session:

```text
/import    # Select Claude Code setup, project files, or recent chats to import
```

`/import` is unavailable while a task is running, in remote sessions, and while connected to the local app-server daemon.

| Claude Code | Codex CLI |
|-------------|-----------|
| `claude` | `codex` |
| `claude -p "..."` | `codex exec "..."` |
| `CLAUDE.md` | `AGENTS.md` |
| `/model` | `/model` |
| `/usage`, `/cost`, `/stats` | `/usage` (account activity) and `/status` (session state) |
| `/compact [focus]` | `/compact` |
| `/plan` | `/plan [goal]` |
| `/diff` | `/diff` |
| `/review` | `/review` or `codex review` |
| `/permissions` | `/permissions` plus `--sandbox` and `--ask-for-approval` |
| `/mcp` | `/mcp` or `codex mcp` |
| `/skills` | `/skills`, `$skill-name` mentions, and `.agents/skills/` |
| `/agents` | `/agent` and `.codex/agents/` |
| `! command` | `! command` (runs under current approvals and sandbox) |
| `@file` | `@file` or `/mention` |


Suggested manual migration steps:

1. Rename or adapt `CLAUDE.md` into `AGENTS.md`.
2. Move reusable skills to `.agents/skills/<skill-name>/SKILL.md`.
3. Move custom agent definitions to `.codex/agents/<agent-name>.toml`.
4. Recreate MCP servers with `codex mcp add ...`.
5. Translate allow/deny habits into Codex sandbox and approval settings.

**Tip:** Do not bulk-copy Claude hooks or settings into Codex. Recreate them intentionally because hook event names, config files, and permission behavior are not identical.



## Useful Links

**Documentation**
- [Codex CLI Docs](https://developers.openai.com/codex/cli) - official Codex CLI overview
- [Models](https://developers.openai.com/codex/models) - recommended models and reasoning modes
- [Command Line Options](https://developers.openai.com/codex/cli/reference) - official CLI reference
- [Slash Commands](https://developers.openai.com/codex/cli/slash-commands) - interactive command reference
- [Config Basics](https://developers.openai.com/codex/config-basic) - config files, precedence, common options
- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) - project instruction discovery

**Extensions**
- [MCP](https://developers.openai.com/codex/mcp) - connecting Codex to external tools
- [Skills](https://developers.openai.com/codex/skills) - reusable workflows
- [Subagents](https://developers.openai.com/codex/subagents) - parallel specialized agents
- [Hooks](https://developers.openai.com/codex/hooks) - lifecycle scripts

**General**
- [openai/codex](https://github.com/openai/codex) - official open-source repository
- [Codex Changelog](https://developers.openai.com/codex/changelog) - release notes
- [ChatGPT Desktop App](https://developers.openai.com/codex/app) - desktop workflows and terminal handoff
- [OpenAI Docs MCP](https://platform.openai.com/docs/docs-mcp) - official docs MCP server

---

Codex CLI Cheat Sheet version 1.3
© 2026 Andrei Smirnov — [github.com/pinebit](https://github.com/pinebit)
