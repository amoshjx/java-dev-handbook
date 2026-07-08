# -*- coding: utf-8 -*-
"""Polish chapter 25 HTML layout: fix tables, dedupe, improve readability."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "25-agent-development.html"

TABLE_AGENT_VS_MODEL = """<div class="card-block block-deliverable"><h4>模型 vs Agent 对比</h4><div class="table-wrap"><table class="data-table"><thead><tr><th>维度</th><th>模型</th><th>Agent</th></tr></thead><tbody>
<tr><td>知识范围</td><td>知识仅限于其训练数据。</td><td>通过工具连接外部系统，能够在模型自带的知识之外，实时、动态扩展知识。</td></tr>
<tr><td>状态与记忆</td><td>无状态，每次推理都跟上一次没关系，除非在外部给模型加上会话历史或上下文管理能力。</td><td>有状态，自动管理会话历史，根据编排自主决策进行多轮推理。</td></tr>
<tr><td>原生工具</td><td>无。</td><td>有，自带工具和对工具的支持能力。</td></tr>
<tr><td>原生逻辑层</td><td>无。需要借助提示词工程或使用推理框架（CoT、ReAct 等）来形成复杂提示，指导模型进行预测。</td><td>有，原生认知架构，内置 CoT、ReAct 等推理框架或 LangChain 等编排框架。</td></tr>
</tbody></table></div></div>"""

TABLE_FRAMEWORKS = """<div class="card-block block-deliverable"><h4>主流框架对比</h4><div class="table-wrap"><table class="data-table"><thead><tr><th>框架</th><th>定位与核心能力</th><th>最适合的场景</th><th>学习难度</th></tr></thead><tbody>
<tr><td>LangChain</td><td>LLM 应用基础组件框架：提供模型调用、Tool Calling、Memory、Chain、Agent abstraction，但更偏「组件拼装库」，需要配合 LangGraph 等做复杂编排。</td><td>快速构建 LLM 应用、工具调用系统、多 API 集成、原型开发。</td><td>中到高（API 多且碎片化）</td></tr>
<tr><td>LlamaIndex</td><td>数据与 RAG 专业框架：强调数据 ingestion、indexing、retrieval、query pipeline，也支持 agent 与 workflow，但核心仍是「数据接入层」。</td><td>企业知识库、文档问答、RAG 系统、结构化/非结构化数据检索。</td><td>中等</td></tr>
<tr><td>AutoGen</td><td>多智能体对话系统：以「Agent 之间的对话驱动协作」为核心，支持角色分工、代码执行、工具调用与自动协作。</td><td>多角色协作（分析+写代码+执行）、自动化研究、复杂任务分解。</td><td>中到高（抽象偏研究风格）</td></tr>
<tr><td>CrewAI</td><td>角色驱动的多 Agent 编排框架：以 Role / Task / Process 为核心，强调结构化 workflow，而不是自由对话。</td><td>内容生成流水线（营销/报告）、业务流程自动化、多步骤任务执行。</td><td>低到中（比 AutoGen 更易上手）</td></tr>
</tbody></table></div></div>"""

SECTION_LLM_BASICS = """          <div class="card-block block-explain">
            <h4>概要</h4>
            <p><strong>LLM（Large Language Model）</strong>是在超大文本语料上训练的「概率生成模型」——基于 Transformer，核心任务是预测「给定前文，下一个 token 最可能是什么」。当模型足够大、数据足够多时，这种「接龙」能力会涌现出语言理解、推理、代码生成等复杂行为。</p>
            <ul>
              <li><strong>Transformer</strong>：LLM 的核心算法架构。</li>
              <li><strong>Self-Attention（自注意力）</strong>：句中每个词向上下文询问「谁对我最重要」，注意力权重由模型训练得出。</li>
              <li><strong>Multi-Head Attention（多头注意力）</strong>：多个子空间并行分析——语法、语义、指代、长距离依赖等，相当于多个「分析师」同时解读同一句子。</li>
            </ul>
          </div>"""

SECTION_AGENT_CONCEPTS = """          <div class="card-block block-explain">
            <h4>概要</h4>
            <p><strong>Agent（智能体）</strong>是「会思考 + 会行动 + 会反思」、能自主完成多步任务的 AI 执行体。LLM 只会「回答」，Agent 能「完成任务」（多步执行 + 调用工具 + 状态管理）。</p>
            <p><strong>五大模块</strong>：</p>
            <ol>
              <li><strong>LLM（大脑）</strong>：推理与语言理解</li>
              <li><strong>Reasoning &amp; Planning</strong>：拆解任务、生成步骤、推理调度</li>
              <li><strong>Tools / Skill System</strong>：API、DB、Web、Code、Prompt</li>
              <li><strong>Memory</strong>：短期上下文 + 长期知识 / 向量库</li>
              <li><strong>Executor</strong>：调用工具、运行代码、返回结果</li>
            </ol>
          </div>"""

SECTION_AGENT_TOOLS = """          <div class="card-block block-explain">
            <h4>概要</h4>
            <p>Tool 给 LLM「大脑」接上可执行的外部世界接口，扩展能力边界。Agent 使用工具通常遵循 <strong>ReAct</strong> 范式：Thought → Action → Tool → Observation 循环。</p>
            <p><strong>为什么需要 Tool？</strong>大模型存在四类典型短板：</p>
            <ul>
              <li><strong>时效性盲区</strong>：无法获取实时信息（天气、股价等）</li>
              <li><strong>私有数据隔离</strong>：行业关键数据需受控接入推理链路</li>
              <li><strong>计算能力差</strong>：高精度数学运算易出现幻觉</li>
              <li><strong>无法直接执行操作</strong>：订票、发邮件、设备控制等需外部系统</li>
            </ul>
            <p><strong>Tool 类型</strong>：Function Calling、API 封装、系统能力封装、MCP 调用。每个工具需精准的 Name、Description 与 Parameters Schema；设计原则为清晰语义、可组合、低歧义参数。</p>
          </div>"""

SECTION_SKILL = """          <div class="card-block block-explain">
            <h4>概要</h4>
            <p><strong>Skill</strong> 是面向特定业务场景的高阶能力封装，由 Prompt、Workflow、RAG 与一个或多个 Tool 组合而成，把「通用推理」扩展为「领域专家能力」。</p>
            <p><strong>Tool vs Skill</strong>：Tool 是原子化外部接口；Skill 是面向任务的复合型能力组合。</p>
            <ul>
              <li><strong>底层 (Tools)</strong>：ERP、MES、数据库、物联网等封装为 OpenAPI 或通用组件</li>
              <li><strong>中层 (Skills)</strong>：业务专家将 Tools 与 System Prompt、SOP、向量库连接为岗位 Skill</li>
              <li><strong>上层 (Agent)</strong>：挂载多 Skill，按指令调度，由 Skill 调用底层 Tools</li>
            </ul>
            <p>开放标准参考 <a href="https://agentskills.io/" target="_blank" rel="noopener noreferrer">agentskills.io</a>。</p>
          </div>"""

SECTION_MEMORY_INTRO = """          <div class="card-block block-memory">
            <h4>Memory 总览</h4>
            <p>LLM 本身无状态，无法跨会话积累经验。Agent Memory 是<strong>可检索、可更新、可压缩、可推理使用</strong>的外部认知层，由「短期 + 长期 + 工具性/知识记忆」构成，目标是跨时间一致性、经验积累与个性化决策。</p>
          </div>"""


def replace_section_block(html: str, section_id: str, old_pattern: str, new_content: str) -> str:
    m = re.search(
        rf'(<section class="section" id="{section_id}">.*?<article class="knowledge-card">.*?<h3>[^<]+</h3>\s*){old_pattern}',
        html,
        flags=re.S,
    )
    if not m:
        print(f"WARN: block not found for {section_id}")
        return html
    return html[: m.start(1)] + m.group(1) + new_content + html[m.end(1) :]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")

    # Fix broken tables
    html = re.sub(
        r'<div class="card-block block-deliverable"><h4>模型 vs Agent 对比</h4><div class="table-wrap"><table class="data-table">.*?</table></div></div>',
        TABLE_AGENT_VS_MODEL,
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>13\. Agent 框架/组件：</li></ul>.*?</div><div class="card-block block-deliverable"><h4>主流框架对比</h4><div class="table-wrap"><table class="data-table">.*?</table></div></div>',
        TABLE_FRAMEWORKS,
        html,
        count=1,
        flags=re.S,
    )

    # Image-only sections: add brief intro
    for sec_id, text in [
        ("agent-preface-selection", "在不同场景下，应在 LLM、规则引擎与传统 ML 之间做选型权衡。要点见图示。"),
        ("agent-preface-architecture", "企业级 Agent 通常包含接入层、编排层、工具层、记忆层与治理层。要点见图示。"),
        ("agent-execution-flow", "典型闭环为：感知输入 → 推理规划 → 工具执行 → 观察反馈 → 迭代直至任务完成。"),
        ("agent-tool-flow", "从用户意图到 Tool 注册、调用、结果回注 LLM 的完整链路。要点见图示。"),
        ("agent-mes-demo", "MES 追溯场景：通过 Agent 串联工单、批次、设备与质检数据，实现自然语言驱动的根因分析。"),
    ]:
        html = re.sub(
            rf'(<section class="section" id="{sec_id}">.*?<h3>[^<]+</h3>\s*)(<div class="ppt-slide-figures">)',
            rf'\1<div class="card-block block-explain"><p>{text}</p></div>\2',
            html,
            count=1,
            flags=re.S,
        )

    # Remove stub-only explain blocks before images
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>4\. Agent执行流程</li></ul></div>',
        "",
        html,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>8\. Agent Tool 完整交互流程：</li></ul></div>',
        "",
        html,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>14\. Agent 呈现模式：</li></ul></div>',
        "",
        html,
    )

    # Replace key content blocks
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>1\. LLM.*?</ul></div>',
        SECTION_LLM_BASICS,
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>1\. Agent概念及特点</li></ul>.*?</div><div class="card-block block-deliverable"><h4>模型 vs Agent 对比</h4>',
        SECTION_AGENT_CONCEPTS + "\n" + '          <div class="card-block block-deliverable"><h4>模型 vs Agent 对比</h4>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>6\. Agent Tool：.*?</ul>\s*<p>可组合性.*?</p></div>',
        SECTION_AGENT_TOOLS,
        html,
        count=1,
        flags=re.S,
    )

    # Skill section body
    html = re.sub(
        r'<div class="card-block block-explain">\s*<h4>概要</h4>\s*<p>是面向特定业务场景.*?</div>\s*<div class="ppt-slide-figures">',
        SECTION_SKILL + "\n          <div class=\"ppt-slide-figures\">",
        html,
        count=1,
        flags=re.S,
    )

    # Merge multiple ppt-slide-figures in skill section into one
    html = re.sub(
        r'(<section class="section" id="agent-skill">.*?<div class="ppt-slide-figures">)(.*?)(</article>\s*</section>)',
        lambda m: m.group(1) + re.sub(r'</div>\s*<div class="ppt-slide-figures">', "\n", m.group(2), flags=re.S) + m.group(3),
        html,
        count=1,
        flags=re.S,
    )

    # Memory intro before short-term section
    html = re.sub(
        r'(<section class="section" id="agent-memory-short">.*?<h3>上下文窗口</h3>\s*)<div class="card-block block-explain">',
        r"\1" + SECTION_MEMORY_INTRO + "\n          <div class=\"card-block block-explain\">",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>10\. Agent Memory：.*?</li></ul>\s*<p>大语言模型.*?</p>\s*<p>Agent Memory.*?</p>\s*<p>构成：.*?</p>\s*<p>目标：.*?</p>\s*',
        '<div class="card-block block-explain"><h4>短期记忆</h4>\n            ',
        html,
        count=1,
        flags=re.S,
    )

    # Fix figure caption numbering after removed images
    html = html.replace("（2/3）", "（1/2）").replace("（3/3）", "（2/2）")

    # Trim learning map duplicate (shorter概要)
    html = re.sub(
        r'(<section class="section" id="agent-learning-map">.*?<h4>概要</h4>\s*<p>).*?(</p>\s*</div>\s*<div class="card-block block-deliverable">)',
        r"\1本章按「前言 → LLM 基础 → Agent 技术栈 → MES Demo」组织，与第 23 章（需求侧）互补，Palantir AIP 详见第 24 章。\2",
        html,
        count=1,
        flags=re.S,
    )

    # CoT section cleanup
    html = re.sub(
        r'<div class="card-block block-explain"><h4>概要</h4><ul><li>3）Chain-of-Thought.*?</li></ul>\s*<p>“对于需要多步推理.*?</p>\s*<ul><li>Zero-shot CoT.*?</li></ul>\s*<p>如“ 请一步一步思考 ”.*?</p>\s*<ul><li>Few-shot CoT.*?</li></ul>\s*<p>先提供几个.*?</p>\s*<p>模型会“照葫芦画瓢”.*?</p>\s*<ul><li>Auto-CoT：.*?</li></ul></div>',
        """<div class="card-block block-explain">
            <h4>概要</h4>
            <p><strong>Chain-of-Thought (CoT)</strong> 让 LLM 逐步写出中间推理过程。对多步推理任务，在 Prompt 中加入「let's think step by step」或提供推理示例，可显著提升准确率。</p>
            <p><strong>三种实现</strong>：</p>
            <ul>
              <li><strong>Zero-shot CoT</strong>：在提问末尾加「请一步一步思考」</li>
              <li><strong>Few-shot CoT</strong>：在 Prompt 中提供「问题 + 推理步骤 + 答案」示例</li>
              <li><strong>Auto-CoT</strong>：让模型自动生成推理示例</li>
            </ul>
          </div>""",
        html,
        count=1,
        flags=re.S,
    )

    HTML.write_text(html, encoding="utf-8")
    print("polished:", HTML)


if __name__ == "__main__":
    main()
