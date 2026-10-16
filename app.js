// 渐进增强：页面内容已静态生成，JS 仅提供搜索过滤
const q=document.getElementById("q");
if(q)q.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();let n=0;
document.querySelectorAll(".scene").forEach(s=>{let c=0;s.querySelectorAll(".card").forEach(li=>{const m=!v||li.dataset.k.includes(v);li.hidden=!m;if(m)c++;});s.hidden=!c;n+=c;});
document.getElementById("none").hidden=n>0;});
