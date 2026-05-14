#!/usr/bin/env python3
"""Inline the brand SVG defs into every HTML file in the kit.

Idempotent: removes any prior <!-- BRAND_DEFS_START --> ... <!-- BRAND_DEFS_END -->
block before injecting, so re-running is safe.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFS_SRC = ROOT / "brand-marks.svg"

# Strip XML declaration, keep the <svg>...</svg> block
defs_text = DEFS_SRC.read_text()
defs_text = re.sub(r'<\?xml[^>]*\?>\s*', '', defs_text).strip()

START = "<!-- BRAND_DEFS_START -->"
END = "<!-- BRAND_DEFS_END -->"
PAYLOAD = f"\n{START}\n{defs_text}\n{END}\n"

PRIOR = re.compile(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.DOTALL)

count = 0
for html in ROOT.rglob("*.html"):
    if "_homepage-captures" in html.parts:
        continue
    text = html.read_text()
    text = PRIOR.sub("", text)
    m = re.search(r"<body[^>]*>", text)
    if not m:
        print(f"  skip · no <body> · {html.relative_to(ROOT)}")
        continue
    insert_at = m.end()
    text = text[:insert_at] + PAYLOAD + text[insert_at:]
    html.write_text(text)
    count += 1
    print(f"  → {html.relative_to(ROOT)}")
print(f"\nInjected into {count} HTML files.")
