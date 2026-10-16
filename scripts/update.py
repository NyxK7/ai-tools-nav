"""每日更新：抓取 GitHub stars、GitHub 新热门 AI 仓库、Hacker News AI 热帖。"""
import json,os,urllib.request,urllib.parse,datetime
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
d["leaderboard"]=sorted(board,key=lambda x:-x["stars"])
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
if items: d["daily"]=items
d["updated"]=now.strftime("%Y-%m-%d %H:%M UTC")
json.dump(d,open("data/tools.json","w"),ensure_ascii=False,indent=1)
print(len(board),"ranked,",len(items),"daily")
