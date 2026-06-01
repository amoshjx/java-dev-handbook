# -*- coding: utf-8 -*-
"""Sync sidebar, titles, and chapter nav across HTML files."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\amos\java-dev-handbook")

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

GLOSSARY_SIDEBAR = SIDEBAR

CHAPTER_META = {
    "java-development.html": ("开发实现", "开发实现"),
    "03-architecture-design.html": ("03 架构设计", "03 架构设计"),
    "04-project-scheduling.html": ("04 项目排期 — 开发 · 测试 · 上线", "04 项目排期 — 开发 · 测试 · 上线"),
    "05-dev-environment.html": ("05 开发环境搭建 — Cursor · IDEA · VS Code", "05 开发环境搭建 — Cursor · IDEA · VS Code"),
    "06-java-basics.html": ("06 Java基础语法", "06 Java基础语法"),
    "07-oop.html": ("07 面向对象", "07 面向对象"),
    "08-jvm.html": ("08 JVM", "08 JVM"),
    "09-concurrency.html": ("09 并发编程", "09 并发编程"),
    "10-io-nio-network.html": ("10 IO·NIO·网络", "10 IO·NIO·网络"),
    "11-persistence.html": ("11 持久化", "11 持久化"),
    "12-spring-framework.html": ("12 Spring Framework", "12 Spring Framework"),
    "13-build-packaging-deploy.html": ("13 项目构建、打包与部署", "13 项目构建、打包与部署"),
    "14-ruoyi-framework.html": ("14 RuoYi 框架", "14 RuoYi 框架"),
    "16-common-modules.html": ("15 常见功能模块", "15 常见功能模块"),
    "17-security-development.html": ("16 安全开发", "16 安全开发"),
    "18-test-driven-development.html": ("17 测试驱动开发", "17 测试驱动开发"),
    "19-testing-quality.html": ("18 测试·质量", "18 测试·质量"),
    "20-performance-tuning.html": ("19 性能调优", "19 性能调优"),
    "21-devops-cloud-native.html": ("20 工程化·DevOps", "20 工程化·DevOps"),
    "22-ai-development.html": ("21 AI 辅助开发", "21 AI 辅助开发"),
    "23-business-intelligence.html": ("22 业务智能化", "22 业务智能化与 LLM 能力需求"),
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
        '<a href="11-persistence.html">← 上一章：持久化</a>\n        <a href="13-build-packaging-deploy.html">下一章：项目构建、打包与部署 →</a>',
    ),
    "13-build-packaging-deploy.html": (
        '<a href="12-spring-framework.html">← 上一章：Spring Framework</a>\n        <a href="14-ruoyi-framework.html">下一章：RuoYi 框架 →</a>',
    ),
    "14-ruoyi-framework.html": (
        '<a href="13-build-packaging-deploy.html">← 上一章：项目构建、打包与部署</a>\n        <a href="16-common-modules.html">下一章：常见功能模块 →</a>',
    ),
    "16-common-modules.html": (
        '<a href="14-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n        <a href="17-security-development.html">下一章：安全开发 →</a>',
    ),
    "17-security-development.html": (
        '<a href="16-common-modules.html">← 上一章：常见功能模块</a>\n        <a href="18-test-driven-development.html">下一章：测试驱动开发 →</a>',
    ),
    "18-test-driven-development.html": (
        '<a href="17-security-development.html">← 上一章：安全开发</a>\n        <a href="19-testing-quality.html">下一章：测试·质量 →</a>',
    ),
    "19-testing-quality.html": (
        '<a href="18-test-driven-development.html">← 上一章：测试驱动开发</a>\n        <a href="20-performance-tuning.html">下一章：性能调优 →</a>',
    ),
    "20-performance-tuning.html": (
        '<a href="19-testing-quality.html">← 上一章：测试·质量</a>\n        <a href="21-devops-cloud-native.html">下一章：工程化·DevOps →</a>',
    ),
    "21-devops-cloud-native.html": (
        '<a href="20-performance-tuning.html">← 上一章：性能调优</a>\n        <a href="22-ai-development.html">下一章：AI 辅助开发 →</a>',
    ),
    "22-ai-development.html": (
        '<a href="21-devops-cloud-native.html">← 上一章：工程化·DevOps</a>\n        <a href="23-business-intelligence.html">下一章：业务智能化 →</a>',
    ),
    "23-business-intelligence.html": (
        '<a href="22-ai-development.html">← 上一章：AI 辅助开发</a>\n        <a href="glossary.html">下一章：术语字典 →</a>',
    ),
}


def replace_sidebar(text: str, *, glossary: bool = False) -> str:
    sidebar = GLOSSARY_SIDEBAR if glossary else SIDEBAR
    return re.sub(
        r'(?s)<li><a href="index\.html">目录首页</a></li>.*?</ul>',
        sidebar + "\n          </ul>",
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


def main():
    for path in sorted(ROOT.glob("*.html")):
        if path.name == "index.html":
            continue
        text = path.read_text(encoding="utf-8")
        text = replace_sidebar(text, glossary=path.name == "glossary.html")
        text = fix_titles(path, text)
        text = fix_nav(path, text)
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.name}")


if __name__ == "__main__":
    main()
