#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "\u9700\u6c42\u5206\u6790"


def read_text(raw: bytes) -> tuple[str, str]:
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("gbk"), "gbk"


for path in sorted(ROOT.glob("*.html")):
    raw = path.read_bytes()
    text, enc = read_text(raw)
    if enc == "utf-8" and (MARKER in text or "Java\u9879\u76ee\u624b\u518c" in text):
        print("skip:", path.name)
        continue
    path.write_text(text, encoding="utf-8", newline="\n")
    print("fixed:", path.name, "from", enc)

print("done")
