# -*- coding: utf-8 -*-
"""Insert chapter 13 RuoYi framework; renumber old 12-21 -> 13-22."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\amos\java-dev-handbook")

# old_num -> (new_num, slug) — process renames in reverse new_num order
RENAMES = {
    21: (22, "business-intelligence"),
    20: (21, "ai-development"),
    19: (20, "devops-cloud-native"),
    18: (19, "performance-tuning"),
    17: (18, "testing-quality"),
    16: (17, "test-driven-development"),
    15: (16, "security-development"),
    14: (15, "common-modules"),
    13: (14, "database-sql-transaction"),
}


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
        ("05–16", "05–17"),
        ("05-16", "05-17"),
        ("12-14 数据", "12-15 框架·数据·业务"),
        ("12-14 数据与业务", "12-15 框架·数据·业务"),
        ("12-14 数据业务", "12-15 框架·数据·业务"),
        ("BACK[12-14 数据业务]", "BACK[12-15 框架·数据·业务]"),
        ("BACK[12-14 数据与业务模块]", "BACK[12-15 框架·数据·业务]"),
        ("C15 --> C16[17 测试·质量]", "C16 --> C17[18 测试·质量]"),
        ("C16 --> OPS[17-19 性能/交付]", "C17 --> OPS[18-20 性能/交付]"),
        ("C19 --> C20[21 业务智能化]", "C20 --> C21[22 业务智能化]"),
        ("IDX --> C16[17 测试·质量]", "IDX --> C17[18 测试·质量]"),
        ("IDX --> C19[20 AI 辅助开发]", "IDX --> C20[21 AI 辅助开发]"),
        ("IDX --> C20[21 业务智能化]", "IDX --> C21[22 业务智能化]"),
        ("C16 --> OPS[17-19 性能/交付]", "C17 --> OPS[18-20 性能/交付]"),
        ("OPS --> C19 --> C20 --> GLOSS", "OPS --> C20 --> C21 --> GLOSS"),
        ("共 21 章", "共 22 章"),
        ("21 章 205", "22 章"),
        ("共 21 章、205", "共 22 章"),
        ("01–21", "01–22"),
        ("01-21", "01-22"),
        ("16 → 17", "17 → 18"),
        ("… → 16 → 17", "… → 17 → 18"),
        ("03 → 04 → … → 16 → 17", "03 → 04 → … → 17 → 18"),
        ("05 → 16 → 17", "05 → 17 → 18"),
        ("第 16 章）之前", "第 17 章）之前"),
        ("测试与质量（第 16 章）", "测试与质量（第 17 章）"),
        ("共 24 个 HTML", "共 25 个 HTML"),
        ("205 个知识点卡片", "知识点卡片"),
        ("第 20 章聚焦", "第 21 章聚焦"),
        ("第 19 章聚焦", "第 20 章聚焦"),
        ("16–19 章", "17–20 章"),
        ("第 16–19 章", "第 17–20 章"),
        ("见第 16–19 章", "见第 17–20 章"),
        ("第 15–16 章", "第 17–18 章"),
        ("21 章、205", "22 章"),
        ("~ `20-business-intelligence.html`", "~ `21-business-intelligence.html`"),
        ("`20-business-intelligence.html`", "`21-business-intelligence.html`"),
        ("16-testing-quality.html` ~ `20-business-intelligence.html`", "17-testing-quality.html` ~ `21-business-intelligence.html`"),
        ("`16-testing-quality.html` ~ `20-business-intelligence.html`", "`17-testing-quality.html` ~ `21-business-intelligence.html`"),
        ("`05-dev-environment.html` ~ `15-test-driven-development.html`", "`05-dev-environment.html` ~ `16-test-driven-development.html`"),
        ("编号 05–16 不变", "编号 05–17（含 13 RuoYi）"),
        ("05–16 子章", "05–17 子章"),
        ("开发实现 05-16", "开发实现 05-17"),
        ("DEV[开发实现 05-16]", "DEV[开发实现 05-17]"),
        ("C14 --> C15[16 TDD]", "C14 --> C15[16 安全]\n      C15 --> C16[17 TDD]"),
        ("C11 --> BACK[12-14 数据业务]", "C11 --> C12[13 RuoYi]\n      C12 --> BACK[13-15 数据业务]"),
        ("C11 --> BACK[12-15 框架·数据·业务]", "C11 --> C12[13 RuoYi]\n      C12 --> BACK[13-15 数据业务]"),
        ('LANG --> C11["12 Spring Framework"]\n    C11 --> BACK', 'LANG --> C11["12 Spring Framework"]\n    C11 --> C12[13 RuoYi]\n    C12 --> BACK'),
        ('C11["12 Spring Framework"]\n    C11 --> BACK[12-15', 'C11["12 Spring Framework"]\n      C11 --> C12[13 RuoYi]\n      C12 --> BACK[13-15'),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def update_all_files() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in (".html", ".md", ".py", ".js"):
            continue
        if path.name == "insert-ruoyi-chapter.py":
            continue
        text = path.read_text(encoding="utf-8")
        new_text = placeholder_paths(text)
        new_text = placeholder_chapter_nums(new_text)
        new_text = apply_range_fixes(new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"  updated {path.relative_to(ROOT)}")


def main() -> None:
    print("=== Phase 1: rename 12-21 -> 13-22 ===")
    mapping = rename_files()
    for old, new in mapping:
        print(f"  {old} -> {new}")

    print("=== Phase 2: update references ===")
    update_all_files()
    print("Done. Run update-refs.py after creating 13-ruoyi-framework.html")


if __name__ == "__main__":
    main()
