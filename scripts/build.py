"""由 data/tools.json 生成静态 HTML（首页 + 场景页）、sitemap.xml、robots.txt、llms.txt、tools.md。"""
import json,html,os,datetime
B="https://nyxk7.github.io/ai-tools-nav"
d=json.load(open("data/tools.json")); E=lambda s:html.escape(str(s or ""),quote=True)
upd=d.get("updated") or ""; day=upd[:10] or datetime.date.today().isoformat()
FEED="https://github.com/NyxK7/ai-tools-nav/issues/new/choose"
def card(t,sc=None):
    tags=[t["pricing"]]+([sc] if sc else [])+([f"★ {t['stars']:,}"] if t.get("stars") else [])
    new='<span class="new">新收录</span>' if t.get("new") else ""
    return (f'<li class="card" data-k="{E((t["name"]+" "+t["desc"]).lower())}"><h3><a href="{E(t["url"])}" target="_blank" rel="noopener">{E(t["name"])}</a>{new}</h3>'
            f'<p>{E(t["desc"])}</p><span class="tag">{E(" · ".join(tags))}</span></li>')
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
<nav aria-label="主导航"><a href="{root}#scenes">场景导航</a><a href="{root}#rank">热门排行榜</a><a href="{root}#daily">每日新品快报</a><a href="{root}#subscribe">邮件订阅</a><a href="{FEED}" target="_blank" rel="noopener">反馈建议</a></nav>
<nav class="scn" aria-label="业务场景">{navs}</nav></header>
<main id="main">{body}</main>
<footer><p>数据更新时间：{E(upd)} · 每日自动更新 · <a href="{root}tools.md">纯文本工具清单</a> · <a href="{root}llms.txt">llms.txt</a> · <a href="https://github.com/NyxK7/ai-tools-nav">源码</a> · <a href="{FEED}" target="_blank" rel="noopener">反馈</a></p>
<p>工具介绍与价格以官网为准，本站不收取工具方费用。</p></footer><script src="{root}app.js" defer></script></body></html>'''
alltools=[t for s in d["scenes"] for t in s["tools"]]
sub=f'''<section id="subscribe" aria-labelledby="h-sub"><h2 id="h-sub">邮件订阅（即将上线）</h2><p>每周一封：本周最值得试的 AI 新工具 + 场景选型建议。订阅功能正在准备中，
可先 <a href="https://github.com/NyxK7/ai-tools-nav" target="_blank" rel="noopener">在 GitHub 上 Watch 本项目</a> 获取更新。</p>
<form class="sub" onsubmit="return false"><label for="em" class="sr">邮箱地址</label><input id="em" type="email" placeholder="your@email.com" disabled><button type="button" disabled>即将上线</button></form>
<p>发现工具失效、想推荐工具或有建议？<a href="{FEED}" target="_blank" rel="noopener">在 GitHub Issues 反馈</a></p></section>'''
# 首页
sc="".join(f'<section class="scene" id="{s["slug"]}" aria-labelledby="h-{s["slug"]}"><h3 id="h-{s["slug"]}"><a href="s/{s["slug"]}.html">{E(s["name"])}</a> <small>{len(s["tools"])} 个工具</small></h3><ul class="grid">{"".join(card(t) for t in s["tools"])}</ul></section>' for s in d["scenes"])
rk="".join(f'<li><a href="{E(t["url"])}" target="_blank" rel="noopener">{E(t["name"])}</a> <small>{E(t["scene"])}</small><span>★ {t["stars"]:,}</span></li>' for t in d["leaderboard"])
dl="".join(f'<li class="card"><h3><a href="{E(i["url"])}" target="_blank" rel="noopener nofollow">{E(i["title"])}</a></h3><p>{E(i["desc"])}</p><span class="tag">{E(i["source"])} · {E(i["metric"])}</span>'+(f' <a href="{E(i["hn"])}" target="_blank" rel="noopener nofollow">HN 讨论</a>' if i.get("hn") else "")+'</li>' for i in d["daily"])
body=f'''<div class="search"><label for="q" class="sr">搜索工具</label><input id="q" type="search" placeholder="搜索工具名称或用途，如：视频、写代码…"></div>
<section id="scenes" aria-labelledby="h-scenes"><h2 id="h-scenes">按业务场景导航</h2>{sc}<p id="none" hidden>没有找到匹配的工具</p></section>
<section id="rank" aria-labelledby="h-rank"><h2 id="h-rank">热门排行榜</h2><p class="note">排名依据：开源工具在 GitHub 上的实时 Star 数（每日通过 GitHub API 更新）。闭源工具没有公开可比数据，暂不参与排名。</p><ol class="rank">{rk}</ol></section>
<section id="daily" aria-labelledby="h-daily"><h2 id="h-daily">每日新品快报 <small>{E(day)}</small></h2><p class="note">来源：GitHub 近 7 天新建、带 ai 主题的仓库（按 Star 排序）与 Hacker News 近 48 小时 AI 相关 Show HN 热帖。程序自动抓取，未经人工审核。</p><ul class="grid">{dl or "<li>今日暂无</li>"}</ul></section>{sub}'''
site={"@context":"https://schema.org","@type":"WebSite","name":"AI 工具导航","url":B+"/","inLanguage":"zh-CN"}
open("index.html","w").write(page("index.html","AI 工具导航 | 按业务场景选 AI 工具 · 热门 AI 排行榜 · 每日新品",
 f"中文 AI 工具导航：写作、编程/Vibe coding、图像、视频、音频、游戏开发、智能体等 {len(d['scenes'])} 大场景 {len(alltools)} 款 AI 工具推荐，GitHub Star 热门排行榜，每日自动追踪新发布的热门 AI 项目。",
 "AI工具,AI工具导航,AI工具排行榜,AI智能体,Vibe coding,AI编程工具,AI绘画,AI视频生成,AI写作,最新AI工具",body,[site,ld_list("AI 工具导航",alltools)],""))
os.makedirs("s",exist_ok=True)
for s in d["scenes"]:
    names="、".join(t["name"] for t in s["tools"][:5])
    b=f'<section aria-labelledby="h-s"><h2 id="h-s">{E(s["name"])} 场景推荐 AI 工具（{len(s["tools"])} 个）</h2><ul class="grid">{"".join(card(t) for t in s["tools"])}</ul></section>{sub}'
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"AI 工具导航","item":B+"/"},{"@type":"ListItem","position":2,"name":s["name"],"item":f"{B}/s/{s['slug']}.html"}]}
    open(f"s/{s['slug']}.html","w").write(page(f"s/{s['slug']}.html",f"{s['name']} AI 工具推荐 | AI 工具导航",
      f"{s['name']}场景最好用的 AI 工具推荐：{names} 等，附中文介绍、官网链接与收费方式，每日更新。",
      f"{s['name']}AI工具,{s['name']}AI,AI工具推荐,AI工具导航",b,[bc,ld_list(s["name"]+" AI 工具",s["tools"])],"../"))
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+
 "".join(f"<url><loc>{u}</loc><lastmod>{day}</lastmod><changefreq>daily</changefreq></url>" for u in [B+"/"]+[f"{B}/s/{s['slug']}.html" for s in d["scenes"]]+[B+"/tools.md",B+"/llms.txt"])+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {B}/sitemap.xml\n")
md=[f"# AI 工具导航 · 全部工具清单\n\n> 中文 AI 工具导航，按业务场景推荐 AI 工具。数据更新：{upd}。网站：{B}/\n"]
for s in d["scenes"]:
    md.append(f"\n## {s['name']}\n")
    md+= [f"- [{t['name']}]({t['url']})：{t['desc']}（{t['pricing']}{'，GitHub ★ %s'%t['stars'] if t.get('stars') else ''}{'，新收录' if t.get('new') else ''}）" for t in s["tools"]]
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
"""+"\n".join(f"- [{s['name']}]({B}/s/{s['slug']}.html)" for s in d["scenes"])+"\n\n## 说明\n- 排行榜只统计有公开 GitHub 仓库的开源工具，依据为 Star 数。\n- 标注“新收录”的条目由程序按关键词自动归类，未经人工审核。\n")
print("built",len(alltools),"tools")
