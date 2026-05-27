#!/usr/bin/env python3
"""Copy good sidebar from chapter 01 into damaged nav pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "01-requirements-analysis.html"
sidebar = re.search(
    r'<aside class="sidebar">.*?</aside>',
    SOURCE.read_text(encoding="utf-8"),
    re.S,
).group()

for name in ("index.html", "java-development.html", "13-ruoyi-framework.html"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<aside class="sidebar">.*?</aside>', sidebar, text, flags=re.S)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("sidebar fixed:", name)

print("done")
