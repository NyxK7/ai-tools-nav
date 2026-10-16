const $=s=>document.querySelector(s),esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
let D,cur=0;
fetch("data/tools.json?"+Date.now()).then(r=>r.json()).then(d=>{D=d;$("#upd").textContent=d.updated||"-";tabs();scenes();rank();daily();});
function tabs(){$("#sceneTabs").innerHTML=D.scenes.map((s,i)=>`<button class="${i==cur?"on":""}" data-i="${i}">${esc(s.name)}</button>`).join("");
document.querySelectorAll("#sceneTabs button").forEach(b=>b.onclick=()=>{cur=+b.dataset.i;$("#q").value="";tabs();scenes();});}
const card=(t,sc)=>`<div class="card"><a class="t" href="${esc(t.url)}" target="_blank" rel="noopener">${esc(t.name)}</a><div class="d">${esc(t.desc)}</div><span class="tag">${esc(t.pricing)}${sc?" · "+esc(sc):""}${t.stars?" · ★ "+t.stars.toLocaleString():""}</span></div>`;
function scenes(){const q=$("#q").value.trim().toLowerCase();
let list=q?D.scenes.flatMap(s=>s.tools.filter(t=>(t.name+t.desc).toLowerCase().includes(q)).map(t=>card(t,s.name))):D.scenes[cur].tools.map(t=>card(t));
$("#sceneList").innerHTML=list.join("")||"<p>没有找到匹配的工具</p>";}
$("#q").oninput=()=>{scenes();location.hash="";};
function rank(){$("#rankList").innerHTML=D.leaderboard.map(t=>`<li><a href="${esc(t.url)}" target="_blank" rel="noopener">${esc(t.name)}</a> <small>${esc(t.scene)}</small><span>★ ${t.stars.toLocaleString()}</span></li>`).join("");}
function daily(){$("#dailyList").innerHTML=D.daily.map(i=>`<div class="card"><a class="t" href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a><div class="d">${esc(i.desc)}</div><span class="tag">${esc(i.source)} · ${esc(i.metric)}</span>${i.hn?`<a class="d" href="${esc(i.hn)}" target="_blank" rel="noopener">HN 讨论</a>`:""}</div>`).join("")||"<p>今日暂无</p>";}
