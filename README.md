# Java项目手册（更新版）

面向**高级 Java 开发者**的离线 HTML 多页速查站点：23 章，按软件工程生命周期编排。

## 章节结构

- `index.html`：按五阶段（规划→语言→应用→交付→AI）分组的章节目录入口
- `01-requirements-analysis.html` ~ `04-project-scheduling.html`：需求·原型·架构·项目排期（一级章）
- `java-development.html`：**开发实现** landing 页（一级分组入口；采用 Java 语言实现，默认 Java 21 LTS / Spring Framework 6.x / Spring Boot 3.x）
- `05-dev-environment.html` ~ `18-test-driven-development.html`：开发实现子章（二级，编号 05–18；含 `11-persistence.html`、`14-ruoyi-framework.html`、`15-project-code-generator.html`；`06-java-basics.html` 含集合/泛型/Stream 内容）
- `19-testing-quality.html` ~ `23-business-intelligence.html`：测试·性能·交付·AI（一级章）
- `glossary.html`：术语字典（统一口径）
- `assets/`：样式与前端脚本

侧边栏为 **2 级目录**：`01`–`04` 与 `19`–`23` 为一级项；`05`–`18` 归入 **开发实现** 分组（缩进子项）。章节 prev/next 线性导航仍为 03 → 04 → … → 18 → 19。

## 统一技术基线

默认基线（全书无特殊声明时统一适用）：

- Java：**Java 21 LTS**
- Spring：**Spring Framework 6.x** / **Spring Boot 3.x**（Jakarta EE 9+）
- 测试口径：JUnit 5 + Mockito 为默认单测组合，关键链路补集成测试
- 交付口径：CI/CD 流水线发布，默认采用蓝绿或金丝雀发布并具备回滚能力

## 如何打开

无需构建，双击 `index.html` 或在浏览器中打开本地路径即可（例如 `file:///C:/Users/amos/java-dev-handbook/index.html`）。

## GitHub 仓库

### 已配置内容

- `.gitignore`：忽略 `__pycache__/`、`node_modules/` 等
- `.github/workflows/ci.yml`：推送/PR 时校验 HTML 内链与 Mermaid 图表
- `.github/workflows/pages.yml`：推送 `main`/`master` 后自动部署 GitHub Pages

### 首次发布（本地执行）

1. **登录 GitHub CLI**（已安装 `gh`）：

```powershell
gh auth login
```

按提示选择 GitHub.com → HTTPS → 浏览器授权。

2. **提交并创建远程仓库**（当前分支为 `master`，可按需改为 `main`）：

```powershell
git commit -m "Initial commit: Java 开发手册静态站点"
gh repo create java-dev-handbook --public --source=. --remote=origin --push
```

若仓库已在 GitHub 上创建，只需添加远程并推送：

```powershell
git remote add origin https://github.com/<你的用户名>/java-dev-handbook.git
git push -u origin master
```

3. **启用 GitHub Pages**：

仓库 → **Settings** → **Pages** → **Build and deployment** → Source 选 **GitHub Actions**。

部署成功后访问：`https://<你的用户名>.github.io/java-dev-handbook/`

### 本地校验（与 CI 相同）

```bash
node scripts/check-html-links.js
node scripts/check-mermaid-diagrams.js
```

> 说明：当前内链校验存在若干已知锚点缺失（主要指向 `21-devops-cloud-native.html`），CI 可能暂时失败；修复后再推送即可通过。


仓库提供 `scripts/check-html-links.js`，用于扫描全站 HTML 内链并校验：

- 目标文件是否存在
- 带 hash 的锚点是否在目标页面存在对应 `id`
- 输出错误清单与统计，发现错误时返回非 0 退出码

使用方式：

```bash
node scripts/check-html-links.js
```

## 维护说明

- 新增章节时同步更新首页目录与侧边栏导航。
- 新增术语优先补充到 `glossary.html` 并使用稳定锚点。
- 修改内链后建议执行一次 `node scripts/check-html-links.js`。
- 批量重编号或插入章节时可参考 `scripts/insert-ruoyi-chapter.py` 与 `scripts/update-refs.py`。
