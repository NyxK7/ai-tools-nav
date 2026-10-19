"""每日新品快报的人工置顶条目（data/tools.json 的 pinned_digest 数组）。
每条：{"source","title","url","desc","date":"YYYY-MM-DD"}。发布日期起 14 天内（与“新收录”标记相同）置顶显示在快报最前，
之后自动不再显示（条目本身保留在 pinned_digest 中作为记录）。update.py 和 build.py 都调用 merge，保证每日抓取不会冲掉置顶。"""
import datetime
PIN_DAYS=14
def active(d,today):
    out=[]
    for p in d.get("pinned_digest",[]):
        age=(today-datetime.date.fromisoformat(p["date"])).days
        if 0<=age<PIN_DAYS:
            out.append({"source":p["source"],"title":p["title"],"url":p["url"],"desc":p.get("desc",""),"metric":f"{p['date']} 发布","pinned":True,"date":p["date"]})
    return sorted(out,key=lambda x:x["date"],reverse=True)
def merge(d,items,today):
    """items：本次抓取结果；为 None/空时沿用上次的非置顶条目。"""
    pins=active(d,today); pu={p["url"] for p in pins}
    fresh=items or [i for i in d.get("daily",[]) if not i.get("pinned")]
    d["daily"]=pins+[i for i in fresh if i["url"] not in pu]
