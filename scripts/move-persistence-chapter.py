# -*- coding: utf-8 -*-
"""Move chapter 14 数据库·事务 ->>11  持久化 (after IO·NIO·网络)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIDEBAR = """            <li><a href="index.html">目录首页</a></li>
            <li><a href="01-requirements-analysis.html">01 需求分析</a></li>
            <li><a href="02-prototype-design.html">02 原型设计</a></li>
            <li><a href="03-architecture-design.html">03 架构设计</a></li>
            <li><a href="04-project-scheduling.html">04 项目排期</a></li>
            <li class="sidebar-group"><span class="sidebar-group-label"><a href="java-development.html">开发实现</a></span></li>
            <li class="sidebar-subitem"><a href="05-dev-environment.html">05 开发环境搭建</a></li>
            <li class="sidebar-subitem"><a href="06-java-basics.html">06 Java基础语法</a></li>
            <li class="sidebar-subitem"><a href="07-oop.html">07 面向对象</a></li>
            <li class="sidebar-subitem"><a href="08-jvm.html">>08  JVM</a></li>
            <li class="sidebar-subitem"><a href="09-concurrency.html">>09  并发编程</a></li>
            <li class="sidebar-subitem"><a href="10-io-nio-network.html">>10  IO·NIO·网络</a></li>
            <li class="sidebar-subitem"><a href="11-persistence.html">>11  持久化</a></li>
            <li class="sidebar-subitem"><a href="12-spring-framework.html">>12  Spring Framework</a></li>
            <li class="sidebar-subitem"><a href="13-ruoyi-framework.html">>13  RuoYi 框架</a></li>
            <li class="sidebar-subitem"><a href="14-common-modules.html">>14  常见功能模块</a></li>
            <li class="sidebar-subitem"><a href="15-security-development.html">>15  安全开发</a></li>
            <li class="sidebar-subitem"><a href="16-test-driven-development.html">>16  测试驱动开发</a></li>
            <li><a href="17-testing-quality.html">>17  测试·质量</a></li>
            <li><a href="18-performance-tuning.html">>18  性能调优</a></li>
            <li><a href="19-devops-cloud-native.html">>19  工程化·DevOps</a></li>
            <li><a href="20-ai-development.html">>20  AI 辅助开发</a></li>
            <li><a href="21-business-intelligence.html">>21  业务智能化</a></li>
            <li><a href="glossary.html">术语字典</a></li>"""

CHAPTER_META = {
    "java-development.html": ("开发实现", "开发实现"),
    "03-architecture-design.html": ("03 架构设计", "03 架构设计"),
    "04-project-scheduling.html": ("04 项目排期 — 开发 · 测试 · 上线", "04 项目排期 — 开发 · 测试 · 上线"),
    "05-dev-environment.html": ("05 开发环境搭建 — Cursor · IDEA · VS Code", "05 开发环境搭建 — Cursor · IDEA · VS Code"),
    "06-java-basics.html": ("06 Java基础语法", "06 Java基础语法"),
    "07-oop.html": ("07 面向对象", "07 面向对象"),
    "08-jvm.html": ("09 JVM", "09 JVM"),
    "09-concurrency.html": ("10 并发编程", "10 并发编程"),
    "10-io-nio-network.html": ("11 IO·NIO·网络", "11 IO·NIO·网络"),
    "11-persistence.html": ("12 持久化", "12 持久化"),
    "12-spring-framework.html": ("13 Spring Framework", "13 Spring Framework"),
    "13-ruoyi-framework.html": ("14 RuoYi 框架", "14 RuoYi 框架"),
    "14-common-modules.html": ("15 常见功能模块", "15 常见功能模块"),
    "15-security-development.html": ("16 安全开发", "16 安全开发"),
    "16-test-driven-development.html": ("17 测试驱动开发", "17 测试驱动开发"),
    "17-testing-quality.html": ("18 测试·质量", "18 测试·质量"),
    "18-performance-tuning.html": ("19 性能调优", "19 性能调优"),
    "19-devops-cloud-native.html": ("20 工程化·DevOps", "20 工程化·DevOps"),
    "20-ai-development.html": ("21 AI 辅助开发", "21 AI 辅助开发"),
    "21-business-intelligence.html": ("22 业务智能化", "22 业务智能化与 LLM 能力需求"),
}

NAV_BLOCK = {
    "01-requirements-analysis.html": (
        '<a href="index.html">← 返回目录</a>\n        <a href="02-prototype-design.html">下一章：原型设计 →</a>',
    ),
    "02-prototype-design.html": (
        '<a href="01-requirements-analysis.html">← 上一章：需求分析</a>\n        <a href="03-architecture-design.html">下一章：架构设计 →</a>',
    ),
    "03-architecture-design.html": (
        '<a href="02-prototype-design.html">← 上一章：原型设计</a>\n        <a href="04-project-scheduling.html">下一章：项目排期 →</a>',
    ),
    "java-development.html": (
        '<a href="04-project-scheduling.html">← 上一章：项目排期</a>\n        <a href="05-dev-environment.html">下一章：开发环境搭建 →</a>',
    ),
    "04-project-scheduling.html": (
        '<a href="03-architecture-design.html">← 上一章：架构设计</a>\n        <a href="05-dev-environment.html">下一章：开发环境搭建 →</a>',
    ),
    "05-dev-environment.html": (
        '<a href="04-project-scheduling.html">← 上一章：项目排期</a>\n        <a href="06-java-basics.html">下一章：Java基础语法 →</a>',
    ),
    "06-java-basics.html": (
        '<a href="05-dev-environment.html">← 上一章：开发环境搭建</a>\n        <a href="07-oop.html">下一章：面向对象 →</a>',
    ),
    "07-oop.html": (
        '<a href="06-java-basics.html">← 上一章：Java基础语法</a>\n        <a href="08-jvm.html">下一章：JVM →</a>',
    ),
    "08-jvm.html": (
        '<a href="07-oop.html">← 上一章：面向对象</a>\n        <a href="09-concurrency.html">下一章：并发编程 →</a>',
    ),
    "09-concurrency.html": (
        '<a href="08-jvm.html">← 上一章：JVM</a>\n        <a href="10-io-nio-network.html">下一章：IO·NIO·网络 →</a>',
    ),
    "10-io-nio-network.html": (
        '<a href="09-concurrency.html">← 上一章：并发编程</a>\n        <a href="11-persistence.html">下一章：持久化 →</a>',
    ),
    "11-persistence.html": (
        '<a href="10-io-nio-network.html">← 上一章：IO·NIO·网络</a>\n        <a href="12-spring-framework.html">下一章：Spring Framework →</a>',
    ),
    "12-spring-framework.html": (
        '<a href="11-persistence.html">← 上一章：持久化</a>\n        <a href="13-ruoyi-framework.html">下一章：RuoYi 框架 →</a>',
    ),
    "13-ruoyi-framework.html": (
        '<a href="12-spring-framework.html">← 上一章：Spring Framework</a>\n        <a href="14-common-modules.html">下一章：常见功能模块 →</a>',
    ),
    "14-common-modules.html": (
        '<a href="13-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n        <a href="15-security-development.html">下一章：安全开发 →</a>',
    ),
    "15-security-development.html": (
        '<a href="14-common-modules.html">← 上一章：常见功能模块</a>\n        <a href="16-test-driven-development.html">下一章：测试驱动开发 →</a>',
    ),
    "16-test-driven-development.html": (
        '<a href="15-security-development.html">← 上一章：安全开发</a>\n        <a href="17-testing-quality.html">下一章：测试·质量 →</a>',
    ),
    "17-testing-quality.html": (
        '<a href="16-test-driven-development.html">← 上一章：测试驱动开发</a>\n        <a href="18-performance-tuning.html">下一章：性能调优 →</a>',
    ),
    "18-performance-tuning.html": (
        '<a href="17-testing-quality.html">← 上一章：测试·质量</a>\n        <a href="19-devops-cloud-native.html">下一章：工程化·DevOps →</a>',
    ),
    "19-devops-cloud-native.html": (
        '<a href="18-performance-tuning.html">← 上一章：性能调优</a>\n        <a href="20-ai-development.html">下一章：AI 辅助开发 →</a>',
    ),
    "20-ai-development.html": (
        '<a href="19-devops-cloud-native.html">← 上一章：工程化·DevOps</a>\n        <a href="21-business-intelligence.html">下一章：业务智能化 →</a>',
    ),
    "21-business-intelligence.html": (
        '<a href="20-ai-development.html">← 上一章：AI 辅助开发</a>\n        <a href="glossary.html">下一章：术语字典 →</a>',
    ),
}


def rename_files() -> None:
    moves = [
        ("11-spring-framework.html", "__tmp_12-spring-framework.html"),
        ("12-ruoyi-framework.html", "__tmp_13-ruoyi-framework.html"),
        ("13-database-sql-transaction.html", "__tmp_11-persistence.html"),
    ]
    finals = [
        ("__tmp_11-persistence.html", "11-persistence.html"),
        ("__tmp_12-spring-framework.html", "12-spring-framework.html"),
        ("__tmp_13-ruoyi-framework.html", "13-ruoyi-framework.html"),
    ]
    for src, dst in moves:
        (ROOT / src).rename(ROOT / dst)
    for src, dst in finals:
        (ROOT / src).rename(ROOT / dst)


def placeholder_paths(text: str) -> str:
    text = text.replace("11-spring-framework.html", "__HREF_SPRING__")
    text = text.replace("12-ruoyi-framework.html", "__HREF_RUOYI__")
    text = text.replace("13-database-sql-transaction.html", "__HREF_PERSIST__")
    text = text.replace("__HREF_PERSIST__", "11-persistence.html")
    text = text.replace("__HREF_SPRING__", "12-spring-framework.html")
    text = text.replace("__HREF_RUOYI__", "13-ruoyi-framework.html")
    return text


def placeholder_chapter_nums(text: str) -> str:
    for old in ("14", "13", "12"):
        text = text.replace(f"第 {old} 章", f"__CHN{old}__")
        text = text.replace(f"第{old}章", f"__CHN{old}__")
    mapping = {"14": "12", "13": "14", "12": "13"}
    for old, new in mapping.items():
        text = text.replace(f"__CHN{old}__", f"第 {new} 章")
    return text


def apply_text_fixes(text: str) -> str:
    fixes = [
        ("数据库·事务", "持久化"),
        ("12 Spring Framework", "13 Spring Framework"),
        ("13 RuoYi 框架", "14 RuoYi 框架"),
        ("14 数据库·事务", "12 持久化"),
        ("14 持久化", "12 持久化"),
        ("13 持久化", "12 持久化"),
        ('P2["环境与语言<br/>05–11"]', 'P2["环境与语言<br/>05–11"]'),
        ('P3["应用开发<br/>12–16"]', 'P3["应用开发<br/>13–16"]'),
        ("交叉引用第 12 章 Spring Framework、第 11 章数据库", "交叉引用第 12 章 Spring Framework、第 11 章持久化"),
        ("第 11 章数据库", "第 11 章持久化"),
        ("第 11 章数据库事务", "第 11 章持久化"),
    ]
    for old, new in fixes:
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
    inner = NAV_BLOCK[path.name][0]
    return re.sub(
        r'<nav class="chapter-nav">.*?</nav>',
        f'<nav class="chapter-nav">\n        {inner}\n      </nav>',
        text,
        count=1,
        flags=re.DOTALL,
    )


def fix_index_cards(text: str) -> str:
    persist_card = """          <a class="index-chapter-card" href="11-persistence.html">
            <span class="index-chapter-num">11</span>
            <span class="index-chapter-title">持久化</span>
            <span class="index-chapter-desc">SQL 优化、索引、事务与连接池</span>
          </a>"""
    spring_card = """          <a class="index-chapter-card" href="12-spring-framework.html">
            <span class="index-chapter-num">12</span>
            <span class="index-chapter-title">Spring Framework</span>
            <span class="index-chapter-desc">IoC、AOP、MVC、事务与分层实践</span>
          </a>"""
    ruoyi_card = """          <a class="index-chapter-card" href="13-ruoyi-framework.html">
            <span class="index-chapter-num">13</span>
            <span class="index-chapter-title">RuoYi 框架</span>
            <span class="index-chapter-desc">企业后台脚手架、权限与代码生成</span>
          </a>"""
    old_persist = re.search(
        r'          <a class="index-chapter-card" href="11-persistence\.html">.*?</a>',
        text,
        flags=re.DOTALL,
    )
    if old_persist and 'id="phase-foundation"' in text[: old_persist.start()]:
        return text
    old_block = re.search(
        r'          <a class="index-chapter-card" href="10-io-nio-network\.html">.*?</a>\n        </div>\n      </section>\n\n      <section class="index-phase" id="phase-application">',
        text,
        flags=re.DOTALL,
    )
    if old_block:
        replacement = (
            '          <a class="index-chapter-card" href="10-io-nio-network.html">\n'
            '            <span class="index-chapter-num">10</span>\n'
            '            <span class="index-chapter-title">IO·NIO·网络</span>\n'
            '            <span class="index-chapter-desc">文件 IO、NIO 与 HTTP 客户端</span>\n'
            "          </a>\n"
            + persist_card
            + "\n        </div>\n      </section>\n\n      <section class=\"index-phase\" id=\"phase-application\">"
        )
        text = text[: old_block.start()] + replacement + text[old_block.end() :]

    for old_card in [
        re.compile(
            r'          <a class="index-chapter-card" href="11-spring-framework\.html">.*?</a>\n',
            re.DOTALL,
        ),
        re.compile(
            r'          <a class="index-chapter-card" href="12-ruoyi-framework\.html">.*?</a>\n',
            re.DOTALL,
        ),
        re.compile(
            r'          <a class="index-chapter-card" href="11-persistence\.html">.*?</a>\n',
            re.DOTALL,
        ),
    ]:
        text = old_card.sub("", text, count=1)

    app_grid = re.search(
        r'(<section class="index-phase" id="phase-application">.*?<div class="index-chapter-grid">)\n',
        text,
        flags=re.DOTALL,
    )
    if app_grid:
        insert_at = app_grid.end()
        text = text[:insert_at] + spring_card + "\n" + ruoyi_card + "\n" + text[insert_at:]
    return text


def fix_java_development_cards(text: str) -> str:
    persist = """        <article class="toc-card">
          <h2><a href="11-persistence.html">>11  持久化</a></h2>
          <p>SQL 优化、索引、事务与连接池。</p>
        </article>"""
    spring = """        <article class="toc-card">
          <h2><a href="12-spring-framework.html">>12  Spring Framework</a></h2>
          <p>Spring Framework 6 应用开发：IoC/DI、AOP、MVC、数据访问、事务、配置、事件、校验与分层实践。</p>
        </article>"""
    ruoyi = """        <article class="toc-card">
          <h2><a href="13-ruoyi-framework.html">>13  RuoYi 框架</a></h2>
          <p>企业后台脚手架简明介绍：管理后台、权限系统、代码生成、官方文档与生产注意点。</p>
        </article>"""

    old = re.search(
        r'        <article class="toc-card">\n          <h2><a href="10-io-nio-network\.html">.*?</article>\n',
        text,
        flags=re.DOTALL,
    )
    if old:
        text = text[: old.end()] + persist + "\n" + text[old.end() :]

    for pattern in [
        r'        <article class="toc-card">\n          <h2><a href="11-spring-framework\.html">.*?</article>\n',
        r'        <article class="toc-card">\n          <h2><a href="12-ruoyi-framework\.html">.*?</article>\n',
        r'        <article class="toc-card">\n          <h2><a href="11-persistence\.html">.*?</article>\n',
    ]:
        text = re.sub(pattern, "", text, count=1, flags=re.DOTALL)

    marker = '        <article class="toc-card">\n          <h2><a href="14-common-modules.html">'
    if marker in text and spring not in text:
        text = text.replace(marker, spring + "\n" + ruoyi + "\n" + marker, 1)
    return text


def update_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = placeholder_paths(text)
    text = placeholder_chapter_nums(text)
    text = apply_text_fixes(text)
    if path.suffix == ".html":
        if path.name == "index.html":
            text = replace_sidebar(text)
            text = fix_index_cards(text)
        elif path.name == "java-development.html":
            text = replace_sidebar(text)
            text = fix_titles(path, text)
            text = fix_java_development_cards(text)
            text = fix_nav(path, text)
        elif path.name != "glossary.html":
            text = replace_sidebar(text)
            text = fix_titles(path, text)
            text = fix_nav(path, text)
        elif path.name == "glossary.html":
            text = replace_sidebar(text)
    path.write_text(text, encoding="utf-8")


def rewrite_update_refs() -> None:
    content = (ROOT / "scripts" / "update-refs.py").read_text(encoding="utf-8")
    content = re.sub(
        r'SIDEBAR = """.*?"""',
        f'SIDEBAR = """{SIDEBAR}"""',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"CHAPTER_META = \{.*?\n\}",
        "CHAPTER_META = " + repr(CHAPTER_META, ensure_ascii=False),
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"NAV_BLOCK = \{.*?\n\}",
        "NAV_BLOCK = " + repr(NAV_BLOCK, ensure_ascii=False),
        content,
        count=1,
        flags=re.DOTALL,
    )
    (ROOT / "scripts" / "update-refs.py").write_text(content, encoding="utf-8")


def main() -> None:
    print("=== Phase 1: rename files ===")
    rename_files()
    for name in ("11-persistence.html", "12-spring-framework.html", "13-ruoyi-framework.html"):
        print(f"  -> {name}")

    print("=== Phase 2: update HTML & scripts ===")
    targets = sorted(ROOT.glob("*.html")) + sorted((ROOT / "scripts").glob("*.py"))
    for path in targets:
        if path.name == "move-persistence-chapter.py":
            continue
        update_file(path)
        print(f"  updated {path.name}")

    rewrite_update_refs()
    print("  updated scripts/update-refs.py")


if __name__ == "__main__":
    main()
