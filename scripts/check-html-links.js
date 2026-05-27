#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const rootDir = path.resolve(__dirname, "..");

function listHtmlFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];

  for (const entry of entries) {
    if (entry.name.startsWith(".")) {
      continue;
    }
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...listHtmlFiles(fullPath));
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith(".html")) {
      results.push(fullPath);
    }
  }

  return results;
}

function parseIds(htmlContent) {
  const ids = new Set();
  const idRegex = /\sid\s*=\s*["']([^"']+)["']/gi;
  let match;
  while ((match = idRegex.exec(htmlContent)) !== null) {
    ids.add(match[1]);
  }
  return ids;
}

function parseLinks(htmlContent) {
  const links = [];
  const hrefRegex = /\shref\s*=\s*["']([^"']+)["']/gi;
  let match;
  while ((match = hrefRegex.exec(htmlContent)) !== null) {
    links.push(match[1].trim());
  }
  return links;
}

function isExternalLink(href) {
  return (
    href.startsWith("http://") ||
    href.startsWith("https://") ||
    href.startsWith("mailto:") ||
    href.startsWith("tel:") ||
    href.startsWith("javascript:")
  );
}

function normalizePathname(rawHref) {
  const noQuery = rawHref.split("?")[0];
  return noQuery;
}

const htmlFiles = listHtmlFiles(rootDir);
const htmlFileSet = new Set(htmlFiles.map((p) => path.resolve(p)));
const idMap = new Map();

for (const filePath of htmlFiles) {
  const content = fs.readFileSync(filePath, "utf8");
  idMap.set(filePath, parseIds(content));
}

const errors = [];
let totalLinks = 0;
let checkedLinks = 0;

for (const sourceFile of htmlFiles) {
  const sourceContent = fs.readFileSync(sourceFile, "utf8");
  const links = parseLinks(sourceContent);

  for (const href of links) {
    totalLinks += 1;

    if (!href || isExternalLink(href)) {
      continue;
    }

    const [targetRaw, hashRaw] = href.split("#");
    const targetPart = normalizePathname(targetRaw || "");
    const hashPart = hashRaw || "";

    if (targetPart === "") {
      if (hashPart) {
        checkedLinks += 1;
        const sourceIds = idMap.get(sourceFile) || new Set();
        if (!sourceIds.has(hashPart)) {
          errors.push({
            type: "MISSING_ANCHOR",
            sourceFile,
            href,
            detail: `锚点 #${hashPart} 不存在于当前页面`,
          });
        }
      }
      continue;
    }

    if (!targetPart.toLowerCase().endsWith(".html")) {
      continue;
    }

    checkedLinks += 1;
    const targetFile = path.resolve(path.dirname(sourceFile), targetPart);
    if (!htmlFileSet.has(targetFile)) {
      errors.push({
        type: "MISSING_FILE",
        sourceFile,
        href,
        detail: `目标文件不存在: ${path.relative(rootDir, targetFile)}`,
      });
      continue;
    }

    if (hashPart) {
      const targetIds = idMap.get(targetFile) || new Set();
      if (!targetIds.has(hashPart)) {
        errors.push({
          type: "MISSING_ANCHOR",
          sourceFile,
          href,
          detail: `锚点 #${hashPart} 不存在于 ${path.relative(rootDir, targetFile)}`,
        });
      }
    }
  }
}

if (errors.length > 0) {
  console.error("HTML 内链锚点校验失败：");
  for (const err of errors) {
    console.error(
      `- [${err.type}] ${path.relative(rootDir, err.sourceFile)} -> ${err.href}`
    );
    console.error(`  ${err.detail}`);
  }
}

console.log("校验统计：");
console.log(`- 扫描 HTML 文件: ${htmlFiles.length}`);
console.log(`- 发现 href 总数: ${totalLinks}`);
console.log(`- 实际校验内链数: ${checkedLinks}`);
console.log(`- 错误数: ${errors.length}`);

process.exit(errors.length > 0 ? 1 : 0);
