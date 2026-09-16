#!/usr/bin/env python3
"""Build the Codex CLI cheat sheet as paginated HTML, PDF, and preview PDF."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

import markdown


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
DEFAULT_OUTPUT = REPO_ROOT / "output"
OUTPUT_PREFIX = "Codex-CLI-Cheat-Sheet"
PREVIEW_CONTENT_PAGES = 5

MD_EXTENSIONS = [
    "tables", "fenced_code", "codehilite", "attr_list", "sane_lists", "smarty",
]
MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "noclasses": True, "pygments_style": "monokai"},
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def parse_source(path: Path) -> tuple[str, str, str]:
    source = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", source, re.MULTILINE)
    if not title_match:
        raise ValueError("cheatsheet.md must start with an H1 title")
    title = title_match.group(1).strip()

    version_match = re.search(r"^Codex CLI Cheat Sheet version\s+(.+?)\s*$", source, re.MULTILINE)
    if not version_match:
        raise ValueError("Missing version line at the end of cheatsheet.md")
    version = version_match.group(1).strip()

    # The cover and closing page render the title/version/footer themselves.
    content = source[title_match.end():]
    content = re.sub(
        r"\n---\s*\n\s*Codex CLI Cheat Sheet version[\s\S]*$",
        "",
        content,
    ).strip()
    content = re.sub(
        r"(?m)^[ \t]*<!--[ \t]*page-break[ \t]*-->[ \t]*$",
        '<div class="manual-page-break" aria-hidden="true"></div>',
        content,
    )
    body = markdown.Markdown(
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
    ).convert(content)
    return title, version, body


def cover_art() -> str:
    """Text-free, flat vector artwork in the phrasebook visual language."""
    return '''<svg viewBox="0 0 560 650" role="img" aria-label="A friendly coding terminal illustration">
      <path fill="#f3ead8" d="M0 220 560 150v500H0Z"/>
      <circle cx="470" cy="250" r="52" fill="#d7a449"/>
      <path fill="#cf6255" d="M0 470 560 330v320H0Z"/>
      <path fill="#18364d" d="M70 232h416a24 24 0 0 1 24 24v244a24 24 0 0 1-24 24H70a24 24 0 0 1-24-24V256a24 24 0 0 1 24-24Z"/>
      <path fill="#fffdf8" d="M70 232h416a24 24 0 0 1 24 24v35H46v-35a24 24 0 0 1 24-24Z"/>
      <circle cx="78" cy="262" r="8" fill="#cf6255"/><circle cx="104" cy="262" r="8" fill="#d7a449"/><circle cx="130" cy="262" r="8" fill="#6b9a8c"/>
      <path d="m113 358 58 45-58 45M211 449h105" fill="none" stroke="#f7f0df" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M361 340c48-43 116-6 103 51-9 41-50 62-103 99-53-37-94-58-103-99-13-57 55-94 103-51Z" fill="#d7a449"/>
      <path d="m325 397 24 24 49-57" fill="none" stroke="#18364d" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M84 563h302" stroke="#f7f0df" stroke-width="8" stroke-linecap="round" opacity=".75"/>
    </svg>'''


def render_html(title: str, version: str, body: str, variant: str) -> str:
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    preview_script = ""
    if variant == "preview":
        preview_script = f'''
          const pages = [...document.querySelectorAll('.content-page')];
          pages.slice({PREVIEW_CONTENT_PAGES}).forEach(page => page.remove());
        '''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="Andrei Smirnov">
  <title>{esc(title)}</title>
  <style>{css}</style>
</head>
<body class="{esc(variant)}">
  <section class="book-page cover-page" data-page-id="cover">
    <div class="cover-stripes"></div>
    <div class="cover-copy">
      <span class="cover-eyebrow">THE PRACTICAL FIELD GUIDE</span>
      <h1><span>Codex CLI</span><br><em>Cheat Sheet</em></h1>
      <p>Commands, models, approvals, and workflows for productive agentic coding.</p>
    </div>
    <div class="cover-art">{cover_art()}</div>
    <div class="cover-bottom"><span>TERMINAL</span><span>WORKFLOWS</span><span>TOOLING</span></div>
  </section>

  <main id="source-content" hidden>{body}</main>
  <div id="content-pages"></div>

  <section class="book-page back-page" data-page-id="final">
    <div class="back-orbit orbit-one"></div><div class="back-orbit orbit-two"></div>
    <div class="back-mark"><span>&gt;_</span></div>
    <div class="back-copy">
      <span class="back-kicker">KEEP BUILDING</span>
      <h1>Ship it before<br><em>the coffee gets cold.</em></h1>
      <p>Keep the context focused. Give precise instructions. Verify the result.</p>
      <a href="https://developers.openai.com/codex">developers.openai.com/codex</a>
    </div>
    <div class="back-meta"><span>VERSION {esc(version)}</span><span>© 2026 ANDREI SMIRNOV</span></div>
  </section>

  <script>
    (() => {{
      const source = document.getElementById('source-content');
      const target = document.getElementById('content-pages');
      let pageNumber = 2;

      function newPage() {{
        const page = document.createElement('section');
        page.className = 'book-page content-page';
        page.dataset.pageId = `content-${{pageNumber - 1}}`;
        page.innerHTML = `<header class="running-head"><span>CODEX CLI</span><b>${{String(pageNumber).padStart(2, '0')}}</b></header><div class="page-body"></div><footer><span>CHEAT SHEET</span><span>ANDREI SMIRNOV</span></footer>`;
        target.appendChild(page);
        pageNumber += 1;
        return page.querySelector('.page-body');
      }}

      let body = newPage();
      const nodes = [...source.children];
      for (let index = 0; index < nodes.length; index += 1) {{
        if (nodes[index].classList.contains('manual-page-break')) {{
          if (body.children.length > 0) body = newPage();
          body.closest('.content-page').dataset.manualBreak = 'true';
          continue;
        }}
        const unit = document.createElement('div');
        unit.className = 'pagination-unit';
        unit.appendChild(nodes[index].cloneNode(true));

        // Headings travel with their first content block. Introductory paragraphs
        // travel with the command, table, or list they introduce.
        const tag = nodes[index].tagName;
        const next = nodes[index + 1];
        const nextIsPayload = next && (
          ['PRE', 'TABLE', 'UL', 'OL'].includes(next.tagName) ||
          next.classList.contains('codehilite')
        );
        if (next && (['H2', 'H3'].includes(tag) || (tag === 'P' && nextIsPayload))) {{
          unit.appendChild(next.cloneNode(true));
          index += 1;
          const afterIntro = nodes[index + 1];
          const introLeadsToPayload = ['H2', 'H3'].includes(tag) && next.tagName === 'P' && afterIntro && (
            ['PRE', 'TABLE', 'UL', 'OL'].includes(afterIntro.tagName) ||
            afterIntro.classList.contains('codehilite')
          );
          if (introLeadsToPayload) {{
            unit.appendChild(afterIntro.cloneNode(true));
            index += 1;
          }}
        }}

        const forcesBreak = unit.firstElementChild?.classList.contains('page-break-before');
        if (forcesBreak && body.children.length > 0) body = newPage();
        body.appendChild(unit);
        if (body.scrollHeight > body.clientHeight + 1 && body.children.length > 1) {{
          unit.remove();
          body = newPage();
          body.appendChild(unit);
        }}
      }}
      source.remove();
      {preview_script}
      document.body.dataset.ready = 'true';
    }})();
  </script>
</body>
</html>'''


def pdf_page_count(path: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page\b", path.read_bytes()))


def detect_overflow(page: Any) -> list[dict[str, Any]]:
    return page.evaluate("""() => [...document.querySelectorAll('.book-page')].flatMap(sheet => {
      const body = sheet.querySelector('.page-body');
      const bad = [];
      if (body && body.scrollHeight > body.clientHeight + 1) bad.push({page: sheet.dataset.pageId, kind: 'vertical'});
      sheet.querySelectorAll('pre, table').forEach(el => {
        if (el.scrollWidth > el.clientWidth + 1) bad.push({page: sheet.dataset.pageId, kind: 'horizontal', tag: el.tagName});
      });
      const last = body?.querySelector('.pagination-unit:last-child > :last-child');
      if (last && ['H2', 'H3'].includes(last.tagName)) bad.push({page: sheet.dataset.pageId, kind: 'orphan-heading'});
      return bad;
    })""")


def detect_forced_breaks(page: Any) -> list[dict[str, Any]]:
    """Confirm every explicit marker is the first pagination unit on its sheet."""
    return page.evaluate("""() => [...document.querySelectorAll('.page-break-before')].map(heading => {
      const unit = heading.closest('.pagination-unit');
      const body = heading.closest('.page-body');
      return {
        heading: heading.textContent.trim(),
        page: heading.closest('.content-page')?.dataset.pageId || null,
        enforced: Boolean(unit && body && body.querySelector('.pagination-unit:first-child') === unit)
      };
    })""")


def export(output: Path, print_html: Path, preview_html: Path) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required; use the repository .venv") from exc

    options = {
        "width": "148mm", "height": "210mm",
        "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
        "print_background": True, "prefer_css_page_size": True,
    }
    report: dict[str, Any] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1200})

        page.goto(print_html.as_uri(), wait_until="networkidle")
        page.wait_for_function("document.body.dataset.ready === 'true'")
        report["overflow"] = detect_overflow(page)
        report["forcedBreaks"] = detect_forced_breaks(page)
        report["manualBreakPages"] = page.locator('.content-page[data-manual-break="true"]').evaluate_all(
            "pages => pages.map(page => page.dataset.pageId)"
        )
        report["contentPages"] = page.locator(".content-page").count()
        pdf = output / f"{OUTPUT_PREFIX}.pdf"
        page.pdf(path=str(pdf), **options)
        report["pdfPages"] = pdf_page_count(pdf)

        page.goto(preview_html.as_uri(), wait_until="networkidle")
        page.wait_for_function("document.body.dataset.ready === 'true'")
        report["previewContentPages"] = page.locator(".content-page").count()
        preview_pdf = output / f"{OUTPUT_PREFIX}-preview.pdf"
        page.pdf(path=str(preview_pdf), **options)
        report["previewPdfPages"] = pdf_page_count(preview_pdf)
        page.close()

        cover_context = browser.new_context(
            viewport={"width": 640, "height": 900},
            device_scale_factor=3,
        )
        cover_page = cover_context.new_page()
        cover_page.goto(print_html.as_uri(), wait_until="networkidle")
        cover_page.wait_for_function("document.body.dataset.ready === 'true'")
        cover = cover_page.locator(".cover-page")
        cover_path = output / f"{OUTPUT_PREFIX}-cover.png"
        cover.screenshot(path=str(cover_path))
        cover_size = cover.evaluate("el => [el.clientWidth, el.clientHeight]")
        report["coverPng"] = cover_path.name
        report["coverCssPixels"] = cover_size
        report["coverDeviceScaleFactor"] = 3
        cover_context.close()
        browser.close()

    expected = report["contentPages"] + 2
    expected_preview = report["previewContentPages"] + 2
    if (report["overflow"] or any(not item["enforced"] for item in report["forcedBreaks"])
            or report["pdfPages"] != expected or report["previewPdfPages"] != expected_preview):
        raise RuntimeError("Rendered output failed overflow or page-count validation")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=ROOT / "cheatsheet.md")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / f"{OUTPUT_PREFIX}-validation-report.json"
    try:
        title, version, body = parse_source(args.source.resolve())
        print_html = output / f"{OUTPUT_PREFIX}.html"
        preview_html = output / f"{OUTPUT_PREFIX}-preview.html"
        print_html.write_text(render_html(title, version, body, "print"), encoding="utf-8")
        preview_html.write_text(render_html(title, version, body, "preview"), encoding="utf-8")
        report = {"status": "passed", "title": title, "version": version}
        report.update(export(output, print_html, preview_html))
    except Exception as exc:
        report = {"status": "failed", "errors": [str(exc)]}
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Built {report['pdfPages']} pages and {report['previewPdfPages']}-page preview in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
