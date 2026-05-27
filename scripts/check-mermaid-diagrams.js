#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const CJK = /[\u4e00-\u9fff\u3400-\u4dbf]/;

function listHtmlFiles(dir) {
  return fs.readdirSync(dir).filter(function (f) {
    return f.endsWith('.html');
  });
}

function extractMermaidBlocks(html) {
  const blocks = [];
  const re = /<pre class="mermaid">([\s\S]*?)<\/pre>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    blocks.push({
      index: blocks.length + 1,
      content: m[1].replace(/^\s+|\s+$/g, ''),
      start: m.index
    });
  }
  return blocks;
}

function checkBlock(content, file, index) {
  const issues = [];
  const lines = content.split('\n');
  const first = (lines[0] || '').trim();
  const type = first.split(/\s+/)[0];

  lines.forEach(function (line, lineNo) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('%%')) return;

    // subgraph without quoted/bracket label
    const subgraphMatch = trimmed.match(/^subgraph\s+(.+)$/);
    if (subgraphMatch) {
      const rest = subgraphMatch[1].trim();
      if (!/^["']/.test(rest) && !/\[/.test(rest)) {
        issues.push({
          line: lineNo + 1,
          type: 'subgraph-unquoted',
          text: trimmed,
          hint: 'subgraph 中文/空格标签应改为 subgraph ID["标签"]'
        });
      }
    }

    // stateDiagram transition labels with CJK, unquoted
    if (/stateDiagram/i.test(first)) {
      const trans = trimmed.match(/^([A-Za-z* \[\]]+)\s*-->\s*([A-Za-z* \[\]]+)\s*:\s*(.+)$/);
      if (trans) {
        const label = trans[3].trim();
        if (CJK.test(label) && !/^["']/.test(label)) {
          issues.push({
            line: lineNo + 1,
            type: 'state-transition-unquoted',
            text: trimmed,
            hint: '状态迁移中文标签应加双引号'
          });
        }
      }
    }

    // gantt title/section/task with CJK
    if (/^gantt\b/i.test(first)) {
      if (/^title\s+/.test(trimmed) && CJK.test(trimmed) && !/^title\s+["']/.test(trimmed)) {
        issues.push({
          line: lineNo + 1,
          type: 'gantt-title-unquoted',
          text: trimmed,
          hint: 'gantt title 含中文应加双引号'
        });
      }
      if (/^section\s+/.test(trimmed) && CJK.test(trimmed) && !/^section\s+["']/.test(trimmed)) {
        issues.push({
          line: lineNo + 1,
          type: 'gantt-section-unquoted',
          text: trimmed,
          hint: 'gantt section 含中文应加双引号'
        });
      }
      const taskMatch = trimmed.match(/^([^:]+):/);
      if (
        taskMatch &&
        !/^section\b/.test(trimmed) &&
        !/^title\b/.test(trimmed) &&
        !/^dateFormat\b/.test(trimmed) &&
        !/^axisFormat\b/.test(trimmed) &&
        CJK.test(taskMatch[1]) &&
        !/^["']/.test(taskMatch[1].trim())
      ) {
        issues.push({
          line: lineNo + 1,
          type: 'gantt-task-unquoted',
          text: trimmed,
          hint: 'gantt 任务名含中文应加双引号'
        });
      }
    }

    // quadrantChart axis/quadrant without quotes (heuristic)
    if (/^quadrantChart\b/i.test(first)) {
      if (/^(x-axis|y-axis|quadrant-\d+)\s+/.test(trimmed) && CJK.test(trimmed)) {
        const parts = trimmed.split(/\s+/);
        const kw = parts[0];
        const val = trimmed.slice(kw.length).trim();
        if (CJK.test(val) && !/^["']/.test(val) && !val.includes('-->')) {
          // x-axis "a" --> "b" is OK; bare labels need quotes
        }
        if (/^(quadrant-\d+)\s+/.test(trimmed)) {
          const qLabel = trimmed.replace(/^quadrant-\d+\s+/, '').trim();
          if (CJK.test(qLabel) && !/^["']/.test(qLabel)) {
            issues.push({
              line: lineNo + 1,
              type: 'quadrant-label-unquoted',
              text: trimmed,
              hint: 'quadrant 标签应加双引号'
            });
          }
        }
      }
    }
  });

  return { file, index, type, issues };
}

function main() {
  const files = listHtmlFiles(ROOT);
  const inventory = [];
  const allIssues = [];
  let totalBlocks = 0;

  files.forEach(function (file) {
    const full = path.join(ROOT, file);
    const html = fs.readFileSync(full, 'utf8');
    const blocks = extractMermaidBlocks(html);
    if (!blocks.length) return;
    inventory.push({ file, count: blocks.length });
    totalBlocks += blocks.length;
    blocks.forEach(function (b) {
      const result = checkBlock(b.content, file, b.index);
      if (result.issues.length) {
        allIssues.push(result);
      }
    });
  });

  console.log('=== Mermaid diagram inventory ===');
  inventory.sort(function (a, b) {
    return b.count - a.count || a.file.localeCompare(b.file);
  });
  inventory.forEach(function (row) {
    console.log('  ' + row.file + ': ' + row.count);
  });
  console.log('Total files: ' + inventory.length + ', total diagrams: ' + totalBlocks);
  console.log('');

  if (!allIssues.length) {
    console.log('OK: no heuristic syntax issues found.');
    process.exit(0);
  }

  console.log('=== Potential Mermaid syntax issues ===');
  allIssues.forEach(function (r) {
    console.log('\n' + r.file + ' #' + r.index + ' (' + r.type + ')');
    r.issues.forEach(function (i) {
      console.log('  L' + i.line + ' [' + i.type + '] ' + i.text);
      console.log('       → ' + i.hint);
    });
  });
  const count = allIssues.reduce(function (n, r) {
    return n + r.issues.length;
  }, 0);
  console.log('\nFound ' + count + ' issue(s) in ' + allIssues.length + ' diagram(s).');
  process.exit(1);
}

main();
