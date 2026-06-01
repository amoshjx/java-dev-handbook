# -*- coding: utf-8 -*-
"""Renumber chapters 06-22 -> 04-20 after merging old 04/05 into 03."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\amos\java-dev-handbook")

# old_num -> (new_num, slug)
RENAMES = {
    6: (4, "project-scheduling"),
    7: (5, "dev-environment"),
    8: (6, "java-basics"),
    9: (7, "oop"),
    10: (8, "collections-generics-stream"),
    11: (9, "jvm"),
    12: (10, "concurrency"),
    13: (11, "io-nio-network"),
    14: (12, "spring-framework"),
    15: (13, "database-sql-transaction"),
    16: (14, "common-modules"),
    17: (15, "security-development"),
    18: (16, "test-driven-development"),
    19: (17, "testing-quality"),
    20: (18, "performance-tuning"),
    21: (19, "devops-cloud-native"),
    22: (20, "ai-development"),
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
            <li class="sidebar-subitem"><a href="08-jvm.html">>08  JVM</a></li>
            <li class="sidebar-subitem"><a href="09-concurrency.html">>09  并发编程</a></li>
            <li class="sidebar-subitem"><a href="10-io-nio-network.html">>10  IO·NIO·网络</a></li>
            <li class="sidebar-subitem"><a href="12-spring-framework.html">>12  Spring Framework</a></li>
            <li class="sidebar-subitem"><a href="13-ruoyi-framework.html">>13  RuoYi 框架</a></li>
            <li class="sidebar-subitem"><a href="11-persistence.html">>11  持久化</a></li>
            <li class="sidebar-subitem"><a href="14-common-modules.html">>14  常见功能模块</a></li>
            <li class="sidebar-subitem"><a href="16-security-development.html">>15  安全开发</a></li>
            <li class="sidebar-subitem"><a href="17-test-driven-development.html">>16  测试驱动开发</a></li>
            <li><a href="18-testing-quality.html">>17  测试·质量</a></li>
            <li><a href="19-performance-tuning.html">>18  性能调优</a></li>
            <li><a href="20-devops-cloud-native.html">>19  工程化·DevOps</a></li>
            <li><a href="21-ai-development.html">>20  AI 辅助开发</a></li>
            <li><a href="22-business-intelligence.html">>21  业务智能化</a></li>
            <li><a href="glossary.html">术语字典</a></li>"""

CHAPTER_META = {
    "03-architecture-design.html": ("03 架构设计", "03 架构设计"),
    "04-project-scheduling.html": ("04 项目排期 — 开发 · 测试 · 上线", "04 项目排期 — 开发 · 测试 · 上线"),
    "05-dev-environment.html": ("05 开发环境搭建 — Cursor · IDEA · VS Code", "05 开发环境搭建 — Cursor · IDEA · VS Code"),
    "06-java-basics.html": ("06 Java基础语法", "06 Java基础语法"),
    "07-oop.html": ("07 面向对象", "07 面向对象"),
    "08-jvm.html": ("09 JVM", "09 JVM"),
    "09-concurrency.html": ("10 并发编程", "10 并发编程"),
    "10-io-nio-network.html": ("11 IO·NIO·网络", "11 IO·NIO·网络"),
    "12-spring-framework.html": ("13 Spring Framework", "13 Spring Framework"),
    "11-persistence.html": ("12 持久化", "12 持久化"),
    "14-common-modules.html": ("14 常见功能模块", "14 常见功能模块"),
    "16-security-development.html": ("15 安全开发", "15 安全开发"),
    "17-test-driven-development.html": ("16 测试驱动开发", "16 测试驱动开发"),
    "18-testing-quality.html": ("17 测试·质量", "17 测试·质量"),
    "19-performance-tuning.html": ("18 性能调优", "18 性能调优"),
    "20-devops-cloud-native.html": ("19 工程化·DevOps", "19 工程化·DevOps"),
    "21-ai-development.html": ("20 AI 辅助开发", "20 AI 辅助开发"),
    "22-business-intelligence.html": ("21 业务智能化", "21 业务智能化与 LLM 能力需求"),
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
        '<a href="10-io-nio-network.html">← 上一章：IO·NIO·网络</a>\n        <a href="11-persistence.html">下一章：持久化 →</a>',
    ),
    "11-persistence.html": (
        '<a href="12-spring-framework.html">← 上一章：Spring Framework</a>\n        <a href="14-common-modules.html">下一章：常见功能模块 →</a>',
    ),
    "14-common-modules.html": (
        '<a href="11-persistence.html">← 上一章：持久化</a>\n        <a href="16-security-development.html">下一章：安全开发 →</a>',
    ),
    "16-security-development.html": (
        '<a href="14-common-modules.html">← 上一章：常见功能模块</a>\n        <a href="17-test-driven-development.html">下一章：测试驱动开发 →</a>',
    ),
    "17-test-driven-development.html": (
        '<a href="16-security-development.html">← 上一章：安全开发</a>\n        <a href="18-testing-quality.html">下一章：测试·质量 →</a>',
    ),
    "18-testing-quality.html": (
        '<a href="17-test-driven-development.html">← 上一章：测试驱动开发</a>\n        <a href="19-performance-tuning.html">下一章：性能调优 →</a>',
    ),
    "19-performance-tuning.html": (
        '<a href="18-testing-quality.html">← 上一章：测试·质量</a>\n        <a href="20-devops-cloud-native.html">下一章：工程化·DevOps →</a>',
    ),
    "20-devops-cloud-native.html": (
        '<a href="19-performance-tuning.html">← 上一章：性能调优</a>\n        <a href="21-ai-development.html">下一章：AI 辅助开发 →</a>',
    ),
    "21-ai-development.html": (
        '<a href="20-devops-cloud-native.html">← 上一章：工程化·DevOps</a>\n        <a href="22-business-intelligence.html">下一章：业务智能化 →</a>',
    ),
    "22-business-intelligence.html": (
        '<a href="21-ai-development.html">← 上一章：AI 辅助开发</a>\n        <a href="glossary.html">下一章：术语字典 →</a>',
    ),
}

TEXT_FIXES = [
    ("架构设计与决策（含原04/05）", "架构设计"),
    ("架构设计与决策（含原 04/05）", "架构设计"),
    ("架构设计与决策", "架构设计"),
    ("架构与决策", "架构设计"),
    ("01–05", "01–03"),
    ("01-05", "01-03"),
    ("技术选型（01–05）", "技术选型（01–03）"),
    ("08-13", "06-11"),
    ("14-16", "11-14"),
    ("19-19", "16-16"),
    ("21-21", "19-19"),
    ("17–20", "16–19"),
    ("18-20", "17-19"),
    ("01–23", "01–20"),
    ("01-23", "01-20"),
    ("共 23 章", "共 20 章"),
    ("22 章", "20 章"),
    ("共 24 项", "共 22 项"),
    ("C06[06 项目排期]", "C04[04 项目排期]"),
    ("C07[07 开发环境]", "C05[05 开发环境]"),
    ("C08 --> LANG[语言与运行时 08-13]", "C06 --> LANG[语言与运行时 06-11]"),
    ("C14 --> BACK[框架与业务 14-16]", "C11 --> BACK[框架与业务 11-14]"),
    ("C18 --> SEC[安全 17]", "C16 --> SEC[安全 15]"),
    ("C19 --> TEST[测试与质量 19-19]", "C17 --> TEST[测试与质量 16-16]"),
    ("C21 --> OPS[性能/交付 21-21]", "C19 --> OPS[性能/交付 19-19]"),
    ("C22 --> AIDEV[开发者 AI 22]", "C21 --> AIDEV[开发者 AI 20]"),
    ("IDX --> C03[03 架构设计与决策]", "IDX --> C03[03 架构设计]"),
    ("ARCH[架构/选型 03]", "ARCH[架构设计 03]"),
    ("SCHED[排期 06]", "SCHED[排期 04]"),
    ("DEV[开发环境 07]", "DEV[开发环境 05]"),
    ("→ 架构设计与决策（含技术选型）→", "→ 架构设计（含技术选型）→"),
]


def rename_files() -> list[tuple[str, str]]:
    mapping: list[tuple[str, str]] = []
    temp_paths: list[tuple[Path, Path]] = []

    for old_num, (new_num, slug) in RENAMES.items():
        old_name = f"{old_num:02d}-{slug}.html"
        temp_name = f"__renum_{new_num:02d}-{slug}.html"
        old_path = ROOT / old_name
        if not old_path.exists():
            raise FileNotFoundError(f"Missing chapter file: {old_name}")
        temp_path = ROOT / temp_name
        old_path.rename(temp_path)
        temp_paths.append((temp_path, ROOT / f"{new_num:02d}-{slug}.html"))
        mapping.append((old_name, f"{new_num:02d}-{slug}.html"))

    for temp_path, final_path in temp_paths:
        temp_path.rename(final_path)

    return mapping


def placeholder_paths(text: str) -> str:
    for old_num in sorted(RENAMES, reverse=True):
        text = text.replace(f"{old_num:02d}-", f"__CH{old_num:02}__")
    for old_num, (new_num, _slug) in RENAMES.items():
        text = text.replace(f"__CH{old_num:02}__", f"{new_num:02d}-")
    return text


def placeholder_chapter_nums(text: str) -> str:
    for old_num in sorted(RENAMES, reverse=True):
        old = f"{old_num:02d}"
        new = f"{RENAMES[old_num][0]:02d}"
        text = text.replace(f"第 {old} 章", f"__CHN{old}__")
        text = text.replace(f"第{old}章", f"__CHN{old}__")
        text = re.sub(rf"\bC{old}\b", f"__CN{old}__", text)
        text = re.sub(rf"\bCH{old}\b", f"__CHX{old}__", text)
    for old_num, (new_num, _slug) in RENAMES.items():
        old = f"{old_num:02d}"
        new = f"{new_num:02d}"
        text = text.replace(f"__CHN{old}__", f"第 {new} 章")
        text = text.replace(f"__CN{old}__", f"C{new}")
        text = text.replace(f"__CHX{old}__", f"CH{new}")
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
    text = re.sub(
        r"<title>.*?</title>",
        f"<title>{title} — Java项目手册</title>",
        text,
        count=1,
    )
    text = re.sub(
        r"<h1>.*?</h1>",
        f"<h1>{h1}</h1>",
        text,
        count=1,
    )
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


def apply_text_fixes(text: str) -> str:
    for old, new in TEXT_FIXES:
        text = text.replace(old, new)
    return text


def update_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = placeholder_paths(text)
    text = placeholder_chapter_nums(text)
    text = apply_text_fixes(text)
    if path.suffix == ".html" and path.name != "glossary.html":
        text = replace_sidebar(text)
        text = fix_titles(path, text)
        text = fix_nav(path, text)
    path.write_text(text, encoding="utf-8")


def rewrite_helper_scripts() -> None:
    nav_entries = [
        ('"01-requirements-analysis.html"', "None", '"02-prototype-design.html"', '"下一章：原型设计 →"'),
        ('"02-prototype-design.html"', '"01-requirements-analysis.html"', '"03-architecture-design.html"', '"下一章：架构设计 →"'),
        ('"03-architecture-design.html"', '"02-prototype-design.html"', '"04-project-scheduling.html"', '"下一章：项目排期 →"'),
        ('"04-project-scheduling.html"', '"03-architecture-design.html"', '"05-dev-environment.html"', '"下一章：开发环境搭建 →"'),
        ('"05-dev-environment.html"', '"04-project-scheduling.html"', '"06-java-basics.html"', '"下一章：Java基础语法 →"'),
        ('"06-java-basics.html"', '"05-dev-environment.html"', '"07-oop.html"', '"下一章：面向对象 →"'),
        ('"07-oop.html"', '"06-java-basics.html"', '"08-jvm.html"', '"下一章：JVM →"'),
        ('"08-jvm.html"', '"07-oop.html"', '"09-concurrency.html"', '"下一章：并发编程 →"'),
        ('"09-concurrency.html"', '"08-jvm.html"', '"10-io-nio-network.html"', '"下一章：IO·NIO·网络 →"'),
        ('"10-io-nio-network.html"', '"09-concurrency.html"', '"12-spring-framework.html"', '"下一章：Spring Framework →"'),
        ('"12-spring-framework.html"', '"10-io-nio-network.html"', '"11-persistence.html"', '"下一章：持久化 →"'),
        ('"11-persistence.html"', '"12-spring-framework.html"', '"14-common-modules.html"', '"下一章：常见功能模块 →"'),
        ('"14-common-modules.html"', '"11-persistence.html"', '"16-security-development.html"', '"下一章：安全开发 →"'),
        ('"16-security-development.html"', '"14-common-modules.html"', '"17-test-driven-development.html"', '"下一章：测试驱动开发 →"'),
        ('"17-test-driven-development.html"', '"16-security-development.html"', '"18-testing-quality.html"', '"下一章：测试·质量 →"'),
        ('"18-testing-quality.html"', '"17-test-driven-development.html"', '"19-performance-tuning.html"', '"下一章：性能调优 →"'),
        ('"19-performance-tuning.html"', '"18-testing-quality.html"', '"20-devops-cloud-native.html"', '"下一章：工程化·DevOps →"'),
        ('"20-devops-cloud-native.html"', '"19-performance-tuning.html"', '"21-ai-development.html"', '"下一章：AI 辅助开发 →"'),
        ('"21-ai-development.html"', '"20-devops-cloud-native.html"', "None", '"返回目录 →"'),
    ]
    nav_lines = "\n".join(
        f"    ({a}, {b}, {c}, {d})," for a, b, c, d in nav_entries
    )
    prev_labels = {
        "02-prototype-design.html": "← 上一章：需求分析",
        "03-architecture-design.html": "← 上一章：原型设计",
        "04-project-scheduling.html": "← 上一章：架构设计",
        "05-dev-environment.html": "← 上一章：项目排期",
        "06-java-basics.html": "← 上一章：开发环境搭建",
        "07-oop.html": "← 上一章：Java基础语法",
        "08-jvm.html": "← 上一章：面向对象",
        "09-concurrency.html": "← 上一章：JVM",
        "10-io-nio-network.html": "← 上一章：并发编程",
        "12-spring-framework.html": "← 上一章：IO·NIO·网络",
        "11-persistence.html": "← 上一章：Spring Framework",
        "14-common-modules.html": "← 上一章：持久化",
        "16-security-development.html": "← 上一章：常见功能模块",
        "17-test-driven-development.html": "← 上一章：安全开发",
        "18-testing-quality.html": "← 上一章：测试驱动开发",
        "19-performance-tuning.html": "← 上一章：测试·质量",
        "20-devops-cloud-native.html": "← 上一章：性能调优",
        "21-ai-development.html": "← 上一章：工程化",
    }
    update_refs = f'''# -*- coding: utf-8 -*-
"""Sync sidebar, titles, and chapter nav across HTML files."""
import re
from pathlib import Path

ROOT = Path(r"C:\\Users\\amos\\java-dev-handbook")

SIDEBAR = """{SIDEBAR}"""

CHAPTER_META = {repr(CHAPTER_META, ensure_ascii=False)}

NAV = [
{nav_lines}
]

PREV_LABELS = {repr(prev_labels, ensure_ascii=False)}


def replace_sidebar(text: str) -> str:
    return re.sub(
        r'(?s)<li><a href="index\\.html">目录首页</a></li>.*?</ul>',
        SIDEBAR + "\\n          </ul>",
        text,
        count=1,
    )


def fix_titles(path: Path, text: str) -> str:
    meta = CHAPTER_META.get(path.name)
    if not meta:
        return text
    title, h1 = meta
    text = re.sub(r"<title>.*?</title>", f"<title>{{title}} — Java项目手册</title>", text, count=1)
    text = re.sub(r"<h1>.*?</h1>", f"<h1>{{h1}}</h1>", text, count=1)
    return text


def fix_nav(path: Path, text: str) -> str:
    block = None
    for fname, prev, nxt, nxt_label in NAV:
        if fname == path.name:
            if prev is None:
                block = f'<a href="index.html">← 返回目录</a>\\n        <a href="{{nxt}}">{{nxt_label}}</a>'
            elif nxt is None:
                block = f'<a href="{{prev}}">{{PREV_LABELS[fname]}}</a>\\n        <a href="index.html">{{nxt_label}}</a>'
            else:
                block = f'<a href="{{prev}}">{{PREV_LABELS[fname]}}</a>\\n        <a href="{{nxt}}">{{nxt_label}}</a>'
            break
    if not block:
        return text
    return re.sub(
        r'<nav class="chapter-nav">.*?</nav>',
        f'<nav class="chapter-nav">\\n        {{block}}\\n      </nav>',
        text,
        count=1,
        flags=re.DOTALL,
    )


def main():
    for path in sorted(ROOT.glob("*.html")):
        if path.name in ("index.html", "glossary.html"):
            continue
        text = path.read_text(encoding="utf-8")
        text = replace_sidebar(text)
        text = fix_titles(path, text)
        text = fix_nav(path, text)
        path.write_text(text, encoding="utf-8")
        print(f"updated {{path.name}}")


if __name__ == "__main__":
    main()
'''
    fix_paths = f'''# -*- coding: utf-8 -*-
"""Rebuild chapter nav blocks after renumbering."""
import re
from pathlib import Path

ROOT = Path(r"C:\\Users\\amos\\java-dev-handbook")

NAV_BLOCK = {repr(NAV_BLOCK, ensure_ascii=False)}


def fix_nav(path: Path, text: str) -> str:
    if path.name not in NAV_BLOCK:
        return text
    inner = NAV_BLOCK[path.name][0]
    return re.sub(
        r'<nav class="chapter-nav">.*?</nav>',
        f'<nav class="chapter-nav">\\n        {{inner}}\\n      </nav>',
        text,
        count=1,
        flags=re.DOTALL,
    )


def main():
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        text = fix_nav(path, text)
        path.write_text(text, encoding="utf-8")
        print(f"fixed {{path.name}}")


if __name__ == "__main__":
    main()
'''
    (ROOT / "scripts" / "update-refs.py").write_text(update_refs, encoding="utf-8")
    (ROOT / "scripts" / "fix-paths.py").write_text(fix_paths, encoding="utf-8")


def update_readme() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("22 章", "20 章")
    text = text.replace("`22-ai-development.html`", "`21-ai-development.html`")
    text = text.replace("~ `22-ai-development.html`", "~ `21-ai-development.html`")
    readme.write_text(text, encoding="utf-8")


def main() -> None:
    print("=== Phase 1: rename files ===")
    mapping = rename_files()
    for old, new in mapping:
        print(f"  {old} -> {new}")

    print("=== Phase 2: update HTML ===")
    for path in sorted(ROOT.glob("*.html")):
        update_file(path)
        print(f"  updated {path.name}")

    print("=== Phase 3: update scripts & README ===")
    for path in sorted((ROOT / "scripts").glob("*")):
        if path.name == "renumber-chapters.py":
            continue
        update_file(path)
        print(f"  updated scripts/{path.name}")
    update_readme()
    rewrite_helper_scripts()
    print("  updated README.md and helper scripts")


if __name__ == "__main__":
    main()
