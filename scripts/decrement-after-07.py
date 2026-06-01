#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decrement chapter numbers 09-23 -> 08-22 (fill missing 08 slot)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RENAMES = {
    9: "jvm",
    10: "concurrency",
    11: "io-nio-network",
    12: "persistence",
    13: "spring-framework",
    14: "build-packaging-deploy",
    15: "ruoyi-framework",
    16: "common-modules",
    17: "security-development",
    18: "test-driven-development",
    19: "testing-quality",
    20: "performance-tuning",
    21: "devops-cloud-native",
    22: "ai-development",
    23: "business-intelligence",
}

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
            <li class="sidebar-subitem"><a href="16-common-modules.html">15 常见功能模块</a></li>
            <li class="sidebar-subitem"><a href="17-security-development.html">16 安全开发</a></li>
            <li class="sidebar-subitem"><a href="18-test-driven-development.html">17 测试驱动开发</a></li>
            <li><a href="19-testing-quality.html">18 测试·质量</a></li>
            <li><a href="20-performance-tuning.html">19 性能调优</a></li>
            <li><a href="21-devops-cloud-native.html">20 工程化·DevOps</a></li>
            <li><a href="22-ai-development.html">21 AI 辅助开发</a></li>
            <li><a href="23-business-intelligence.html">22 业务智能化</a></li>
            <li><a href="glossary.html">术语字典</a></li>"""

CHAPTER_META = {
    "08-jvm.html": ("08 JVM", "08 JVM"),
    "09-concurrency.html": ("09 并发编程", "09 并发编程"),
    "10-io-nio-network.html": ("10 IO·NIO·网络", "10 IO·NIO·网络"),
    "11-persistence.html": ("11 持久化", "11 持久化"),
    "12-spring-framework.html": ("12 Spring Framework", "12 Spring Framework"),
    "13-build-packaging-deploy.html": (
        "13 项目构建、打包与部署",
        "13 项目构建、打包与部署",
    ),
    "14-ruoyi-framework.html": ("14 RuoYi 框架", "14 RuoYi 框架"),
    "16-common-modules.html": ("15 常见功能模块", "15 常见功能模块"),
    "17-security-development.html": ("16 安全开发", "16 安全开发"),
    "18-test-driven-development.html": ("17 测试驱动开发", "17 测试驱动开发"),
    "19-testing-quality.html": ("18 测试·质量", "18 测试·质量"),
    "20-performance-tuning.html": ("19 性能调优", "19 性能调优"),
    "21-devops-cloud-native.html": ("20 工程化·DevOps", "20 工程化·DevOps"),
    "22-ai-development.html": ("21 AI 辅助开发", "21 AI 辅助开发"),
    "23-business-intelligence.html": (
        "22 业务智能化",
        "22 业务智能化与 LLM 能力需求",
    ),
}

NAV_BLOCK = {
    "07-oop.html": (
        '<a href="06-java-basics.html">← 上一章：Java基础语法</a>\n'
        '        <a href="08-jvm.html">下一章：JVM →</a>'
    ),
    "08-jvm.html": (
        '<a href="07-oop.html">← 上一章：面向对象</a>\n'
        '        <a href="09-concurrency.html">下一章：并发编程 →</a>'
    ),
    "09-concurrency.html": (
        '<a href="08-jvm.html">← 上一章：JVM</a>\n'
        '        <a href="10-io-nio-network.html">下一章：IO·NIO·网络 →</a>'
    ),
    "10-io-nio-network.html": (
        '<a href="09-concurrency.html">← 上一章：并发编程</a>\n'
        '        <a href="11-persistence.html">下一章：持久化 →</a>'
    ),
    "11-persistence.html": (
        '<a href="10-io-nio-network.html">← 上一章：IO·NIO·网络</a>\n'
        '        <a href="12-spring-framework.html">下一章：Spring Framework →</a>'
    ),
    "12-spring-framework.html": (
        '<a href="11-persistence.html">← 上一章：持久化</a>\n'
        '        <a href="13-build-packaging-deploy.html">下一章：项目构建、打包与部署 →</a>'
    ),
    "13-build-packaging-deploy.html": (
        '<a href="12-spring-framework.html">← 上一章：Spring Framework</a>\n'
        '        <a href="14-ruoyi-framework.html">下一章：RuoYi 框架 →</a>'
    ),
    "14-ruoyi-framework.html": (
        '<a href="13-build-packaging-deploy.html">← 上一章：项目构建、打包与部署</a>\n'
        '        <a href="16-common-modules.html">下一章：常见功能模块 →</a>'
    ),
    "16-common-modules.html": (
        '<a href="14-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n'
        '        <a href="17-security-development.html">下一章：安全开发 →</a>'
    ),
    "17-security-development.html": (
        '<a href="16-common-modules.html">← 上一章：常见功能模块</a>\n'
        '        <a href="18-test-driven-development.html">下一章：测试驱动开发 →</a>'
    ),
    "18-test-driven-development.html": (
        '<a href="17-security-development.html">← 上一章：安全开发</a>\n'
        '        <a href="19-testing-quality.html">下一章：测试·质量 →</a>'
    ),
    "19-testing-quality.html": (
        '<a href="18-test-driven-development.html">← 上一章：测试驱动开发</a>\n'
        '        <a href="20-performance-tuning.html">下一章：性能调优 →</a>'
    ),
    "20-performance-tuning.html": (
        '<a href="19-testing-quality.html">← 上一章：测试·质量</a>\n'
        '        <a href="21-devops-cloud-native.html">下一章：工程化·DevOps →</a>'
    ),
    "21-devops-cloud-native.html": (
        '<a href="20-performance-tuning.html">← 上一章：性能调优</a>\n'
        '        <a href="22-ai-development.html">下一章：AI 辅助开发 →</a>'
    ),
    "22-ai-development.html": (
        '<a href="21-devops-cloud-native.html">← 上一章：工程化·DevOps</a>\n'
        '        <a href="23-business-intelligence.html">下一章：业务智能化 →</a>'
    ),
    "23-business-intelligence.html": (
        '<a href="22-ai-development.html">← 上一章：AI 辅助开发</a>\n'
        '        <a href="glossary.html">下一章：术语字典 →</a>'
    ),
}

TEXT_FIXES = [
    ("22–23", "21–22"),
    ("23-23", "22-22"),
    ("18–21", "17–20"),
    ("19-21", "18-20"),
    ("13–17", "12–16"),
    ("13-17", "12-16"),
    ("05–18", "05–18"),
    ("05-18", "05-18"),
    ("05–12", "05–11"),
    ("05-12", "05-11"),
    ("06-12", "06-11"),
    ("06–12", "06–11"),
    ("17-17", "16-16"),
    ("16–17", "15–16"),
    ("05 → 18 → 19", "05 → 18 → 19"),
    ("18 → 19", "18 → 19"),
    ("23 章", "22 章"),
    ("22 章面向", "21 章面向"),
    ("23 章面向", "22 章面向"),
    ('C19 --> C20["19 测试·质量"]', 'C18 --> C19["18 测试·质量"]'),
    ('C19["18 TDD"]', 'C18["17 TDD"]'),
    ('C16 --> BACK["17-17 业务与安全"]', 'C14 --> BACK["16-16 业务与安全"]'),
    ('C16["15 RuoYi"]', 'C14["14 RuoYi"]'),
    ('C14["14 构建·打包·部署"]', 'C13["13 构建·打包·部署"]'),
    ('C13 --> C14', 'C12 --> C13'),
    ('C13["13 Spring Framework"]', 'C12["12 Spring Framework"]'),
    ('LANG --> C13', 'LANG --> C12'),
    ('05 → 18 → 19', "05 → 18 → 19"),
    ("图：开发实现章组阅读顺序（05 → 18 → 19）", "图：开发实现章组阅读顺序（05 → 18 → 19）"),
    ("P3 --> P4", "P3 --> P4"),  # noop anchor
]

SKIP_FILES = {"mermaid.min.js"}


def rename_files() -> None:
    temp_paths: list[tuple[Path, Path]] = []
    for old_num, slug in RENAMES.items():
        old_path = ROOT / f"{old_num:02d}-{slug}.html"
        if not old_path.exists():
            raise FileNotFoundError(old_path)
        temp_path = ROOT / f"__decr_{old_num:02d}-{slug}.html"
        old_path.rename(temp_path)
        temp_paths.append((temp_path, ROOT / f"{old_num - 1:02d}-{slug}.html"))

    for temp_path, final_path in temp_paths:
        temp_path.rename(final_path)
        print(f"  {temp_path.name} -> {final_path.name}")


def placeholder_paths(text: str) -> str:
    for old_num in sorted(RENAMES, reverse=True):
        text = text.replace(f"{old_num:02d}-", f"__CH{old_num:02d}__")
    for old_num in RENAMES:
        text = text.replace(f"__CH{old_num:02d}__", f"{old_num - 1:02d}-")
    return text


def placeholder_chapter_nums(text: str) -> str:
    for old_num in sorted(RENAMES, reverse=True):
        old = f"{old_num:02d}"
        new = f"{old_num - 1:02d}"
        text = text.replace(f"第 {old} 章", f"__CHN{old}__")
        text = text.replace(f"第{old}章", f"__CHN{old}__")
        text = re.sub(rf">\s*{old}\s+", lambda _m, o=old: f">__LNK{o}__ ", text)
        text = re.sub(rf'index-chapter-num">{old}<',
            f'index-chapter-num">__IDX{old}<',
            text,
        )
        text = text.replace(f'["{old} ', f'["__QT{old}__ ')
        text = re.sub(rf"\bC{old}\b", f"__CN{old}__", text)
    for old_num in RENAMES:
        old = f"{old_num:02d}"
        new = f"{old_num - 1:02d}"
        text = text.replace(f"__CHN{old}__", f"第 {new} 章")
        text = text.replace(f"__LNK{old}__", f">{new} ")
        text = text.replace(f'index-chapter-num">__IDX{old}<', f'index-chapter-num">{new}<')
        text = text.replace(f'["__QT{old}__ ', f'["{new} ')
        text = text.replace(f"__CN{old}__", f"C{new}")
    return text


def apply_text_fixes(text: str) -> str:
    for old, new in TEXT_FIXES:
        if old != new:
            text = text.replace(old, new)
    return text


def replace_sidebar(text: str) -> str:
    return re.sub(
        r'(?s)<li><a href="index\.html">目录首页</a></li>.*?</ul>',
        SIDEBAR + "\n          </ul>",
        text,
        count=1,
    )


def fix_titles(path: Path, text: str) -> str:
    meta = CHAPTER_META.get(path.name)
    if not meta:
        return text
    title, h1 = meta
    text = re.sub(r"<title>.*?</title>", f"<title>{title} — Java项目手册</title>", text, count=1)
    text = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", text, count=1)
    return text


def fix_nav(path: Path, text: str) -> str:
    if path.name not in NAV_BLOCK:
        return text
    inner = NAV_BLOCK[path.name]
    return re.sub(
        r'<nav class="chapter-nav">.*?</nav>',
        f'<nav class="chapter-nav">\n        {inner}\n      </nav>',
        text,
        count=1,
        flags=re.DOTALL,
    )


def transform_text(text: str) -> str:
    text = placeholder_paths(text)
    text = apply_text_fixes(text)
    text = placeholder_chapter_nums(text)
    return text


def update_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = transform_text(text)
    if path.name not in ("index.html", "glossary.html"):
        text = replace_sidebar(text)
        text = fix_titles(path, text)
        text = fix_nav(path, text)
    else:
        text = replace_sidebar(text)
    path.write_text(text, encoding="utf-8")


def update_other(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(transform_text(text), encoding="utf-8")


def update_readme() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = transform_text(text)
    text = text.replace("22 章知识点", "22 章知识点")
    text = text.replace(
        "`05-dev-environment.html` ~ `18-test-driven-development.html`：开发实现子章（二级，编号 05–18；含 `12-persistence.html`、`14-ruoyi-framework.html`；`06-java-basics.html` 含集合/泛型/Stream 内容，`08` 编号已移除）",
        "`05-dev-environment.html` ~ `18-test-driven-development.html`：开发实现子章（二级，编号 05–18；含 `11-persistence.html`、`14-ruoyi-framework.html`；`06-java-basics.html` 含集合/泛型/Stream 内容）",
    )
    text = text.replace(
        "`19-testing-quality.html` ~ `23-business-intelligence.html`：测试·性能·交付·AI（一级章）",
        "`19-testing-quality.html` ~ `23-business-intelligence.html`：测试·性能·交付·AI（一级章）",
    )
    text = text.replace(
        "侧边栏为 **2 级目录**：`01`–`04` 与 `18`–`22` 为一级项；`05`–`17` 归入 **开发实现** 分组（缩进子项）。章节 prev/next 线性导航仍为 03 → 04 → … → 18 → 19。",
        "侧边栏为 **2 级目录**：`01`–`04` 与 `18`–`22` 为一级项；`05`–`17` 归入 **开发实现** 分组（缩进子项）。章节 prev/next 线性导航仍为 03 → 04 → … → 18 → 19。",
    )
    readme.write_text(text, encoding="utf-8")


def update_sidebar_js() -> None:
    path = ROOT / "assets" / "sidebar.js"
    text = path.read_text(encoding="utf-8")
    text = text.replace("/^1[0-8]-/", "/^1[0-7]-/")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    print("=== Phase 1: rename files ===")
    rename_files()

    print("=== Phase 2: update HTML ===")
    for path in sorted(ROOT.glob("*.html")):
        update_html(path)
        print(f"  updated {path.name}")

    print("=== Phase 3: update scripts/assets ===")
    for path in sorted((ROOT / "scripts").glob("*.py")):
        if path.name == Path(__file__).name:
            continue
        update_other(path)
        print(f"  updated scripts/{path.name}")
    update_sidebar_js()
    update_readme()
    print("  updated README.md and sidebar.js")


if __name__ == "__main__":
    main()
