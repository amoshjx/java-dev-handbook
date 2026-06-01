# -*- coding: utf-8 -*-
"""Insert chapter 15 project code generator; renumber old 15-22 -> 16-23."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RENAMES = {
    22: (23, "business-intelligence"),
    21: (22, "ai-development"),
    20: (21, "devops-cloud-native"),
    19: (20, "performance-tuning"),
    18: (19, "testing-quality"),
    17: (18, "test-driven-development"),
    16: (17, "security-development"),
    15: (16, "common-modules"),
}

SIDEBAR_INSERT = (
    '            <li class="sidebar-subitem"><a href="14-ruoyi-framework.html">14 RuoYi 框架</a></li>\n'
    '            <li class="sidebar-subitem"><a href="16-common-modules.html">16 常见功能模块</a></li>'
)
SIDEBAR_WITH_NEW = (
    '            <li class="sidebar-subitem"><a href="14-ruoyi-framework.html">14 RuoYi 框架</a></li>\n'
    '            <li class="sidebar-subitem"><a href="15-project-code-generator.html">15 项目代码生成器</a></li>\n'
    '            <li class="sidebar-subitem"><a href="16-common-modules.html">16 常见功能模块</a></li>'
)


def rename_files() -> list[tuple[str, str]]:
    mapping: list[tuple[str, str]] = []
    temp_paths: list[tuple[Path, Path]] = []

    for old_num in sorted(RENAMES, reverse=True):
        new_num, slug = RENAMES[old_num]
        old_name = f"{old_num:02d}-{slug}.html"
        temp_name = f"__ins_{new_num:02d}-{slug}.html"
        old_path = ROOT / old_name
        if not old_path.exists():
            raise FileNotFoundError(f"Missing: {old_name}")
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
        text = text.replace(f"第 {old} 章", f"__CHN{old}__")
        text = text.replace(f"第{old}章", f"__CHN{old}__")
        text = re.sub(rf"\bC{old}\b", f"__CN{old}__", text)
    for old_num, (new_num, _slug) in RENAMES.items():
        old = f"{old_num:02d}"
        new = f"{new_num:02d}"
        text = text.replace(f"__CHN{old}__", f"第 {new} 章")
        text = text.replace(f"__CN{old}__", f"C{new}")
    return text


def apply_range_fixes(text: str) -> str:
    fixes = [
        ("05–17", "05–18"),
        ("05-17", "05-18"),
        ("03 → 04 → … → 17 → 18", "03 → 04 → … → 18 → 19"),
        ("05 → … → 17 → 18", "05 → … → 18 → 19"),
        ("图：开发实现章组阅读顺序（05 → 17 → 18）", "图：开发实现章组阅读顺序（05 → 18 → 19）"),
        ("测试与质量（第 18 章）", "测试与质量（第 19 章）"),
        ("第 18 章）之前", "第 19 章）之前"),
        ("共 22 章", "共 23 章"),
        ("01–22", "01–23"),
        ("01-22", "01-23"),
        ("17 → 18", "18 → 19"),
        ("… → 17 → 18", "… → 18 → 19"),
        ("16 → 17", "17 → 18"),
        ("17-20 章", "18-21 章"),
        ("第 17–20 章", "第 18–21 章"),
        ("第 16–19 章", "第 17–20 章"),
        ("第 21 章聚焦", "第 22 章聚焦"),
        ("第 20 章聚焦", "第 21 章聚焦"),
        (
            "`05-dev-environment.html` ~ `17-test-driven-development.html`：开发实现子章（二级，编号 05–17",
            "`05-dev-environment.html` ~ `18-test-driven-development.html`：开发实现子章（二级，编号 05–18",
        ),
        (
            "`17-test-driven-development.html`：开发实现子章",
            "`18-test-driven-development.html`：开发实现子章",
        ),
        (
            "`17-testing-quality.html` ~ `21-business-intelligence.html`",
            "`19-testing-quality.html` ~ `23-business-intelligence.html`",
        ),
        (
            "C14 --> BACK[15-16 业务与安全]",
            "C14 --> C15[15 代码生成]\n    C15 --> BACK[16-17 业务与安全]",
        ),
        (
            "环境 → 语言与运行时 → Spring → 构建部署 → RuoYi → 业务模块 → 安全 → TDD",
            "环境 → 语言与运行时 → Spring → 构建部署 → RuoYi → 代码生成器 → 业务模块 → 安全 → TDD",
        ),
        (
            'C13 --> C14["14 RuoYi"]\n    C14 --> BACK["15-16 业务与安全"]',
            'C13 --> C14["14 RuoYi"]\n    C14 --> C15["15 代码生成器"]\n    C15 --> BACK["16-17 业务与安全"]',
        ),
        (
            '<a href="15-common-modules.html">下一章：常见功能模块 →</a>',
            '<a href="15-project-code-generator.html">下一章：项目代码生成器 →</a>',
        ),
        (
            '<a href="14-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n        <a href="16-common-modules.html">下一章：常见功能模块 →</a>',
            '<a href="14-ruoyi-framework.html">← 上一章：RuoYi 框架</a>\n        <a href="15-project-code-generator.html">下一章：项目代码生成器 →</a>',
        ),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def insert_sidebar_line(text: str) -> str:
    if "15-project-code-generator.html" in text:
        return text
    if SIDEBAR_INSERT in text:
        return text.replace(SIDEBAR_INSERT, SIDEBAR_WITH_NEW)
    return text


def update_all_files() -> None:
    skip = {"insert-codegen-chapter.py", "insert-ruoyi-chapter.py"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in (".html", ".md", ".py", ".js"):
            continue
        if path.name in skip:
            continue
        text = path.read_text(encoding="utf-8")
        new_text = placeholder_paths(text)
        new_text = placeholder_chapter_nums(new_text)
        new_text = apply_range_fixes(new_text)
        new_text = insert_sidebar_line(new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"  updated {path.relative_to(ROOT)}")


def main() -> None:
    print("=== Phase 1: rename 15-22 -> 16-23 ===")
    mapping = rename_files()
    for old, new in mapping:
        print(f"  {old} -> {new}")

    print("=== Phase 2: update references ===")
    update_all_files()
    print("Done. Add 15-project-code-generator.html if not present.")


if __name__ == "__main__":
    main()
