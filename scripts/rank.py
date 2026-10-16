"""按公开可引用的流行度信号为每个场景内的工具排序，信号与来源写入 data/tools.json。
信号：Tranco 网站流行度排名（https://tranco-list.eu ，综合 CrUX/Cloudflare Radar/Umbrella/Majestic/Farsight 30 天数据）。
只对官网位于独立域名（裸域或 www.）的工具取排名；托管在大平台子域名/路径下的工具（如 yiyan.baidu.com、github.com/...）
无法单独归因，不赋排名。无排名的工具排在有排名的工具之后，其中有 GitHub 仓库的按 Star 数排序。绝不编造数字。"""
import csv,io,json,urllib.request
from urllib.parse import urlparse
UA={"User-Agent":"ai-tools-nav"}
meta=json.load(urllib.request.urlopen(urllib.request.Request("https://tranco-list.eu/api/lists/date/latest",headers=UA),timeout=60))
raw=urllib.request.urlopen(urllib.request.Request(meta["download"],headers=UA),timeout=300).read().decode()
R={dom:int(r) for r,dom in csv.reader(io.StringIO(raw))}
date=meta["configuration"]["endDate"]; lid=meta["list_id"]
d=json.load(open("data/tools.json"))
for s in d["scenes"]:
    for t in s["tools"]:
        u=urlparse(t["url"]); h=(u.hostname or "").removeprefix("www.")
        own=h.count(".")==1 and u.path.strip("/")==""  # 独立域名
        t.pop("signal",None)
        if own and h in R:
            t["signal"]={"type":"tranco","rank":R[h],"domain":h,"source":f"https://tranco-list.eu/list/{lid}/1000000","date":date}
        elif t.get("stars"):
            t["signal"]={"type":"github_stars","stars":t["stars"],"repo":t.get("github"),"source":f"https://github.com/{t.get('github')}"}
    s["tools"].sort(key=lambda t:(0,t["signal"]["rank"]) if t.get("signal",{}).get("type")=="tranco"
                    else (1,-t["signal"]["stars"]) if t.get("signal") else (2,0))
d["ranking"]={"method":"tranco","list_id":lid,"date":date}
json.dump(d,open("data/tools.json","w"),ensure_ascii=False,indent=1)
print("ranked; tranco list",lid,date)
