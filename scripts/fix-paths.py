# -*- coding: utf-8 -*-
"""Rebuild chapter nav blocks after renumbering."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\amos\java-dev-handbook")

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
        '<a href="09-concurrency.html">← 上一章：并发编程</a>\n        <a href="12-spring-framework.html">下一章：Spring Framework →</a>',
    ),
    "12-spring-framework.html": (
        '<a href="10-io-nio-network.html">← 上一章：IO·NIO·网络</a>\n        <a href="13-ruoyi-framework.html">下一章：RuoYi 框架 →</a>',
    ),
    "13-ruoyi-framework.html": (
        '<a href="12-spring-framework.html">← 上一章：Spring Framework</a>\n        <a href="11-persistence.html">下一章：持久化 →</a>',
    ),
    "11-persistence.html": (
        '<a href="13-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n        <a href="14-common-modules.html">下一章：常见功能模块 →</a>',
    ),
    "14-common-modules.html": (
        '<a href="11-persistence.html">← 上一章：持久化</a>\n        <a href="15-security-development.html">下一章：安全开发 →</a>',
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
        text = path.read_text(encoding="utf-8")
        text = fix_nav(path, text)
        path.write_text(text, encoding="utf-8")
        print(f"fixed {path.name}")


if __name__ == "__main__":
    main()
