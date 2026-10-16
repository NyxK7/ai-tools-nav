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

   `avail` 取值：`cn` 国内服务、`oss` 开源可本地部署、`intl` 境外服务（国内可能无法直接使用）。开源项目可加 `"github": "owner/repo"` 以参与 Star 排行。

3. 本地运行 `python3 scripts/build.py` 和 `python3 scripts/linkcheck.py`，确认生成正常、链接有效
4. 提交 PR，说明收录理由

## 收录原则

- 只收录真实存在、官网可访问的工具；介绍保持客观中立，不使用「最好」「第一」等绝对化用语
- 优先收录面向中国大陆用户提供服务的产品；境外服务须标注 `intl`
- 不收录任何翻墙/代理/规避网络监管的工具或教程，不收录违法违规内容
- 请勿直接修改生成的 HTML 文件，也不要提交任何密钥或个人信息

## 代码贡献

脚本均为无依赖的 Python 3 标准库代码，前端为原生 JS/CSS。提交前请保证 `scripts/build.py` 可正常运行。

提交贡献即表示你同意以 [MIT 许可证](LICENSE) 授权你的贡献。
