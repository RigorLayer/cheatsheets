# Repository instructions

Do not commit or push anything without the user's explicit approval.

This repository contains independently maintained cheat sheets:

- `claude/` — Claude Code cheat sheet, renderer, styles, and Makefile.
- `codex/` — Codex cheat sheet, renderer, styles, and Makefile.
- `output/` — generated artifacts; ignored by Git.

Work only on the cheat sheet requested by the user, unless the task explicitly concerns shared build configuration or documentation. Follow the nearest nested `AGENTS.md` for content and production rules.

Use `cheatsheet.md` as each sheet's source. Verify product commands and details against official documentation; do not invent material. Preserve the version line and copyright footer.

Run `make setup` from the repository root to install dependencies into `.venv` and install Playwright Chromium. Dependency versions are recorded in `requirements.txt`.

Build only the requested sheet with root target `make claude` or `make codex`, or run `make` in its directory. Do not add a build-all or clean-all target. A sheet's `make clean` may remove only its own generated files, never the shared output directory.

Keep both renderers' default output paths rooted in this repository. Do not depend on the original books repository or copy its virtual environment. Keep `.venv/` and generated files out of Git.

After renderer, style, source, or build changes, build the affected sheet and inspect its validation report. The renderer must pass overflow, explicit page-break, and PDF page-count validation.
