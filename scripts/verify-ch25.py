# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / "25-agent-development.html").read_text(encoding="utf-8")
imgs = set(re.findall(r"assets/agent-ch25/([^\"']+)", html))
missing = [i for i in sorted(imgs) if not (root / "assets" / "agent-ch25" / i).exists()]
ids = set(re.findall(r'id="([^"]+)"', html))
links = set(re.findall(r'href="#([^"]+)"', html))
broken = links - ids
print("referenced images:", len(imgs))
print("missing images:", len(missing))
for m in missing:
    print("  MISSING:", m)
print("section ids:", len([i for i in ids if i.startswith("agent-")]))
print("broken anchors:", broken)
