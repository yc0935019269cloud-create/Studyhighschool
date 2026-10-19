
(function(){
'use strict';
const main=document.querySelector('main');if(!main)return;
const page=location.pathname.split('/').pop();
const subject=location.pathname.split('/').slice(-2,-1)[0];
const tools=document.createElement('div');tools.className='read-tools';
tools.innerHTML='<button type="button" data-action="font">字級：標準</button><button type="button" data-action="focus" aria-pressed="false">專心讀觀念</button><button type="button" data-action="print">列印本頁</button><input type="search" aria-label="搜尋本頁講義" placeholder="搜尋本頁關鍵字"><button type="button" data-action="find">找下一處</button><span class="search-status" aria-live="polite"></span>';
const header=main.querySelector('header');if(header)header.after(tools);else main.prepend(tools);
let large=false;try{large=localStorage.getItem('study-read-large')==='1'}catch(e){}
function font(){document.documentElement.style.setProperty('--read-scale',large?'1.13':'1');tools.querySelector('[data-action=font]').textContent=large?'字級：放大':'字級：標準'}font();
tools.querySelector('[data-action=font]').onclick=function(){large=!large;font();try{localStorage.setItem('study-read-large',large?'1':'0')}catch(e){}};
tools.querySelector('[data-action=focus]').onclick=function(){let on=document.body.classList.toggle('read-focus');this.setAttribute('aria-pressed',String(on));this.textContent=on?'顯示完整講義':'專心讀觀念'};
tools.querySelector('[data-action=print]').onclick=()=>window.print();
let needle='',matches=[],at=-1;
function find(){
 const q=tools.querySelector('input').value.trim();
 document.querySelectorAll('.read-match').forEach(e=>e.classList.remove('read-match'));
 if(q!==needle){needle=q;at=-1;matches=q?Array.from(main.querySelectorAll('.content p,.content li,.content td,.lesson-section p,.lesson-section summary,.reader-guide p')).filter(e=>e.textContent.includes(q)&&!Array.from(e.children).some(c=>c.textContent.includes(q))):[]}
 if(!matches.length){tools.querySelector('.search-status').textContent=q?'未找到，請換個詞':'請輸入關鍵字';return}
 at=(at+1)%matches.length;const el=matches[at];let d=el.closest('details');while(d){d.open=true;d=d.parentElement.closest('details')}
 if(el.closest('.q,.check-card')){document.body.classList.remove('read-focus');const b=tools.querySelector('[data-action=focus]');b.setAttribute('aria-pressed','false');b.textContent='專心讀觀念';document.body.classList.remove('only-marked');const om=document.getElementById('onlyMarked');if(om)om.classList.remove('active')}
 el.classList.add('read-match');el.scrollIntoView({block:'center',behavior:'smooth'});tools.querySelector('.search-status').textContent=(at+1)+' / '+matches.length;
}
tools.querySelector('[data-action=find]').onclick=find;tools.querySelector('input').onkeydown=e=>{if(e.key==='Enter')find()};
document.querySelectorAll('.lesson-widget').forEach(w=>{
 const type=w.dataset.widget;
 if(type==='humidity'){
 w.innerHTML='<h3>動手算｜相對濕度不是水氣總量</h3><p>先固定實際水氣壓，再調整溫度，觀察相對濕度。</p><label>氣溫 <input aria-label="氣溫" type="range" min="0" max="40" value="25"></label><label>實際水氣壓（百帕）<input aria-label="實際水氣壓" type="range" min="1" max="40" value="12"></label><output aria-live="polite"></output><svg viewBox="0 0 500 90" role="img" aria-label="水氣壓與飽和值比較"><rect x="10" y="20" width="450" height="32" rx="6" fill="var(--line)"/><rect class="water-bar" x="10" y="20" width="100" height="32" rx="6" fill="var(--accent)"/><text x="10" y="80" fill="currentColor" font-size="14">長條：實際水氣壓 ÷ 同溫飽和水氣壓</text></svg><p class="widget-note"></p><small>飽和水氣壓以液態水面的 Magnus 近似計算；超過飽和時僅提示凝結，不模擬雲滴成長。</small>';
 const inputs=w.querySelectorAll('input');function update(){const t=+inputs[0].value,e=+inputs[1].value,es=6.112*Math.exp(17.67*t/(t+243.5)),rh=e/es*100;w.querySelector('output').textContent=t+'°C；飽和值約 '+es.toFixed(1)+' hPa；相對濕度 '+rh.toFixed(1)+'%';w.querySelector('.water-bar').setAttribute('width',450*Math.min(rh,100)/100);w.querySelector('.widget-note').textContent=rh>100?'設定值超過飽和，真實系統可能凝結；不能把持續過飽和當一般穩定狀態。':rh>99?'接近飽和，適合思考露點與凝結條件。':'保持水氣壓不變而降溫，分母變小，所以相對濕度上升。'}inputs.forEach(i=>i.oninput=update);update();
 }
 if(type==='punnett'){
 w.innerHTML='<h3>動手排｜一對等位基因的組合</h3><p>模型：完全顯性、配子等機率、各型存活率相同。</p><label>親代一 <select aria-label="親代一"><option>AA</option><option selected>Aa</option><option>aa</option></select></label><label>親代二 <select aria-label="親代二"><option>AA</option><option selected>Aa</option><option>aa</option></select></label><table aria-label="配子組合方格"></table><output aria-live="polite"></output>';
 const sels=w.querySelectorAll('select');function update(){const a=sels[0].value.split(''),b=sels[1].value.split(''),cs=[];w.querySelector('table').innerHTML='<tr><th>配子</th>'+b.map(x=>'<th scope="col">'+x+'</th>').join('')+'</tr>'+a.map(x=>'<tr><th scope="row">'+x+'</th>'+b.map(y=>{let g=[x,y].sort().join('');cs.push(g);return '<td>'+g+'</td>'}).join('')+'</tr>').join('');const n=g=>cs.filter(x=>x===g).length*25;w.querySelector('output').textContent='AA '+n('AA')+'% ／ Aa '+n('Aa')+'% ／ aa '+n('aa')+'%；顯性表現 '+(100-n('aa'))+'%'}sels.forEach(s=>s.onchange=update);update();
 }
 if(type==='linkage'){
 w.innerHTML='<h3>動手配｜連鎖時四種配子不一定等量</h3><p>固定相引排列 AB／ab，與 ab／ab 試交；假設互為對應的兩類機率相等。</p><label>重組率 r（%）<input type="range" aria-label="重組率" min="0" max="50" value="20"></label><output aria-live="polite"></output><svg viewBox="0 0 500 140" aria-label="四種配子機率" role="img"></svg><small>r＝50%無法區別不同染色體與同染色體上距離很遠的基因。</small>';
 function update(){let r=+w.querySelector('input').value,vs=[(100-r)/2,(100-r)/2,r/2,r/2],ns=['AB','ab','Ab','aB'];w.querySelector('output').textContent='重組率 '+r+'%；親型各 '+vs[0]+'%，重組型各 '+vs[2]+'%';w.querySelector('svg').innerHTML=vs.map((v,i)=>'<text x="0" y="'+(i*34+22)+'" fill="currentColor" font-size="15">'+ns[i]+'</text><rect x="45" y="'+(i*34+6)+'" width="'+(v*7)+'" height="20" rx="4" fill="'+(i<2?'var(--accent)':'var(--pr)')+'"/><text x="'+(v*7+55)+'" y="'+(i*34+22)+'" fill="currentColor" font-size="15">'+v+'%</text>').join('')}w.querySelector('input').oninput=update;update();
 }
});
})();
