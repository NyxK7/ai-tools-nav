"""由 data/tools.json 生成静态 HTML（首页 + 场景页）、sitemap.xml、robots.txt、llms.txt、tools.md。"""
import json,html,os,datetime
B="https://nyxk7.github.io/ai-tools-nav"
API="https://ai-tools-nav-seven-pearl.vercel.app/api/subscribe"
d=json.load(open("data/tools.json")); E=lambda s:html.escape(str(s or ""),quote=True)
upd=d.get("updated") or ""; day=upd[:10] or datetime.date.today().isoformat()
FEED="https://github.com/NyxK7/ai-tools-nav/issues/new/choose"
AV={"cn":"国内服务","oss":"开源，可本地部署","intl":"境外服务，国内可能无法直接使用"}
def av(t): return t.get("avail") or ("oss" if t.get("github") else "intl")
def card(t,sc=None):
    g=t.get("signal") or {}
    sig=f"Tranco #{g['rank']:,}" if g.get("type")=="tranco" else ("暂无流行度数据" if not g else "")
    tags=[AV[av(t)],t["pricing"]]+([sc] if sc else [])+([f"★ {t['stars']:,}"] if t.get("stars") else [])+([sig] if sig else [])
    new='<span class="new">新收录</span>' if t.get("new") else ""
    return (f'<li class="card" data-k="{E((t["name"]+" "+t["desc"]).lower())}"><h3><a href="{E(t["url"])}" target="_blank" rel="noopener">{E(t["name"])}</a>{new}</h3>'
            f'<p>{E(t["desc"])}</p></li>')
def ld_list(name,tools):
    return {"@context":"https://schema.org","@type":"ItemList","name":name,"numberOfItems":len(tools),"itemListElement":[
      {"@type":"ListItem","position":i+1,"item":{"@type":"SoftwareApplication","name":t["name"],"url":t["url"],"description":t["desc"],
       "applicationCategory":"AI 工具","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"} if "免费" in t["pricing"] else None}} for i,t in enumerate(tools)]}
def clean(o):
    if isinstance(o,dict): return {k:clean(v) for k,v in o.items() if v is not None}
    if isinstance(o,list): return [clean(v) for v in o]
    return o
def page(path,title,desc,kw,body,ld,root):
    url=B+"/"+path.replace("index.html","")
    lds="".join(f'<script type="application/ld+json">{json.dumps(clean(x),ensure_ascii=False)}</script>' for x in ld)
    navs="".join(f'<a href="{root}s/{s["slug"]}.html">{E(s["name"])}</a>' for s in d["scenes"])
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="keywords" content="{E(kw)}">
<link rel="canonical" href="{url}"><meta name="robots" content="index,follow"><meta name="applicable-device" content="pc,mobile">
<meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:site_name" content="AI 工具导航">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#4f46e5"><link rel="icon" href="{root}favicon.svg">
<link rel="stylesheet" href="{root}style.css">{lds}</head><body>
<a class="skip" href="#main">跳到正文</a>
<header><p class="logo"><a href="{root}">🧭 AI 工具导航</a></p><h1>{E(title.split(" | ")[0])}</h1><p>{E(desc)}</p>
<nav aria-label="主导航"><a href="{root}#scenes">场景导航</a><a href="{root}#rank">热门排行榜</a><a href="{root}#daily">每日新品快报</a><a href="{root}#subscribe">邮件订阅</a><a href="{FEED}" target="_blank" rel="noopener">反馈建议</a><a href="{root}about.html">关于</a></nav>
<nav class="scn" aria-label="业务场景">{navs}</nav></header>
<main id="main">{body}</main>
<footer><p>数据更新时间：{E(upd)} · 每日自动更新 · <a href="{root}tools.md">纯文本工具清单</a> · <a href="{root}llms.txt">llms.txt</a> · <a href="https://github.com/NyxK7/ai-tools-nav">源码</a> · <a href="{FEED}" target="_blank" rel="noopener">反馈</a></p>
<p>工具介绍与价格以官网为准，本站不收取工具方费用。标注“境外服务”的工具仅作客观信息介绍，请遵守所在地法律法规使用。</p><p><a href="{root}about.html">关于本站</a> · <a href="{root}disclaimer.html">免责声明</a> · <a href="{root}privacy.html">隐私政策</a></p></footer><script src="{root}app.js" defer></script><script>if(/\\.vercel\\.app$/.test(location.hostname)){{var s=document.createElement("script");s.defer=1;s.src="/_vercel/insights/script.js";document.head.appendChild(s)}}</script></body></html>'''
alltools=[t for s in d["scenes"] for t in s["tools"]]
SUBT=f'''<section id="subscribe" aria-labelledby="h-sub"><h2 id="h-sub">邮件订阅</h2><p>每周一封：本周最值得试的 AI 新工具 + 场景选型建议。随时可退订。邮箱仅用于发送周刊，详见<a href="{{root}}privacy.html">隐私政策</a>。</p>
<form class="sub" id="subf" action="{API}" method="post"><label for="em" class="sr">邮箱地址</label><input id="em" name="email" type="email" placeholder="your@email.com" required maxlength="254" autocomplete="email"><input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" title="请勿填写"><label class="agree"><input type="checkbox" name="agree" required> 我已阅读并同意<a href="{{root}}privacy.html">隐私政策</a>（含数据由境外邮件服务商处理的说明）</label><button type="submit">订阅</button></form>
<p id="subm" role="status" aria-live="polite"></p>
<p>发现工具失效、想推荐工具或有建议？<a href="{FEED}" target="_blank" rel="noopener">在 GitHub Issues 反馈</a></p></section>'''
sub=lambda root:SUBT.replace("{root}",root)
# 首页
sc="".join(f'<section class="scene" id="{s["slug"]}" aria-labelledby="h-{s["slug"]}"><h3 id="h-{s["slug"]}"><a href="s/{s["slug"]}.html">{E(s["name"])}</a> <small>{len(s["tools"])} 个工具</small></h3><ul class="grid">{"".join(card(t) for t in s["tools"])}</ul></section>' for s in d["scenes"])
rk="".join(f'<li><a href="{E(t["url"])}" target="_blank" rel="noopener">{E(t["name"])}</a> <small>{E(t["scene"])}</small><span>★ {t["stars"]:,}</span></li>' for t in d["leaderboard"])
dl="".join(f'<li class="card"><h3><a href="{E(i["url"])}" target="_blank" rel="noopener nofollow">{E(i["title"])}</a></h3><p>{E(i["desc"])}</p><span class="tag">{E(i["source"])} · {E(i["metric"])}</span>'+(f' <a href="{E(i["hn"])}" target="_blank" rel="noopener nofollow">HN 讨论</a>' if i.get("hn") else "")+'</li>' for i in d["daily"])
body=f'''<div class="search"><label for="q" class="sr">搜索工具</label><input id="q" type="search" placeholder="搜索工具名称或用途，如：视频、写代码…"></div>
<section id="scenes" aria-labelledby="h-scenes"><h2 id="h-scenes">按业务场景导航</h2><p class="note">场景内排序依据公开流行度信号：优先按 Tranco 网站流行度排名（数值越小越热门，数据日期 {E((d.get("ranking") or {}).get("date",""))}）；官网不在独立域名、无法单独统计的工具排在其后，有开源仓库的按 GitHub Star 排序，其余标注“暂无流行度数据”。排序不代表质量评价。<a href="about.html#rank-method">详细说明</a></p>{sc}<p id="none" hidden>没有找到匹配的工具</p></section>
<section id="rank" aria-labelledby="h-rank"><h2 id="h-rank">热门排行榜</h2><p class="note">排名依据：开源工具在 GitHub 上的实时 Star 数（每日通过 GitHub API 更新）。闭源工具没有公开可比数据，暂不参与排名。</p><ol class="rank">{rk}</ol></section>
<section id="daily" aria-labelledby="h-daily"><h2 id="h-daily">每日新品快报 <small>{E(day)}</small></h2><p class="note">来源：GitHub 近 7 天新建、带 ai 主题的仓库（按 Star 排序）与 Hacker News 近 48 小时 AI 相关 Show HN 热帖。程序自动抓取，未经人工审核。</p><ul class="grid">{dl or "<li>今日暂无</li>"}</ul></section>{sub("")}'''
site={"@context":"https://schema.org","@type":"WebSite","name":"AI 工具导航","url":B+"/","inLanguage":"zh-CN"}
open("index.html","w").write(page("index.html","AI 工具导航 | 按业务场景选 AI 工具 · 热门 AI 排行榜 · 每日新品",
 f"中文 AI 工具导航：写作、编程/Vibe coding、图像、视频、音频、游戏开发、智能体等 {len(d['scenes'])} 大场景 {len(alltools)} 款 AI 工具推荐，GitHub Star 热门排行榜，每日自动追踪新发布的热门 AI 项目。",
 "AI工具,AI工具导航,AI工具排行榜,AI智能体,Vibe coding,AI编程工具,AI绘画,AI视频生成,AI写作,最新AI工具",body,[site,ld_list("AI 工具导航",alltools)],""))
os.makedirs("s",exist_ok=True)
for s in d["scenes"]:
    names="、".join(t["name"] for t in s["tools"][:5])
    b=f'<section aria-labelledby="h-s"><h2 id="h-s">{E(s["name"])} 场景推荐 AI 工具（{len(s["tools"])} 个）</h2><p class="note">场景内排序依据公开流行度信号：优先按 Tranco 网站流行度排名（数值越小越热门，数据日期 {E((d.get("ranking") or {}).get("date",""))}）；官网不在独立域名、无法单独统计的工具排在其后，有开源仓库的按 GitHub Star 排序，其余标注“暂无流行度数据”。排序不代表质量评价。<a href="../about.html#rank-method">详细说明</a></p><ul class="grid">{"".join(card(t) for t in s["tools"])}</ul></section>{sub("../")}'
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"AI 工具导航","item":B+"/"},{"@type":"ListItem","position":2,"name":s["name"],"item":f"{B}/s/{s['slug']}.html"}]}
    open(f"s/{s['slug']}.html","w").write(page(f"s/{s['slug']}.html",f"{s['name']} AI 工具推荐 | AI 工具导航",
      f"{s['name']}场景常用 AI 工具推荐：{names} 等，附中文介绍、官网链接与收费方式，每日更新。",
      f"{s['name']}AI工具,{s['name']}AI,AI工具推荐,AI工具导航",b,[bc,ld_list(s["name"]+" AI 工具",s["tools"])],"../"))
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+
 "".join(f"<url><loc>{u}</loc><lastmod>{day}</lastmod><changefreq>daily</changefreq></url>" for u in [B+"/"]+[f"{B}/s/{s['slug']}.html" for s in d["scenes"]]+[B+"/about.html",B+"/disclaimer.html",B+"/privacy.html",B+"/tools.md",B+"/llms.txt"])+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {B}/sitemap.xml\n")
md=[f"# AI 工具导航 · 全部工具清单\n\n> 中文 AI 工具导航，按业务场景推荐 AI 工具。数据更新：{upd}。网站：{B}/\n"]
for s in d["scenes"]:
    md.append(f"\n## {s['name']}\n")
    md+= [f"- [{t['name']}]({t['url']})：{t['desc']}（{AV[av(t)]}，{t['pricing']}{'，GitHub ★ %s'%t['stars'] if t.get('stars') else ''}{'，新收录' if t.get('new') else ''}）" for t in s["tools"]]
md.append("\n## 热门排行榜（依据 GitHub Star 数）\n"); md+=[f"{i+1}. {t['name']} — ★ {t['stars']}" for i,t in enumerate(d["leaderboard"])]
md.append(f"\n## 每日新品快报（{day}）\n"); md+=[f"- [{i['title']}]({i['url']})（{i['source']}，{i['metric']}）{i['desc']}" for i in d["daily"]]
open("tools.md","w").write("\n".join(md)+"\n")
open("llms.txt","w").write(f"""# AI 工具导航

> 面向中文用户的 AI 工具导航站：按业务场景（写作、编程/Vibe coding、图像设计、视频、音频、游戏开发、智能体/自动化、办公效率、客服营销）推荐真实 AI 工具，提供基于 GitHub Star 的开源工具排行榜，并每日自动抓取 GitHub 与 Hacker News 上新出现的热门 AI 项目。数据每日更新，最近更新：{upd}。

## 主要内容
- [全部工具清单（Markdown）]({B}/tools.md)：所有工具的名称、官网、一句话介绍、收费方式
- [结构化数据（JSON）]({B}/data/tools.json)
- [首页]({B}/)

## 场景页面
"""+"\n".join(f"- [{s['name']}]({B}/s/{s['slug']}.html)" for s in d["scenes"])+"\n\n## 说明\n- 场景内排序：按 Tranco 网站流行度排名（独立域名），其后按 GitHub Star，其余无数据；与国内/境外无关。每个工具的 signal 字段记录信号与来源。\n- 排行榜只统计有公开 GitHub 仓库的开源工具，依据为 Star 数。\n- 每个工具标注可用性：国内服务 / 开源可本地部署 / 境外服务（国内可能无法直接使用）。境外服务仅作客观介绍。\n- 标注“新收录”的条目由程序按关键词自动归类，未经人工审核。\n")
def static(fn,title,body):
    open(fn,"w").write(page(fn,title+" | AI 工具导航",title+" - AI 工具导航",title,f'<section class="doc">{body}</section>',[],""))
static("about.html","关于本站",f'''<h2>关于本站</h2><p>AI 工具导航是一个面向中文用户的非营利性信息整理站点，按业务场景收录 AI 工具的名称、官网链接、简介与收费方式，并提供开源项目 GitHub Star 排行与每日新项目快报。</p>
<p>收录原则：兼顾面向中国大陆用户提供服务的国内产品与境外、开源工具；开源工具标注“开源，可本地部署”；境外服务标注“境外服务，国内可能无法直接使用”，仅作客观信息介绍，本站不提供任何访问境外服务的方法或工具。</p>
<h3 id="rank-method">排序方法</h3><p>场景内工具按公开、可引用的流行度信号排序，与是否国内服务无关；“国内服务 / 开源 / 境外服务”仅作可用性标注。</p><ol>
<li>官网位于独立域名的工具，按 <a href="https://tranco-list.eu/">Tranco</a> 网站流行度排名排序（综合 Chrome UX Report、Cloudflare Radar、Cisco Umbrella、Majestic、Farsight 近 30 天数据，每日自动更新）。</li>
<li>官网是大平台子域名或子页面的工具（如 yiyan.baidu.com、github.com 上的项目）无法单独统计，排在其后；其中有开源仓库的按 GitHub Star 数排序。</li>
<li>两者都没有的标注“暂无流行度数据”，排在最后。</li></ol>
<p>局限：Tranco 统计的是整个域名的流量，对“产品内置 AI 功能”（如飞书、钉钉、Figma）反映的是整个产品的热度；其数据源对中国大陆流量覆盖有限，国内产品排名可能偏低。本站不编造任何数据，每个工具的信号与来源记录在 <a href="data/tools.json">data/tools.json</a> 的 signal 字段。“热门排行榜”仅依据 GitHub Star 数。</p>
<p>站点代码开源于 <a href="https://github.com/NyxK7/ai-tools-nav">GitHub</a>。纠错、推荐或下架请求请通过 <a href="{FEED}">GitHub Issues</a> 提交。</p>''')
static("disclaimer.html","免责声明",f'''<h2>免责声明</h2><ol>
<li>本站内容仅供信息参考，不构成任何推荐、背书或投资建议。工具功能、价格、可用性以各官网为准，可能随时变化。</li>
<li>本站链接指向第三方网站，本站不对第三方网站的内容、服务、隐私做法及合规性负责。用户使用第三方服务时应自行阅读并遵守其用户协议。</li>
<li>标注“境外服务”的工具可能未在中国大陆提供服务或未完成相关备案，本站仅作客观介绍，不提供、不鼓励任何违反法律法规的访问方式。请用户遵守《生成式人工智能服务管理暂行办法》等所在地法律法规。</li>
<li>“每日新品快报”和“新收录”内容由程序自动抓取与归类，未经人工审核，可能存在错误。</li>
<li>如认为本站内容侵犯您的合法权益或存在错误，请通过 <a href="{FEED}">GitHub Issues</a> 联系，我们将及时核实处理。</li></ol>''')
static("privacy.html","隐私政策",f'''<h2>隐私政策</h2><p>更新日期：2026-10-16</p>
<h3>1. 我们收集的信息</h3><p>本站无需注册。仅当您主动订阅邮件周刊时，我们收集您填写的<strong>邮箱地址</strong>。为防止滥用，订阅接口会临时使用请求 IP 做频率限制（仅保存在服务器内存中，不做持久存储）。</p>
<p>托管于 Vercel 的站点版本使用 Vercel Web Analytics 统计匿名访问量（不使用 Cookie、不识别个人身份）。GitHub Pages 版本不加载该统计脚本。</p>
<h3>2. 使用目的</h3><p>邮箱仅用于向您发送 AI 工具周刊，不用于其他目的，不出售、不出租给任何第三方。</p>
<h3>3. 存储与跨境传输</h3><p>邮箱地址存储于邮件服务商 Resend（服务器位于境外）。订阅即表示您单独同意将邮箱地址提供给该境外服务商用于发送周刊。网站托管服务商 Vercel、GitHub 同样位于境外。</p>
<h3>4. 保存期限</h3><p>保存至您退订为止；退订后我们将停止发送并在合理期限内删除您的邮箱。</p>
<h3>5. 您的权利与退订</h3><p>您可随时退订：每封周刊邮件均提供退订链接；也可在下方输入邮箱直接退订。如需查询、更正或删除数据，请通过 <a href="{FEED}">GitHub Issues</a> 联系（请勿在公开 Issue 中填写邮箱）。</p>
<form class="sub" id="unsubf" action="{API.replace("subscribe","unsubscribe")}" method="post"><label for="uem" class="sr">邮箱地址</label><input id="uem" name="email" type="email" placeholder="your@email.com" required maxlength="254"><input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px"><button type="submit">退订</button></form><p id="unsubm" role="status" aria-live="polite"></p>
<h3>6. 未成年人</h3><p>本站不面向未满 14 周岁的未成年人收集信息。</p>
<h3>7. 变更</h3><p>本政策变更将在本页更新并注明日期。</p>''')
print("built",len(alltools),"tools")
