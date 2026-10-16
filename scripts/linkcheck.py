"""检查所有官网链接。用法: python scripts/linkcheck.py [--prune-auto]
--prune-auto: 自动删除失效的“新收录”条目（人工精选条目只报告不删除）。"""
import json,sys,urllib.request,concurrent.futures as cf
d=json.load(open("data/tools.json"))
def ok(u):
    for m in ("HEAD","GET"):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,method=m,headers={"User-Agent":"Mozilla/5.0 (link-check; ai-tools-nav)"}),timeout=20); return r.status
        except urllib.error.HTTPError as e:
            if e.code in (401,403,405,429,999): return e.code  # 反爬/限流，不算失效
            st=e.code
        except Exception as e: st=str(e)[:60]
    return st
tools=[(s,t) for s in d["scenes"] for t in s["tools"]]
with cf.ThreadPoolExecutor(16) as ex: res=list(ex.map(lambda st:ok(st[1]["url"]),tools))
bad=[(s["name"],t["name"],t["url"],r) for (s,t),r in zip(tools,res) if not isinstance(r,int) or r>=400 and r not in (401,403,405,429,999)]
for b in bad: print("失效:",*b)
if "--prune-auto" in sys.argv and bad:
    dead={b[2] for b in bad}
    for s in d["scenes"]: s["tools"]=[t for t in s["tools"] if not (t.get("auto") and t["url"] in dead)]
    json.dump(d,open("data/tools.json","w"),ensure_ascii=False,indent=1)
print(f"检查 {len(tools)} 个链接，失效 {len(bad)} 个")
