# RL Cheat Sheets

Printable Claude Code and Codex cheat sheets, maintained and built independently.

## Contents

| Cheat sheet | Source | Build |
| --- | --- | --- |
| Claude Code | `claude/cheatsheet.md` | `make claude` |
| Codex | `codex/cheatsheet.md` | `make codex` |

Each directory contains its Markdown source, `style.css`, Python renderer, Makefile, and content instructions in `AGENTS.md`.

## Setup

Prerequisites: Python 3.10 or newer with `venv` and pip, GNU Make, and internet access for dependency installation. The setup target installs Playwright Chromium in its standard user cache. On Linux, Chromium may also require system libraries; use Playwright's documented installation instructions for your distribution.

```sh
cd ~/cheatsheets
make setup
```

To choose a Python interpreter, use `make setup PYTHON=/path/to/python3`.
The repository uses its own `.venv`; it has no dependency on the original books repository. Python dependencies are pinned in `requirements.txt` to the versions used by the source repository at extraction.

## Build

```sh
make claude
make codex
```

Run either command independently. Running `make` without a target displays help. You can also run `make -C claude` or `make -C codex`.

Builds produce these artifacts in the Git-ignored `output/` directory:

- Full paginated HTML and PDF.
- Preview HTML and PDF.
- A PNG cover image.
- A JSON validation report covering overflow, explicit page breaks, and PDF page counts.

Filenames use `Claude-Code-Cheat-Sheet` or `Codex-CLI-Cheat-Sheet` as their prefix. Rendering fails when its built-in layout validation fails.

## Clean

```sh
make -C claude clean
make -C codex clean
```

Each command removes only that sheet's generated artifacts. There is no combined build or clean target.

## Editing

Edit the relevant `cheatsheet.md` and follow the root and sheet-specific `AGENTS.md` instructions. Rebuild the affected sheet and review its PDF and validation report. Verify product details against the [official Claude Code documentation](https://code.claude.com/docs/en/overview) or [official Codex documentation](https://developers.openai.com/codex/).

These files were copied from the `books` repository. Future work in this repository is independent; changes do not synchronize back automatically.

## License

- **Cheat sheet content** (`*/cheatsheet.md`, `*/style.css`): [CC BY 4.0](LICENSE-CONTENT) — free to share and adapt with attribution.
- **Code and tooling** (`render.py`, `Makefile`, etc.): [MIT](LICENSE) — free to use, modify, and distribute.
