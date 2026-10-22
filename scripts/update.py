"""每日更新：抓取 GitHub stars、GitHub 新热门 AI 仓库、Hacker News AI 热帖，并合并 pinned_digest 中的置顶条目。"""
import json,os,urllib.request,urllib.parse,datetime
from digest import merge
T=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
def get(u,gh=False):
    h={"User-Agent":"ai-tools-nav"}
    if gh and T: h["Authorization"]="Bearer "+T
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30))
d=json.load(open("data/tools.json"))
now=datetime.datetime.now(datetime.timezone.utc)
board=[]
for s in d["scenes"]:
    for t in s["tools"]:
        if t.get("github"):
            try:
                r=get("https://api.github.com/repos/"+t["github"],True)
                t["stars"]=r["stargazers_count"]; board.append({"name":t["name"],"url":t["url"],"scene":s["name"],"stars":t["stars"],"repo":t["github"]})
            except Exception as e: print("skip",t["github"],e)
since=(now-datetime.timedelta(days=7)).strftime("%Y-%m-%d")
items=[]
try:
    q=urllib.parse.quote(f"topic:ai created:>{since}")
    for r in get(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=10",True)["items"]:
        items.append({"source":"GitHub","title":r["full_name"],"url":r["html_url"],"desc":(r["description"] or "")[:160],"metric":f"★ {r['stargazers_count']}"})
except Exception as e: print("gh search fail",e)
try:
    ts=int((now-datetime.timedelta(days=2)).timestamp())
    for h in get(f"https://hn.algolia.com/api/v1/search?query=AI&tags=show_hn&numericFilters=created_at_i>{ts},points>10&hitsPerPage=10")["hits"]:
        items.append({"source":"Hacker News","title":h["title"],"url":h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}","desc":"","metric":f"▲ {h['points']} 分","hn":f"https://news.ycombinator.com/item?id={h['objectID']}"})
except Exception as e: print("hn fail",e)
# —— 合规过滤：自动抓取的条目不收越狱、灰产中转/发卡、恶意软件、刷星、成人等内容 ——
BLOCK=["jailbreak","越狱","relay","中转","发卡","api key","free key","crack","破解","bypass","malware","exploit","ransomware","nsfw","porn","18+","色情","赌","gambling","casino","proxy pool","翻墙","vpn","star-buying","fake star","刷星","injector","dll inject","injection framework","harvest token","session cookie","anonymous account","bulk-create","sniper","автопилот"]
items=[it for it in items if not any(b in (it["title"]+" "+it["desc"]+" "+it["url"]).lower() for b in BLOCK)]
merge(d,items,now.date())  # 置顶的官方发布保留 14 天，其余为本次抓取

# —— 保守的自动收录：只收 GitHub 新仓库，Star≥200，且只命中一个场景的关键词 ——
RULES={"coding":["coding agent","code editor","copilot","vibe coding","code generation","ide","developer tool","cli for code"],
"image":["image generation","text-to-image","diffusion","stable diffusion","image editing"],
"video":["video generation","text-to-video","video editing"],
"audio":["text-to-speech","tts","speech recognition","voice clone","music generation","asr"],
"gamedev":["game engine","game development","gamedev"],
"agents":["ai agent","agent framework","multi-agent","workflow automation","mcp server","autonomous agent"],
"writing":["writing assistant","copywriting"],
"productivity":["note-taking","presentation","slides","pdf"],
"marketing":["customer support","chatbot for support","marketing"]}
import re
existing={t["url"].rstrip("/").lower() for s in d["scenes"] for t in s["tools"]}
bys={s["slug"]:s for s in d["scenes"]}
today=now.strftime("%Y-%m-%d")
for it in items:
    if it["source"]!="GitHub" or int(it["metric"].split()[-1])<200: continue
    text=(it["title"]+" "+it["desc"]).lower()
    hit=[k for k,ws in RULES.items() if any(re.search(r"\b"+re.escape(w)+r"\b",text) for w in ws)]
    if len(hit)!=1 or it["url"].lower() in existing: continue
    bys[hit[0]]["tools"].append({"name":it["title"].split("/")[-1],"url":it["url"],"desc":it["desc"] or "GitHub 新热门开源项目",
      "pricing":"开源","avail":"oss","github":it["title"],"auto":True,"added":today})
    existing.add(it["url"].lower()); print("新收录",hit[0],it["title"])
# 新收录标记保留 14 天
for s in d["scenes"]:
    for t in s["tools"]:
        t["new"]=bool(t.get("added")) and (now-datetime.datetime.fromisoformat(t["added"]).replace(tzinfo=datetime.timezone.utc)).days<14
d["updated"]=now.strftime("%Y-%m-%d %H:%M UTC")
json.dump(d,open("data/tools.json","w"),ensure_ascii=False,indent=1)
print(len(board),"stars refreshed,",len(items),"fetched,",len(d["daily"]),"daily (incl. pinned)")
