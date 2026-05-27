#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def fix_bytes(raw: bytes) -> bytes:
    raw = raw.replace(b"\xe2\x80\x3f", b"\xe2\x80\x94")
    raw = raw.replace(b"\xe6\x9e\x3f/a>", b'\xe6\x9e\x90"></a>')
    raw = raw.replace(b"\xe6\x9e\x3f/strong>", b'\xe6\x9e\x90"></strong>')
    raw = raw.replace(b"\xe7\x9b\x3f/a>", b'\xe7\x9b\xae"></a>')
    raw = raw.replace(b"\xe7\x9b\x3f/p>", b'\xe7\x9b\xae"></p>')
    raw = raw.replace(b"\xe7\x9b\x3f/li>", b'\xe7\x9b\xae"></li>')
    raw = raw.replace(b"\xe7\x9b\x3f/strong>", b'\xe7\x9b\xae"></strong>')
    raw = raw.replace(b"\xe8\x83\xbd\x3f/a>", b'\xe8\x83\xbd"></a>')
    raw = raw.replace(b"\xe8\x83\xbd\x3f/p>", b'\xe8\x83\xbd"></p>')
    raw = raw.replace(b"\xe8\x83\xbd\x3f/strong>", b'\xe8\x83\xbd"></strong>')
    raw = raw.replace(b"\xe5\x8f\x3f/a>", b'\xe5\x8f\x98"></a>')
    raw = raw.replace(b"\xe5\x8f\x3f/p>", b'\xe5\x8f\x98"></p>')
    raw = raw.replace(b"\xe5\x8f\x3f/strong>", b'\xe5\x8f\x98"></strong>')
    raw = raw.replace(b"\xe7\xa0\x3f/strong>", b'\xe7\xa0\x81"></strong>')
    raw = raw.replace(b"\xe8\xaf\x3f/strong>", b'\xe8\xaf\x84"></strong>')
    raw = raw.replace(b"\xe6\x80\xa7\x3f/a>", b'\xe6\x80\xa7"></a>')
    raw = raw.replace(b"\xe6\x80\xa7\x3f/p>", b'\xe6\x80\xa7"></p>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/li>", b'\xe7\xab\xa0"></li>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/p>", b'\xe7\xab\xa0"></p>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/strong>", b'\xe7\xab\xa0"></strong>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/h2>", b'\xe7\xab\xa0"></h2>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/ul>", b'\xe7\xab\xa0"></ul>')
    raw = raw.replace(b"\xe7\xab\xa0\x3f/a>", b'\xe7\xab\xa0"></a>')
    return raw


def decode_html(raw: bytes) -> str:
    raw = fix_bytes(raw)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return raw.decode("gbk")
    except UnicodeDecodeError:
        return raw.decode("gbk", errors="replace")


def remove_mermaid_script(text: str) -> str:
    return re.sub(r'\s*<script src="assets/mermaid\.min\.js" defer></script>\n?', "", text)


for path in sorted(ROOT.glob("*.html")):
    raw = path.read_bytes()
    text = remove_mermaid_script(decode_html(raw))
    path.write_text(text, encoding="utf-8", newline="\n")
    print("written:", path.name)

print("done")
