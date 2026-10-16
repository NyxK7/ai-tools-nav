# 🧭 AI 工具导航（ai-tools-nav）

[![Daily update](https://github.com/NyxK7/ai-tools-nav/actions/workflows/daily-update.yml/badge.svg)](https://github.com/NyxK7/ai-tools-nav/actions/workflows/daily-update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

面向中文用户的 AI 工具导航站：**按业务场景**整理真实可用的 AI 工具，附 GitHub Star 开源排行榜与每日新品快报。纯静态、无框架、无外部 CDN，每天由 GitHub Actions 自动更新。

- 🌐 GitHub Pages：<https://nyxk7.github.io/ai-tools-nav/>
- ▲ Vercel（含邮件订阅接口）：<https://ai-tools-nav-seven-pearl.vercel.app/>

## ✨ 功能

- **9 大业务场景**：写作、编程/Vibe coding、图像设计、视频、音频、游戏开发、智能体/自动化、办公效率、客服营销
- **可用性标注**：每个工具标注「国内服务」「开源，可本地部署」或「境外服务，国内可能无法直接使用」，国内服务优先展示
- **热门排行榜**：依据开源工具的 GitHub Star 数，每日刷新
- **每日新品快报**：自动抓取 GitHub 新建 AI 仓库与 Hacker News Show HN 热帖
- **SEO / AI 友好**：预渲染 HTML、JSON-LD 结构化数据、`sitemap.xml`、`llms.txt`、`tools.md`
- **邮件周刊订阅**：Vercel Serverless 函数 + Resend 联系人，带格式校验、蜜罐与频率限制，支持自助退订
- 关于 / 免责声明 / 隐私政策页面

## ⚙️ 每日自动更新原理

`.github/workflows/daily-update.yml` 每天北京时间 08:00 运行（也可手动触发）：

1. `scripts/update.py`：刷新 GitHub Star，抓取近 7 天新建的 `topic:ai` 仓库和近 48 小时 Show HN 帖子；Star ≥ 200 且关键词唯一匹配某场景的仓库会自动收录并标记「新收录」（14 天）
2. `scripts/linkcheck.py --prune-auto`：检查链接，只自动移除失效的「自动收录」条目
3. `scripts/build.py`：重新生成全部页面
4. 有变化时自动提交推送，GitHub Pages 与 Vercel 随之重新部署

## 📁 项目结构

```
data/tools.json        # 唯一数据源：场景、工具、排行榜、每日快报
scripts/seed.py        # 初始数据
scripts/update.py      # 每日抓取与自动收录
scripts/linkcheck.py   # 链接检查
scripts/build.py       # 生成 index.html、s/*.html、关于/免责/隐私页、sitemap、llms.txt、tools.md
api/subscribe.js       # Vercel 函数：订阅（写入 Resend 联系人分组）
api/unsubscribe.js     # Vercel 函数：退订（删除联系人）
app.js / style.css     # 搜索过滤与表单提交（渐进增强）、样式
.github/               # 每日更新工作流、Issue 模板
```

> `index.html`、`s/`、`sitemap.xml` 等为生成文件，请修改 `data/tools.json` 或 `scripts/build.py`，不要直接改 HTML。

## 🛠 本地运行

只需 Python 3.10+，无第三方依赖：

```bash
git clone https://github.com/NyxK7/ai-tools-nav.git && cd ai-tools-nav
python3 scripts/build.py          # 生成页面
python3 -m http.server 8000       # 打开 http://localhost:8000
# 可选：
python3 scripts/linkcheck.py      # 检查链接
GH_TOKEN=xxx python3 scripts/update.py   # 抓取更新（令牌可选，用于提高 GitHub API 限额）
```

订阅接口部署在 Vercel，需要环境变量 `RESEND_API_KEY`（加密）和 `RESEND_SEGMENT_ID`，请勿将密钥提交到仓库。

## 🤝 参与贡献

- **推荐工具 / 报告失效 / 建议**：[提交 Issue](https://github.com/NyxK7/ai-tools-nav/issues/new/choose)
- **直接提交 PR**：在 `data/tools.json` 对应场景中添加条目，详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📊 数据来源

- 工具信息：人工整理，来自各工具官网
- Star 数与新仓库：[GitHub REST API](https://docs.github.com/rest)
- Show HN：[Hacker News Algolia API](https://hn.algolia.com/api)

## ⚠️ 免责声明

本项目仅作信息整理，不构成推荐或背书；工具功能、价格与可用性以官网为准。标注「境外服务」的工具仅作客观介绍，本项目不提供任何访问境外服务的方法，请遵守所在地法律法规。自动抓取内容未经人工审核。详见[免责声明](https://nyxk7.github.io/ai-tools-nav/disclaimer.html)。

## 📄 许可证

[MIT](LICENSE) © 2026 Niank Wang (NyxK7)。第三方工具名称与商标归各自所有者。
