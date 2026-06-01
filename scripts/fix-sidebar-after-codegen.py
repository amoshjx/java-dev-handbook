# -*- coding: utf-8 -*-
"""Fix sidebar labels and insert chapter 15 after codegen insert."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL_FIXES = [
    ('16-common-modules.html">15 ', '16-common-modules.html">16 '),
    ('17-security-development.html">16 ', '17-security-development.html">17 '),
    ('18-test-driven-development.html">17 ', '18-test-driven-development.html">18 '),
    ('19-testing-quality.html">18 ', '19-testing-quality.html">19 '),
    ('20-performance-tuning.html">19 ', '20-performance-tuning.html">20 '),
    ('21-devops-cloud-native.html">20 ', '21-devops-cloud-native.html">21 '),
    ('22-ai-development.html">21 ', '22-ai-development.html">22 '),
    ('23-business-intelligence.html">22 ', '23-business-intelligence.html">23 '),
]

SIDEBAR_INSERT = (
    '            <li class="sidebar-subitem"><a href="14-ruoyi-framework.html">14 RuoYi 框架</a></li>\n'
    '            <li class="sidebar-subitem"><a href="16-common-modules.html">16 常见功能模块</a></li>'
)
SIDEBAR_WITH_NEW = (
    '            <li class="sidebar-subitem"><a href="14-ruoyi-framework.html">14 RuoYi 框架</a></li>\n'
    '            <li class="sidebar-subitem"><a href="15-project-code-generator.html">15 项目代码生成器</a></li>\n'
    '            <li class="sidebar-subitem"><a href="16-common-modules.html">16 常见功能模块</a></li>'
)

TOC_CARD_FIXES = [
    ('href="16-common-modules.html">15 常见功能模块', 'href="16-common-modules.html">16 常见功能模块'),
    ('href="17-security-development.html">16 安全开发', 'href="17-security-development.html">17 安全开发'),
    ('href="18-test-driven-development.html">17 测试驱动开发', 'href="18-test-driven-development.html">18 测试驱动开发'),
]

INDEX_CARD_FIXES = [
    ('index-chapter-num">15</span>\n            <span class="index-chapter-title">常见功能模块',
     'index-chapter-num">16</span>\n            <span class="index-chapter-title">常见功能模块'),
    ('index-chapter-num">16</span>\n            <span class="index-chapter-title">安全开发',
     'index-chapter-num">17</span>\n            <span class="index-chapter-title">安全开发'),
    ('index-chapter-num">17</span>\n            <span class="index-chapter-title">测试驱动开发',
     'index-chapter-num">18</span>\n            <span class="index-chapter-title">测试驱动开发'),
    ('index-chapter-num">18</span>\n            <span class="index-chapter-title">测试·质量',
     'index-chapter-num">19</span>\n            <span class="index-chapter-title">测试·质量'),
    ('index-chapter-num">19</span>\n            <span class="index-chapter-title">性能调优',
     'index-chapter-num">20</span>\n            <span class="index-chapter-title">性能调优'),
    ('index-chapter-num">20</span>\n            <span class="index-chapter-title">工程化',
     'index-chapter-num">21</span>\n            <span class="index-chapter-title">工程化'),
    ('index-chapter-num">21</span>\n            <span class="index-chapter-title">AI 辅助开发',
     'index-chapter-num">22</span>\n            <span class="index-chapter-title">AI 辅助开发'),
    ('index-chapter-num">22</span>\n            <span class="index-chapter-title">业务智能化',
     'index-chapter-num">23</span>\n            <span class="index-chapter-title">业务智能化'),
]


def main() -> None:
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in LABEL_FIXES:
            text = text.replace(old, new)
        if SIDEBAR_INSERT in text and "15-project-code-generator.html" not in text:
            text = text.replace(SIDEBAR_INSERT, SIDEBAR_WITH_NEW)
        for old, new in TOC_CARD_FIXES:
            text = text.replace(old, new)
        if path.name == "index.html":
            for old, new in INDEX_CARD_FIXES:
                text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
