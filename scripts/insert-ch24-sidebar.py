# -*- coding: utf-8 -*-
"""Insert chapter 24 sidebar link before glossary in all HTML chapters."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = (
    '            <li><a href="23-business-intelligence.html">23 业务智能化</a></li>\n'
    '            <li><a href="glossary.html">术语字典</a></li>'
)
NEW = (
    '            <li><a href="23-business-intelligence.html">23 业务智能化</a></li>\n'
    '            <li><a href="24-palantir-aip.html">24 Palantir AIP 架构</a></li>\n'
    '            <li><a href="glossary.html">术语字典</a></li>'
)

count = 0
for path in ROOT.glob("*.html"):
    if path.name == "24-palantir-aip.html":
        continue
    text = path.read_text(encoding="utf-8")
    if OLD not in text:
        continue
    path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    count += 1
print("sidebar updated:", count)
