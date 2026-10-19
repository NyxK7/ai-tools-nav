# 贡献指南

感谢你愿意让 AI 工具导航变得更好！

## 通过 Issue（最简单）

[新建 Issue](https://github.com/NyxK7/ai-tools-nav/issues/new/choose)，选择「反馈」模板，写明工具名称、官网链接、适用场景和一句话介绍。失效链接、信息错误也欢迎反馈。

## 通过 Pull Request 添加工具

1. Fork 本仓库并新建分支
2. 编辑 `data/tools.json`，在对应场景的 `tools` 数组中添加：

   ```json
   {
     "name": "工具名称",
     "url": "https://官网地址",
     "desc": "客观的一句话介绍（谁出品、能做什么）",
     "pricing": "免费 / 免费+付费 / 付费 / 开源免费",
     "avail": "cn"
   }
   ```

   `avail` 取值：`cn` 国内服务、`oss` 开源可本地部署、`intl` 境外服务（国内可能无法直接使用）。开源项目可加 `"github": "owner/repo"` 以获取 Star 数；官网不在独立域名时，热门排行榜按 Star 数排名。

3. 本地运行 `python3 scripts/build.py` 和 `python3 scripts/linkcheck.py`，确认生成正常、链接有效
4. 提交 PR，说明收录理由

## 在每日新品快报置顶官方发布

快报每天由程序自动抓取并整栏刷新。重要的官方发布（如新模型）可手动置顶：在 `data/tools.json` 的 `pinned_digest` 数组里加一条：

```json
{
  "source": "DeepSeek 官方",
  "title": "DeepSeek-V4.1-Flash-1017",
  "url": "https://官方发布页或模型页",
  "desc": "中文一句到两句介绍，只写官方公布的信息",
  "date": "2026-10-17"
}
```

`date` 为发布日期（YYYY-MM-DD），显示为「YYYY-MM-DD 发布」。从该日起 14 天内（与「新收录」标记相同）置顶在快报最前，之后自动不再显示，条目保留作记录。合并逻辑在 `scripts/digest.py`，`update.py` 与 `build.py` 都会调用，每日抓取不会冲掉置顶。改完运行 `python3 scripts/build.py` 即可生效。

## 收录原则

- 只收录真实存在、官网可访问的工具；介绍保持客观中立，不使用「最好」「第一」等绝对化用语
- 优先收录面向中国大陆用户提供服务的产品；境外服务须标注 `intl`
- 不收录任何翻墙/代理/规避网络监管的工具或教程，不收录违法违规内容
- 请勿直接修改生成的 HTML 文件，也不要提交任何密钥或个人信息

## 代码贡献

脚本均为无依赖的 Python 3 标准库代码，前端为原生 JS/CSS。提交前请保证 `scripts/build.py` 可正常运行。

提交贡献即表示你同意以 [MIT 许可证](LICENSE) 授权你的贡献。
