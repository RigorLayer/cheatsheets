.PHONY: all clean

PYTHON := ../.venv/bin/python
OUTPUT := ../output

all:
	$(PYTHON) render.py cheatsheet.md --output $(OUTPUT)

clean:
	rm -f $(OUTPUT)/Codex-CLI-Cheat-Sheet.html $(OUTPUT)/Codex-CLI-Cheat-Sheet.pdf
	rm -f $(OUTPUT)/Codex-CLI-Cheat-Sheet-preview.html $(OUTPUT)/Codex-CLI-Cheat-Sheet-preview.pdf
	rm -f $(OUTPUT)/Codex-CLI-Cheat-Sheet-cover.png
	rm -f $(OUTPUT)/Codex-CLI-Cheat-Sheet-validation-report.json
