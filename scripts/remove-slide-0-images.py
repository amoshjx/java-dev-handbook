# -*- coding: utf-8 -*-
"""Remove figure nodes referencing slide-*-0.png from chapter 25."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "25-agent-development.html"
html = path.read_text(encoding="utf-8")
before = len(re.findall(r"slide-\d+-0\.png", html))

pattern = (
    r'<figure class="diagram-block diagram-image ppt-slide-figure">'
    r'<img src="assets/agent-ch25/slide-\d+-0\.png"[^>]*/>'
    r'<figcaption class="diagram-caption">[^<]*</figcaption>'
    r"</figure>\s*"
)
html, n = re.subn(pattern, "", html)
html = re.sub(r'<div class="ppt-slide-figures">\s*</div>\s*', "", html)

after = len(re.findall(r"slide-\d+-0\.png", html))
path.write_text(html, encoding="utf-8")
print("removed figures:", n)
print("slide-*-0.png before:", before, "after:", after)
