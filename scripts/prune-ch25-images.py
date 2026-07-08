# -*- coding: utf-8 -*-
"""Remove broken image references from chapter 25 HTML."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "25-agent-development.html"
IMG_DIR = ROOT / "assets" / "agent-ch25"

html = HTML.read_text(encoding="utf-8")
existing = {p.name for p in IMG_DIR.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}}
referenced = set(re.findall(r"assets/agent-ch25/([^\"']+)", html))
missing = sorted(referenced - existing)

print("referenced:", len(referenced))
print("existing images:", len(existing))
print("missing:", len(missing))
for m in missing:
    print("  -", m)

# Remove figure nodes with missing images
for fname in missing:
    pattern = (
        r'<figure class="diagram-block diagram-image ppt-slide-figure">'
        rf'<img src="assets/agent-ch25/{re.escape(fname)}"[^>]*/>'
        r'<figcaption class="diagram-caption">[^<]*</figcaption>'
        r"</figure>\s*"
    )
    html, n = re.subn(pattern, "", html)
    if n:
        print(f"removed {n} figure(s) for {fname}")
        continue

    # header / standalone img (not in figure)
    pattern2 = (
        r'<div class="diagram-block diagram-image">\s*'
        rf'<img src="assets/agent-ch25/{re.escape(fname)}"[^>]*/>\s*'
        r'<p class="diagram-caption">[^<]*</p>\s*'
        r"</div>\s*"
    )
    html, n2 = re.subn(pattern2, "", html)
    if n2:
        print(f"removed {n2} diagram-block(s) for {fname}")

html = re.sub(r'<div class="ppt-slide-figures">\s*</div>\s*', "", html)

remaining = set(re.findall(r"assets/agent-ch25/([^\"']+)", html))
still_missing = sorted(remaining - existing)
HTML.write_text(html, encoding="utf-8")
print("remaining references:", len(remaining))
print("still missing after cleanup:", still_missing)
