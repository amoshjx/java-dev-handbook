# -*- coding: utf-8 -*-
"""Move Palantir sections from ch25 to ch24."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH25 = ROOT / "25-agent-development.html"
CH24 = ROOT / "24-palantir-aip.html"
SRC_IMG = ROOT / "assets" / "agent-ch25"
DST_IMG = ROOT / "assets" / "palantir-aip-ppt"

ID_MAP = {
    "agent-palantir-overview": "aip-ppt-overview",
    "agent-palantir-ontology": "aip-ppt-ontology",
    "agent-palantir-products": "aip-ppt-products",
    "agent-palantir-assist-logic": "aip-ppt-assist-logic",
    "agent-palantir-studio": "aip-ppt-studio",
    "agent-palantir-evals": "aip-ppt-evals",
    "agent-palantir-threads": "aip-ppt-threads",
    "agent-palantir-architecture": "aip-ppt-architecture",
    "agent-palantir-architecture-detail": "aip-ppt-architecture-detail",
}

TITLE_MAP = {
    "五、Palantir AIP 概述": "附录 A：分享材料 — AIP 概述",
    "五、Palantir AIP：本体论": "附录 A：分享材料 — 本体论",
    "五、Palantir AIP：产品与功能": "附录 A：分享材料 — 产品与功能",
    "五、Palantir AIP：Assist 与 Logic": "附录 A：分享材料 — Assist 与 Logic",
    "五、Palantir AIP：Chatbot Studio": "附录 A：分享材料 — Chatbot Studio",
    "五、Palantir AIP：AIP Evals": "附录 A：分享材料 — AIP Evals",
    "五、Palantir AIP：AIP Threads": "附录 A：分享材料 — AIP Threads",
    "五、Palantir AIP：架构总览": "附录 A：分享材料 — 架构总览",
    "五、Palantir AIP：架构能力详解": "附录 A：分享材料 — 架构能力详解",
}


def extract_palantir_sections(html: str) -> tuple[str, str]:
    pattern = r'(      <section class="section" id="agent-palantir-overview">.*?)(      <section class="section" id="agent-mes-demo">)'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        raise SystemExit("Palantir block not found in ch25")
    block = m.group(1)
    rest_start = m.group(2)
    html_without = html[: m.start(1)] + rest_start + html[m.end(2) :]
    return block, html_without


def transform_for_ch24(block: str) -> str:
    for old, new in ID_MAP.items():
        block = block.replace(f'id="{old}"', f'id="{new}"')
    for old, new in TITLE_MAP.items():
        block = block.replace(f"<h2>{old}</h2>", f"<h2>{new}</h2>")
    block = block.replace("assets/agent-ch25/", "assets/palantir-aip-ppt/")
  # remove self-referential tips
    block = re.sub(
        r'<div class="card-block block-tips"><h4>延伸阅读</h4><p>Palantir AIP 的 Ontology、Action Types、Evals 与 Java 接入细节见<a href="24-palantir-aip.html">第 24 章 Palantir AIP 架构</a>。</p></div>\s*',
        "",
        block,
    )
    return block


def move_images(block: str) -> None:
    DST_IMG.mkdir(parents=True, exist_ok=True)
    names = set(re.findall(r"assets/palantir-aip-ppt/([^\"']+)", block))
    for name in names:
        src = SRC_IMG / name
        dst = DST_IMG / name
        if src.exists():
            shutil.copy2(src, dst)
            print("copied", name)


def update_ch25(html: str) -> str:
    html = html.replace(
        "推理编排（ReAct / Plan-and-Execute / CoT / ToT）、Tool/MCP/Skill/Memory/Graph RAG 技术栈，以及 Palantir AIP 参考架构与 MES 追溯 Demo。承接",
        "推理编排（ReAct / Plan-and-Execute / CoT / ToT）、Tool/MCP/Skill/Memory/Graph RAG 技术栈与 MES 追溯 Demo。Palantir AIP 详见",
    )
    html = html.replace(
        '<a href="24-palantir-aip.html">第 24 章</a>的企业级 AIP 架构形成「业务落地 → 平台参考」闭环。',
        '<a href="24-palantir-aip.html">第 24 章 Palantir AIP 架构</a>。',
    )
    html = html.replace(
        "覆盖从 LLM 基础、Agent 架构、MCP/Skill/Memory 到 Palantir AIP 参考与 MES Demo 的全链路内容。",
        "覆盖从 LLM 基础、Agent 架构、MCP/Skill/Memory 到 MES Demo 的 Agent 开发全链路内容。",
    )
    html = re.sub(
        r'<li><a href="#agent-palantir-overview">Palantir AIP</a>：Ontology 与企业 AI 平台</li>\s*',
        "",
        html,
    )
    html = html.replace("<h2>六、MES Trace Agent Demo</h2>", "<h2>五、MES Trace Agent Demo</h2>")
    html = html.replace("<h1>25 Agent 开发：IFP 模块与实践全栈</h1>", "<h1>25 Agent 开发：LLM 与 Agent 实践</h1>")
    return html


def update_ch24_learning_map(html: str) -> str:
    insert = (
        '              <li><a href="#aip-ppt-overview">附录 A</a>：分享材料图文（概述、产品截图、架构矩阵）。</li>\n'
    )
    marker = '              <li><a href="#security-governance">最后做治理</a>：权限、用途、安全标记、血缘、发布门禁和运行监控。</li>\n'
    if insert.strip() not in html and marker in html:
        html = html.replace(marker, marker + insert)
    return html


def main() -> None:
    ch25 = CH25.read_text(encoding="utf-8")
    block, ch25_new = extract_palantir_sections(ch25)
    block = transform_for_ch24(block)
    move_images(block)

    ch24 = CH24.read_text(encoding="utf-8")
    marker = '      <section class="section" id="aip-conclusion">'
    if marker not in ch24:
        raise SystemExit("aip-conclusion marker not found in ch24")
    if "aip-ppt-overview" not in ch24:
        ch24 = ch24.replace(marker, block + marker)
    ch24 = update_ch24_learning_map(ch24)

    ch25_new = update_ch25(ch25_new)
    CH24.write_text(ch24, encoding="utf-8")
    CH25.write_text(ch25_new, encoding="utf-8")
    print("done: Palantir sections moved to ch24")


if __name__ == "__main__":
    main()
