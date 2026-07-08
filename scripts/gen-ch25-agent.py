# -*- coding: utf-8 -*-
"""Generate chapter 25 HTML from PPT extracted text and slide images."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_PATH = ROOT / "pptx_extracted_content.txt"
MANIFEST_PATH = ROOT / "assets" / "agent-ch25" / "manifest.txt"
OUT_PATH = ROOT / "25-agent-development.html"

SIDEBAR = """            <li><a href="index.html">目录首页</a></li>
            <li><a href="01-requirements-analysis.html">01 需求分析</a></li>
            <li><a href="02-prototype-design.html">02 原型设计</a></li>
            <li><a href="03-architecture-design.html">03 架构设计</a></li>
            <li><a href="04-project-scheduling.html">04 项目排期</a></li>
            <li class="sidebar-group"><span class="sidebar-group-label"><a href="java-development.html">开发实现</a></span></li>
            <li class="sidebar-subitem"><a href="05-dev-environment.html">05 开发环境搭建</a></li>
            <li class="sidebar-subitem"><a href="06-java-basics.html">06 Java基础语法</a></li>
            <li class="sidebar-subitem"><a href="07-oop.html">07 面向对象</a></li>
            <li class="sidebar-subitem"><a href="08-jvm.html">08 JVM</a></li>
            <li class="sidebar-subitem"><a href="09-concurrency.html">09 并发编程</a></li>
            <li class="sidebar-subitem"><a href="10-io-nio-network.html">10 IO·NIO·网络</a></li>
            <li class="sidebar-subitem"><a href="11-persistence.html">11 持久化</a></li>
            <li class="sidebar-subitem"><a href="12-spring-framework.html">12 Spring Framework</a></li>
            <li class="sidebar-subitem"><a href="13-build-packaging-deploy.html">13 构建·打包·部署</a></li>
            <li class="sidebar-subitem"><a href="14-ruoyi-framework.html">14 RuoYi 框架</a></li>
            <li class="sidebar-subitem"><a href="15-project-code-generator.html">15 项目代码生成器</a></li>
            <li class="sidebar-subitem"><a href="16-common-modules.html">16 常见功能模块</a></li>
            <li class="sidebar-subitem"><a href="17-security-development.html">17 安全开发</a></li>
            <li class="sidebar-subitem"><a href="18-test-driven-development.html">18 测试驱动开发</a></li>
            <li><a href="19-testing-quality.html">19 测试·质量</a></li>
            <li><a href="20-performance-tuning.html">20 性能调优</a></li>
            <li><a href="21-devops-cloud-native.html">21 工程化·DevOps·CI/CD</a></li>
            <li><a href="22-ai-development.html">22 AI 辅助开发</a></li>
            <li><a href="23-business-intelligence.html">23 业务智能化</a></li>
            <li><a href="24-palantir-aip.html">24 Palantir AIP 架构</a></li>
            <li><a href="25-agent-development.html">25 Agent 开发</a></li>
            <li><a href="glossary.html">术语字典</a></li>"""

TYPO_FIXES = {
    "流桯": "流程",
    "查间": "查询",
    "参教": "参数",
    "自然语商": "自然语言",
    "故据": "数据",
    "充成": "完成",
    "力克成信想": "未完成信息",
    "信和": "信号",
    "某一荣": "某一类",
    "放漳": "故障",
    "效据": "数据",
    "范国": "范围",
    "信思": "信息",
    "换入": "接入",
    "均可可": "均可",
    "投警": "报警",
    "可维护性查": "可维护性差",
    "Singal": "Single",
    "堤高": "提高",
    "大展": "大屏",
}

REDUNDANT_PATTERNS = [
    re.compile(r"^一、前言"),
    re.compile(r"^二、"),
    re.compile(r"^三、LLM"),
    re.compile(r"^四、Agent\s*$"),
    re.compile(r"^五、"),
    re.compile(r"^六、"),
    re.compile(r"^目录页\s*$"),
    re.compile(r"^演示：\s*$"),
    re.compile(r"^5\. Agent 推理模式\s*$"),
    re.compile(r"^10\. Agent Memory：\s*$"),
    re.compile(r"^11\. Graph RAG：\s*$"),
    re.compile(r"^谢谢！\s*$"),
    re.compile(r"^\d+\.\s*Agent执行流程\s*$"),
    re.compile(r"^\d+\.\s*Agent Tool 完整交互流程：?\s*$"),
    re.compile(r"^14\.\s*Agent 呈现模式：?\s*$"),
    re.compile(r"^9\.\s*Agent Skill"),
]

IMG_DIR = ROOT / "assets" / "agent-ch25"

HARD_CODED_TABLES: dict[int, str] = {
    13: """<div class="table-wrap"><table class="data-table"><thead><tr><th>维度</th><th>模型</th><th>Agent</th></tr></thead><tbody>
<tr><td>知识范围</td><td>知识仅限于其训练数据。</td><td>通过工具连接外部系统，能够在模型自带的知识之外，实时、动态扩展知识。</td></tr>
<tr><td>状态与记忆</td><td>无状态，每次推理都跟上一次没关系，除非在外部给模型加上会话历史或上下文管理能力。</td><td>有状态，自动管理会话历史，根据编排自主决策进行多轮推理。</td></tr>
<tr><td>原生工具</td><td>无。</td><td>有，自带工具和对工具的支持能力。</td></tr>
<tr><td>原生逻辑层</td><td>无。需要借助提示词工程或使用推理框架（CoT、ReAct 等）来形成复杂提示，指导模型进行预测。</td><td>有，原生认知架构，内置 CoT、ReAct 等推理框架或 LangChain 等编排框架。</td></tr>
</tbody></table></div>""",
    35: """<div class="table-wrap"><table class="data-table"><thead><tr><th>框架</th><th>定位与核心能力</th><th>最适合的场景</th><th>学习难度</th></tr></thead><tbody>
<tr><td>LangChain</td><td>LLM 应用基础组件框架：提供模型调用、Tool Calling、Memory、Chain、Agent abstraction，但更偏「组件拼装库」，需要配合 LangGraph 等做复杂编排。</td><td>快速构建 LLM 应用、工具调用系统、多 API 集成、原型开发。</td><td>中到高（API 多且碎片化）</td></tr>
<tr><td>LlamaIndex</td><td>数据与 RAG 专业框架：强调数据 ingestion、indexing、retrieval、query pipeline，也支持 agent 与 workflow，但核心仍是「数据接入层」。</td><td>企业知识库、文档问答、RAG 系统、结构化/非结构化数据检索。</td><td>中等</td></tr>
<tr><td>AutoGen</td><td>多智能体对话系统：以「Agent 之间的对话驱动协作」为核心，支持角色分工、代码执行、工具调用与自动协作。</td><td>多角色协作（分析+写代码+执行）、自动化研究、复杂任务分解。</td><td>中到高（抽象偏研究风格）</td></tr>
<tr><td>CrewAI</td><td>角色驱动的多 Agent 编排框架：以 Role / Task / Process 为核心，强调结构化 workflow，而不是自由对话。</td><td>内容生成流水线（营销/报告）、业务流程自动化、多步骤任务执行。</td><td>低到中（比 AutoGen 更易上手）</td></tr>
</tbody></table></div>""",
    36: """<div class="table-wrap"><table class="data-table"><thead><tr><th>模式</th><th>简介</th><th>典型场景</th><th>实现难度</th><th>实现方式</th></tr></thead><tbody>
<tr><td>Chat Agent（对话式）</td><td>自然语言交互为主，内部流程对用户透明</td><td>问答助手、内容生成、通用分析</td><td>⭐</td><td>单轮/多轮 LLM + Prompt + 基础 Memory + 可选 RAG</td></tr>
<tr><td>Copilot（人机协同）</td><td>Agent 提供建议，人类确认后执行</td><td>IDE Copilot、SQL生成、运营分析</td><td>⭐⭐</td><td>LLM + Suggestion Layer + UI确认机制 + Tool API（human approval gate）</td></tr>
<tr><td>Workflow / Pipeline Agent</td><td>固定流程 DAG，每一步模块化执行</td><td>企业RAG、信息抽取、审核流</td><td>⭐⭐⭐</td><td>LangChain Chains / DAG Orchestrator / Airflow-like LLM pipeline</td></tr>
<tr><td>Autonomous Agent（自主式）</td><td>自主规划 + 执行 + 反思循环</td><td>AutoGPT任务执行、复杂调研</td><td>⭐⭐⭐⭐</td><td>ReAct / Plan-and-Execute / Tool Loop + Memory + Reflection loop</td></tr>
<tr><td>State Machine Agent（状态机）</td><td>状态驱动的确定性流程控制</td><td>MES、风控审批、工业控制</td><td>⭐⭐⭐⭐</td><td>LangGraph / FSM / State Transition Graph + Guardrails + deterministic routing</td></tr>
<tr><td>Event-driven Agent（事件驱动）</td><td>基于事件触发执行，而非用户请求</td><td>AIOps告警、订单处理、监控系统</td><td>⭐⭐⭐⭐</td><td>Event Bus（Kafka/Webhook）+ Agent Listener + Trigger-based Tool execution</td></tr>
<tr><td>UI-native Agent（界面嵌入式）</td><td>Agent 嵌入业务系统 UI 中输出结构化结果</td><td>CRM助手、Excel/BI Copilot</td><td>⭐⭐⭐</td><td>Frontend Widget + Backend Agent Service + Structured Output(JSON schema/function calling)</td></tr>
<tr><td>Multi-agent System（多智能体）</td><td>多个 Agent 分工协作形成组织结构</td><td>研究、复杂工程生成、自动开发系统</td><td>⭐⭐⭐⭐⭐</td><td>Agent orchestration framework（AutoGen / CrewAI / LangGraph multi-node graph）</td></tr>
</tbody></table></div>""",
}


def fix_text(text: str) -> str:
    for old, new in TYPO_FIXES.items():
        text = text.replace(old, new)
    return text


def is_redundant(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    return any(p.match(s) for p in REDUNDANT_PATTERNS)


def linkify(text: str) -> str:
  escaped = html.escape(text)
  escaped = re.sub(
      r"(https?://[^\s<]+)",
      r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
      escaped,
  )
  return escaped


def load_manifest() -> dict[int, list[str]]:
    mapping: dict[int, list[str]] = {}
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        idx_s, files = line.split("\t", 1)
        mapping[int(idx_s)] = [f.strip() for f in files.split(",") if f.strip()]
    return mapping


def parse_slides() -> dict[int, list[str]]:
    raw = TEXT_PATH.read_text(encoding="utf-8")
    slides: dict[int, list[str]] = {}
    current = None
    for line in raw.splitlines():
        m = re.match(r"^--- 第 (\d+) 页 ---$", line.strip())
        if m:
            current = int(m.group(1))
            slides[current] = []
            continue
        if current is None:
            continue
        if line.startswith("===") or line.startswith("幻灯片总数"):
            continue
        slides[current].append(line)
    return slides


def render_images(slide_no: int, caption: str, manifest: dict[int, list[str]]) -> str:
    files = manifest.get(slide_no, [])
    files = [
        f for f in files
        if not re.match(r"slide-\d+-0\.", f)
        and (IMG_DIR / f).exists()
    ]
    if not files:
        return ""
    parts = ['<div class="ppt-slide-figures">']
    for i, fname in enumerate(files, start=1):
        suffix = f"（{i}/{len(files)}）" if len(files) > 1 else ""
        alt = html.escape(f"{caption}{suffix}")
        cap = html.escape(f"图：{caption}{suffix}")
        parts.append(
            f'<figure class="diagram-block diagram-image ppt-slide-figure">'
            f'<img src="assets/agent-ch25/{html.escape(fname)}" alt="{alt}" loading="lazy" />'
            f'<figcaption class="diagram-caption">{cap}</figcaption>'
            f"</figure>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def prose_to_html(lines: list[str]) -> str:
    cleaned = [fix_text(ln.strip()) for ln in lines if ln.strip() and not is_redundant(ln)]
    if not cleaned:
        return ""

    paragraphs: list[str] = []
    buffer: list[str] = []
    for line in cleaned:
        if re.match(r"^\d+[.）)]", line) and buffer:
            paragraphs.append(" ".join(buffer))
            buffer = [line]
            continue
        if line.endswith(("。", "！", "？", "；", ".")) or len(line) > 120:
            buffer.append(line)
            paragraphs.append(" ".join(buffer))
            buffer = []
        else:
            buffer.append(line)
    if buffer:
        paragraphs.append(" ".join(buffer))

    return "\n".join(f"<p>{linkify(p)}</p>" for p in paragraphs)


def merge_table_rows(rows: list[str]) -> list[str]:
    merged: list[str] = []
    for row in rows:
        s = row.strip()
        if not s:
            continue
        if "|" in s:
            merged.append(s)
        elif merged:
            merged[-1] = merged[-1] + " " + s
    return merged


def table_from_pipe_rows(rows: list[str]) -> str:
    rows = merge_table_rows(rows)
    if not rows:
        return ""
    parsed = []
    for row in rows:
        if "|" not in row:
            continue
        cells = [fix_text(c.strip()) for c in row.split("|")]
        parsed.append(cells)
    if not parsed:
        return ""
    header = parsed[0]
    body = parsed[1:] if len(parsed) > 1 else []
    out = ['<div class="table-wrap"><table class="data-table">', "<thead><tr>"]
    for cell in header:
        out.append(f"<th>{html.escape(cell)}</th>")
    out.append("</tr></thead>")
    if body:
        out.append("<tbody>")
        for row in body:
            out.append("<tr>")
            for cell in row:
                out.append(f"<td>{html.escape(cell)}</td>")
            out.append("</tr>")
        out.append("</tbody>")
    out.append("</table></div>")
    return "".join(out)


def split_table_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    table_rows = []
    prose = []
    for ln in lines:
        if "|" in ln and not ln.strip().startswith("http"):
            table_rows.append(ln)
        else:
            prose.append(ln)
    return prose, table_rows


# (id, h2, h3, slide_no, caption, table_title)
SECTIONS = [
    ("agent-learning-map", "学习地图", "本章导览", 2, None, None),
    ("agent-preface-trends", "行业趋势与展望", "白皮书要点", 3, "趋势/展望", None),
    ("agent-preface-selection", "技术选型：LLM vs 规则 vs ML", "决策框架", 4, "选型决策", None),
    ("agent-preface-architecture", "企业级 Agent 架构", "分层与治理", 5, "企业级 Agent 架构", None),
    ("agent-llm", "LLM 基础认知", "基础概念", 8, "LLM 基础", None),
    ("agent-concepts", "Agent 概念与五大模块", "从模型到执行体", 13, "Agent 概念", "模型 vs Agent 对比"),
    ("agent-execution-flow", "Agent 执行流程", "感知—推理—行动闭环", 14, "执行流程", None),
    ("agent-reasoning-modes", "Agent 推理模式", "模式总览", 15, "ReAct", None),
    ("agent-tools", "Agent Tool", "工具定义与 ReAct 范式", 19, "Agent Tool", None),
    ("agent-mcp", "MCP（Model Context Protocol）", "协议概览", 20, "MCP 概览", None),
    ("agent-tool-flow", "Tool 完整交互流程", "端到端调用链路", 23, "Tool 交互流程", None),
    ("agent-skill", "Agent Skill", "能力封装与设计模式", 24, "Agent Skill", None),
    ("agent-memory", "Agent Memory", "Memory 总览", 28, "短期记忆", None),
    ("agent-graph-rag", "Graph RAG", "流程总览", 31, "Graph RAG 流程", None),
    ("agent-single-multi", "Single Agent 与 Multi-Agent", "架构选型经验法则", 34, "单/多 Agent", None),
    ("agent-frameworks", "Agent 框架对比", "LangChain / LlamaIndex 等", 35, "框架对比", "主流框架对比"),
    ("agent-presentation-modes", "Agent 呈现模式", "八种落地形态", 36, "呈现模式", "八种落地模式"),
    ("agent-mes-demo", "MES Trace Agent Demo", "追溯场景演示", 46, "MES Demo", None),
    ("agent-conclusion", "结语", "认知与行动", 47, "结语", None),
]


def build_learning_map(manifest: dict[int, list[str]]) -> str:
    return """
      <section class="section" id="agent-learning-map">
        <h2>学习地图</h2>
        <article class="knowledge-card">
          <h3>本章导览</h3>
          <div class="card-block block-explain">
            <h4>概要</h4>
            <p>从 <strong>LLM 认知</strong>到 <strong>Agent 行动</strong>：覆盖推理编排（ReAct / Plan-and-Execute / CoT / ToT）、Tool / MCP / Skill / Memory / Graph RAG 技术栈，并以 MES 追溯 Demo 收束。与<a href="23-business-intelligence.html">第 23 章业务智能化</a>（需求侧 What/Why）互补；Palantir AIP 平台实践见<a href="24-palantir-aip.html">第 24 章</a>。</p>
          </div>
          <div class="card-block block-deliverable">
            <h4>阅读顺序</h4>
            <ol>
              <li><a href="#agent-preface-trends">前言</a>：趋势、选型与企业级架构</li>
              <li><a href="#agent-llm">LLM 基础</a>：Transformer、训练与推理</li>
              <li><a href="#agent-concepts">Agent 详解</a>：概念、<a href="#agent-reasoning-modes">推理模式</a>、Tool、<a href="#agent-mcp">MCP</a>、Skill、<a href="#agent-memory">Memory</a>、<a href="#agent-graph-rag">Graph RAG</a></li>
              <li><a href="#agent-mes-demo">MES Demo</a>：工业追溯场景演示</li>
            </ol>
          </div>
          <div class="card-block block-memory">
            <h4>速记</h4>
            <p>LLM 负责「回答」，Agent 负责「完成任务」；Tool 是原子接口，Skill 是业务复合能力，Memory 让 Agent 跨越单次对话持续进化。</p>
          </div>
        </article>
      </section>"""


def build_llm_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    subsections = [
        ("agent-llm-basics", "基础概念：Transformer 与注意力", 8, None),
        ("agent-llm-decoder", "Decoder-only 架构", 9, "Decoder-only"),
        ("agent-llm-training", "训练流程：预训练 / SFT / 对齐", 10, "LLM 训练"),
        ("agent-llm-inference", "推理流程：Prefill 与 Decode", 11, "LLM 推理"),
        ("agent-llm-multimodal", "多模态 LLM：理解与生成", 12, "多模态 LLM"),
    ]
    articles: list[str] = []
    for anchor, title, slide_no, cap in subsections:
        prose, _ = split_table_lines(slides.get(slide_no, []))
        body = prose_to_html(prose) or "<p>见配图。</p>"
        imgs = render_images(slide_no, cap, manifest) if cap else ""
        articles.append(f"""
        <article class="knowledge-card" id="{anchor}">
          <h3>{html.escape(title)}</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body}</div>
          {imgs}
        </article>""")
    return f"""
      <section class="section" id="agent-llm">
        <h2>LLM 基础认知</h2>
        {"".join(articles)}
      </section>"""


def build_reasoning_modes_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    modes = [
        ("agent-reasoning-react", "ReAct：推理与行动交替", 15, "ReAct"),
        ("agent-reasoning-plan", "Plan-and-Execute：先规划后执行", 16, "Plan-and-Execute"),
        ("agent-reasoning-cot", "Chain-of-Thought：思维链", 17, "CoT"),
        ("agent-reasoning-tot", "Tree of Thoughts：多分支探索与剪枝", 18, "ToT"),
    ]
    articles: list[str] = [
        """
        <article class="knowledge-card">
          <h3>模式总览</h3>
          <div class="card-block block-explain">
            <h4>概要</h4>
            <p>Agent 推理编排没有唯一最优解，常见四种模式各有适用场景：<strong>ReAct</strong>（边想边做）、<strong>Plan-and-Execute</strong>（先规划后执行）、<strong>CoT</strong>（显式思维链）、<strong>ToT</strong>（多分支探索）。实践中可组合使用，例如 Plan 定框架、ReAct 执行子步骤。</p>
          </div>
        </article>"""
    ]
    for anchor, title, slide_no, cap in modes:
        prose, _ = split_table_lines(slides.get(slide_no, []))
        body = prose_to_html(prose) or "<p>要点见图示。</p>"
        imgs = render_images(slide_no, cap, manifest)
        articles.append(f"""
        <article class="knowledge-card" id="{anchor}">
          <h3>{html.escape(title)}</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body}</div>
          {imgs}
        </article>""")
    return f"""
      <section class="section" id="agent-reasoning-modes">
        <h2>Agent 推理模式</h2>
        {"".join(articles)}
      </section>"""


def build_graph_rag_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    subsections = [
        ("agent-graph-rag-etl", "ETL 与构建：Schema 到图", 31),
        ("agent-graph-rag-query", "查询重写：Cypher 生成", 32),
        ("agent-graph-rag-synthesis", "答案合成：证据整合", 33),
    ]
    articles = [
        """
        <article class="knowledge-card">
          <h3>流程总览</h3>
          <div class="card-block block-explain">
            <h4>概要</h4>
            <p>Graph RAG 的核心观点是：<strong>知识不是文档，而是图</strong>——(实体) —[关系]→ (实体)。典型链路为：关系数据 ETL 入图 → 自然语言查询重写为 Cypher → 用图查询结果增强 LLM 最终生成。</p>
            <p>常用图数据库：Neo4j、TigerGraph、Neptune（AWS）。</p>
          </div>
        </article>"""
    ]
    for anchor, title, slide_no in subsections:
        prose, _ = split_table_lines(slides.get(slide_no, []))
        body = prose_to_html(prose) or "<p>见流程总览与配图。</p>"
        articles.append(f"""
        <article class="knowledge-card" id="{anchor}">
          <h3>{html.escape(title)}</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body}</div>
        </article>""")
    img = render_images(31, "Graph RAG 流程", manifest)
    return f"""
      <section class="section" id="agent-graph-rag">
        <h2>Graph RAG</h2>
        {"".join(articles)}
        {img}
      </section>"""


def build_memory_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    subsections = [
        ("agent-memory-short", "短期记忆：上下文窗口", 28, None),
        ("agent-memory-long", "长期记忆：向量库与知识图谱", 29, "长期记忆"),
        ("agent-memory-rag", "工具性/知识记忆：Agentic RAG", 30, "知识记忆"),
    ]
    articles = [
        """
        <article class="knowledge-card">
          <h3>Memory 总览</h3>
          <div class="card-block block-memory">
            <h4>概要</h4>
            <p>LLM 本身无状态，无法跨会话积累经验。Agent Memory 是<strong>可检索、可更新、可压缩、可推理使用</strong>的外部认知层，由「短期 + 长期 + 工具性/知识记忆」三层构成，目标是跨时间一致性、经验积累与个性化决策。</p>
          </div>
        </article>"""
    ]
    for anchor, title, slide_no, cap in subsections:
        prose, _ = split_table_lines(slides.get(slide_no, []))
        body = prose_to_html(prose) or "<p>见总览与配图。</p>"
        imgs = render_images(slide_no, cap, manifest) if cap else ""
        articles.append(f"""
        <article class="knowledge-card" id="{anchor}">
          <h3>{html.escape(title)}</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body}</div>
          {imgs}
        </article>""")
    return f"""
      <section class="section" id="agent-memory">
        <h2>Agent Memory</h2>
        {"".join(articles)}
      </section>"""


def build_mcp_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    prose_20, _ = split_table_lines(slides.get(20, []))
    prose_21, _ = split_table_lines(slides.get(21, []))
    prose_22, _ = split_table_lines(slides.get(22, []))
    body_overview = prose_to_html(prose_20)
    body_init = prose_to_html(prose_21)
    body_exec = prose_to_html(prose_22)
    imgs_overview = render_images(20, "MCP 概览", manifest)
    imgs_init = render_images(21, "MCP 初始化与发现", manifest)
    imgs_exec = render_images(22, "MCP 执行与通知", manifest)
    return f"""
      <section class="section" id="agent-mcp">
        <h2>MCP（Model Context Protocol）</h2>
        <article class="knowledge-card" id="agent-mcp-overview">
          <h3>协议概览：架构与基本元素</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body_overview or '<p>要点见图示。</p>'}</div>
          {imgs_overview}
        </article>
        <article class="knowledge-card" id="agent-mcp-lifecycle">
          <h3>生命周期：初始化与工具发现</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body_init or '<p>要点见图示。</p>'}</div>
          {imgs_init}
        </article>
        <article class="knowledge-card" id="agent-mcp-execution">
          <h3>生命周期：工具执行与实时通知</h3>
          <div class="card-block block-explain"><h4>概要</h4>{body_exec or '<p>要点见图示。</p>'}</div>
          {imgs_exec}
        </article>
      </section>"""


def build_skill_section(slides: dict[int, list[str]], manifest: dict[int, list[str]]) -> str:
    extra_note = (
        '<p>Skill 开放标准可参考 '
        '<a href="https://agentskills.io/" target="_blank" rel="noopener noreferrer">agentskills.io</a>。</p>'
    )
    fig_parts = [
        render_images(24, "Skill 与 Tool 分层", manifest),
        render_images(25, "Skill 标准参考", manifest),
        render_images(26, "五种设计模式", manifest),
        render_images(27, "领域专家 Skill 库", manifest),
    ]
    imgs_html: list[str] = []
    for part in fig_parts:
        if not part:
            continue
        imgs_html.append(re.sub(r"</?div class=\"ppt-slide-figures\">", "", part))
    figs = f'<div class="ppt-slide-figures">{"".join(imgs_html)}</div>' if imgs_html else ""
    return f"""
      <section class="section" id="agent-skill">
        <h2>Agent Skill</h2>
        <article class="knowledge-card">
          <h3>能力封装与设计模式</h3>
          <div class="card-block block-explain">
            <h4>概要</h4>
            <p><strong>Skill</strong> 是面向特定业务场景的高阶能力封装（Capabilities），由提示词（Prompt）、工作流（Workflow）、知识库（RAG）以及一个或多个 Tool 组合而成。它是有状态的、具备业务逻辑，本质上是把「通用推理能力」扩展成「领域专家能力」。</p>
            <p><strong>Tool</strong> 是 Agent 可调用的外部能力接口（原子化）；<strong>Skill</strong> 是为完成某类任务封装好的能力组合（复合型）。</p>
            <ul>
              <li><strong>底层 (Tools)</strong>：开发人员将 ERP、MES、数据库、物联网设备等封装为 OpenAPI 或通用组件。</li>
              <li><strong>中层 (Skills)</strong>：业务专家或 AI 编排师将 Tools 与 System Prompt、SOP 流程、向量库连接，配置出岗位 Skill。</li>
              <li><strong>上层 (Agent)</strong>：挂载多个 Skill，按用户指令调度 Skill，再由 Skill 调用底层 Tools。</li>
            </ul>
            {extra_note}
          </div>
          {figs}
        </article>
      </section>"""


def build_section(
    sec_id: str,
    h2: str,
    h3: str,
    slide_no: int,
    caption: str | None,
    table_title: str | None,
    slides: dict[int, list[str]],
    manifest: dict[int, list[str]],
) -> str:
    lines = slides.get(slide_no, [])
    prose, table_rows = split_table_lines(lines)
    cap = caption or h3
    body: list[str] = []
    pb = prose_to_html(prose)
    tbl = HARD_CODED_TABLES.get(slide_no) or table_from_pipe_rows(table_rows)
    skip_prose = slide_no in HARD_CODED_TABLES or (
        tbl and prose and len(prose) <= 2 and all(is_redundant(ln) or re.match(r"^\d+\.", ln.strip()) for ln in prose)
    )
    if pb and not skip_prose:
        body.append(f'<div class="card-block block-explain"><h4>概要</h4>{pb}</div>')
    if tbl:
        title = html.escape(table_title or "对照表")
        body.append(f'<div class="card-block block-deliverable"><h4>{title}</h4>{tbl}</div>')
    imgs = render_images(slide_no, cap, manifest)
    if imgs:
        if not body:
            body.append('<div class="card-block block-explain"><p>要点见图示。</p></div>')
        body.append(imgs)

    if not body:
        body.append('<div class="card-block block-explain"><p>（暂无正文，待补充。）</p></div>')

    return f"""
      <section class="section" id="{sec_id}">
        <h2>{html.escape(h2)}</h2>
        <article class="knowledge-card">
          <h3>{html.escape(h3)}</h3>
          {"".join(body)}
        </article>
      </section>"""


def main() -> None:
    slides = parse_slides()
    manifest = load_manifest()
    parts: list[str] = [build_learning_map(manifest)]

    skip_ids = {"agent-learning-map", "agent-mcp-lifecycle-a", "agent-mcp-lifecycle-b",
                "agent-mcp-overview", "agent-skill-overview", "agent-skill-agentskills", "agent-skill-patterns", "agent-skill-structure",
                "agent-reasoning-react", "agent-reasoning-plan", "agent-reasoning-cot", "agent-reasoning-tot",
                "agent-graph-rag-etl", "agent-graph-rag-query", "agent-graph-rag-synthesis",
                "agent-memory-short", "agent-memory-long", "agent-memory-rag",
                "agent-mcp-overview",
                "agent-llm-basics", "agent-llm-decoder", "agent-llm-training",
                "agent-llm-inference", "agent-llm-multimodal"}

    for sec_id, h2, h3, slide_no, cap, table_title in SECTIONS:
        if sec_id == "agent-learning-map":
            continue
        if sec_id == "agent-llm":
            parts.append(build_llm_section(slides, manifest))
            continue
        if sec_id == "agent-reasoning-modes":
            parts.append(build_reasoning_modes_section(slides, manifest))
            continue
        if sec_id == "agent-graph-rag":
            parts.append(build_graph_rag_section(slides, manifest))
            continue
        if sec_id == "agent-mcp":
            parts.append(build_mcp_section(slides, manifest))
            continue
        if sec_id == "agent-memory":
            parts.append(build_memory_section(slides, manifest))
            continue
        if sec_id == "agent-skill":
            parts.append(build_skill_section(slides, manifest))
            continue
        parts.append(build_section(sec_id, h2, h3, slide_no, cap, table_title, slides, manifest))

    sections_html = "".join(parts)

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>25 Agent 开发 — Java项目手册</title>
  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/sidebar.js" defer></script>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">Java项目手册</div>
      <nav>
        <div class="nav-group">
          <ul class="nav-list">
{SIDEBAR}
          </ul>
        </div>
      </nav>
    </aside>

    <main class="main">
      <header class="page-header">
        <h1>25 Agent 开发：LLM 与 Agent 实践</h1>
        <p>从<strong>LLM 认知</strong>到<strong>Agent 行动</strong>——系统梳理 Agent 推理编排、工具协议与企业落地路径。承接<a href="23-business-intelligence.html">第 23 章业务智能化</a>的需求视角；Palantir AIP 平台实践见<a href="24-palantir-aip.html">第 24 章</a>。</p>
      </header>
{sections_html}
      <nav class="chapter-nav">
        <a href="24-palantir-aip.html">← 上一章：Palantir AIP 架构</a>
        <a href="glossary.html">下一章：术语字典 →</a>
      </nav>
    </main>
  </div>
  <script src="assets/diagram.js" defer></script>
  <script src="assets/explain-format.js" defer></script>
  <script src="assets/chapter-toc.js" defer></script>
</body>
</html>
"""
    OUT_PATH.write_text(page, encoding="utf-8")
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
