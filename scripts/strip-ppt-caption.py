# -*- coding: utf-8 -*-
import re
from pathlib import Path

html = Path(__file__).resolve().parents[1] / "25-agent-development.html"
text = html.read_text(encoding="utf-8")
text = re.sub(r"图：PPT 第 \d+ 页 — ", "图：", text)
text = re.sub(r'alt="PPT 第 \d+ 页配图：', 'alt="', text)
html.write_text(text, encoding="utf-8")
print("done")
