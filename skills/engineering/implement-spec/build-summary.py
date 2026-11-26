#!/usr/bin/env python3
"""Build summary.html from summary.src.html.

Inlines summary.css and summary.js (kept next to this script), strips HTML
comments, and checks the page. Exits 1 and prints every problem when a check
fails, so fix the source and run it again.

Usage: python3 build-summary.py SRC.html [OUT.html]   (OUT defaults to summary.html beside SRC)
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

here = Path(__file__).resolve().parent
src = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name("summary.html")
html = src.read_text()
errors = []

# Inline assets and drop comments
html = html.replace('<link rel="stylesheet" href="summary.css">', "<style>\n" + (here / "summary.css").read_text() + "</style>")
html = html.replace('<script src="summary.js"></script>', "<script>\n" + (here / "summary.js").read_text() + "</script>")
html = re.sub(r"<!--.*?-->\n?", "", html, flags=re.S)
if 'href="summary.css"' in html or 'src="summary.js"' in html:
    errors.append("summary.css or summary.js link was edited, so it could not be inlined")

# Placeholders. Prose is checked for any UPPER_SNAKE token and for the template's
# single-word placeholders. Code blocks hold real output, so only the template's own tokens count there.
SINGLE = ("TITLE", "DATE", "GOAL", "SUITE", "SLUG", "COMMITS", "FILES", "PASSED", "FAILED", "SKIPPED", "DEVIATIONS")
PRE_TOKENS = ("STEP_COMMAND", "VAL_COMMAND_AND_EXCERPT", "MANUAL_OUTPUT_EXCERPT")
body = re.sub(r"<(style|script)\b.*?</\1>", "", html, flags=re.S)
code = " ".join(re.findall(r"<pre\b.*?</pre>", body, flags=re.S))
prose = re.sub(r"<(pre|code)\b.*?</\1>", "", body, flags=re.S)
visible = re.sub(r"<[^>]+>", " ", prose)
found = set(re.findall(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b", visible))
found |= {w for w in SINGLE if re.search(rf"\b{w}\b", visible)}
found |= {t for t in PRE_TOKENS if t in code}
for token in sorted(found):
    errors.append(f"placeholder left: {token}")
if "ABSOLUTE/PATH" in body:
    errors.append("placeholder left: ABSOLUTE/PATH in a link")
if re.search(r"<(tr|li|dd)>\s*</\1>", body):
    errors.append("an empty row or item")

# Links
ids = set(re.findall(r'\bid="([^"]+)"', html))
for href in re.findall(r'\bhref="([^"]*)"', html):
    if href.startswith("#"):
        if len(href) > 1 and href[1:] not in ids:
            errors.append(f"link to a missing id: {href}")
    elif href.startswith("file://"):
        path = unquote(urlparse(href).path)
        if not path.startswith("/"):
            errors.append(f"file link is not absolute: {href}")
        elif not Path(path).exists():
            errors.append(f"file link points at nothing: {href}")
    elif not href.startswith("https://"):
        errors.append(f"link is not #id, file:///, or https://: {href}")

if errors:
    print("summary not built. Fix summary.src.html and run again:", file=sys.stderr)
    for e in errors:
        print("  " + e, file=sys.stderr)
    sys.exit(1)
out.write_text(html)
print(f"built {out}")
