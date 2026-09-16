.PHONY: all clean

PYTHON := ../.venv/bin/python
OUTPUT := ../output

all:
	$(PYTHON) render.py cheatsheet.md --output $(OUTPUT)

clean:
	rm -f $(OUTPUT)/Claude-Code-Cheat-Sheet.html $(OUTPUT)/Claude-Code-Cheat-Sheet.pdf
	rm -f $(OUTPUT)/Claude-Code-Cheat-Sheet-preview.html $(OUTPUT)/Claude-Code-Cheat-Sheet-preview.pdf
	rm -f $(OUTPUT)/Claude-Code-Cheat-Sheet-cover.png
	rm -f $(OUTPUT)/Claude-Code-Cheat-Sheet-validation-report.json
