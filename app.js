// 渐进增强：页面内容已静态生成，JS 仅提供搜索过滤
const q=document.getElementById("q");
if(q)q.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();let n=0;
document.querySelectorAll(".scene").forEach(s=>{let c=0;s.querySelectorAll(".card").forEach(li=>{const m=!v||li.dataset.k.includes(v);li.hidden=!m;if(m)c++;});s.hidden=!c;n+=c;});
document.getElementById("none").hidden=n>0;});
// 订阅表单：POST 到 Vercel API（GitHub Pages 跨域 CORS）
const f=document.getElementById("subf");
if(f)f.addEventListener("submit",async e=>{e.preventDefault();const m=document.getElementById("subm"),b=f.querySelector("button");
b.disabled=true;m.textContent="提交中…";
try{const r=await fetch(f.action,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:f.email.value,website:f.website.value})});
const j=await r.json().catch(()=>({}));m.textContent=j.msg||(r.ok?"订阅成功":"订阅失败，请稍后再试");if(r.ok)f.reset();}
catch(_){m.textContent="网络错误，请稍后再试";}b.disabled=false;});
const uf=document.getElementById("unsubf");
if(uf)uf.addEventListener("submit",async e=>{e.preventDefault();const m=document.getElementById("unsubm");m.textContent="提交中…";
try{const r=await fetch(uf.action,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:uf.email.value,website:uf.website.value})});
const j=await r.json().catch(()=>({}));m.textContent=j.msg||(r.ok?"已退订":"退订失败，请稍后再试");}catch(_){m.textContent="网络错误，请稍后再试";}});
