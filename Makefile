.DEFAULT_GOAL := help
.PHONY: help setup claude codex

PYTHON ?= python3
VENV := .venv

help:
	@echo "make setup   Create the virtual environment and install rendering dependencies"
	@echo "make claude  Build the Claude Code cheat sheet"
	@echo "make codex   Build the Codex cheat sheet"

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install -r requirements.txt
	$(VENV)/bin/python -m playwright install chromium

claude:
	$(MAKE) -C claude

codex:
	$(MAKE) -C codex
