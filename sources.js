
(function(){'use strict';
const books=window.SOURCE_BOOKS;if(!books){document.getElementById('status').textContent='原講義目錄未載入，請確認 source-pages.js 與本頁放在一起。';return}
const $=id=>document.getElementById(id);let book=books[0],page=1;
$('book').innerHTML=books.map(b=>'<option value="'+b.id+'">'+b.id+'（'+b.total+'頁）</option>').join('');
function readHash(){const h=new URLSearchParams(location.hash.slice(1));book=books.find(b=>b.id===h.get('book'))||books[0];page=Math.max(1,Math.min(book.total,Number(h.get('page'))||1));page=Math.floor(page);render()}
function route(b,p){book=b;page=Math.max(1,Math.min(b.total,p));const hash='#book='+encodeURIComponent(b.id)+'&page='+page;history.pushState(null,'',hash);render()}
function render(){
 const p=book.pages[page-1];$('book').value=book.id;$('page').max=book.total;$('page').value=page;
 $('title').textContent=book.id+' · 第 '+page+' 頁｜'+p.topic;$('lesson').href=p.lesson;
 $('count').textContent=page+' / '+book.total;$('text').textContent=p.text;
 $('original').alt=book.id+' PDF第'+page+'頁完整原頁：'+p.topic;
 $('status').textContent='正在載入原頁…';$('original').onload=()=>{$('status').textContent='完整原頁已載入'};
 $('original').onerror=()=>{$('status').textContent='原頁載入失敗，請重新整理或檢查網路。'};
 $('original').src=p.image;
 ['prev','prevBottom'].forEach(id=>$(id).disabled=page<=1);['next','nextBottom'].forEach(id=>$(id).disabled=page>=book.total);
 const groups=[];book.pages.forEach(p=>{const last=groups[groups.length-1];if(last&&last.topic===p.topic)last.end=p.page;else groups.push({topic:p.topic,start:p.page,end:p.page})});
 $('chapters').replaceChildren(...groups.map(g=>{const b=document.createElement('button');b.textContent=g.topic;const s=document.createElement('small');s.textContent='PDF '+g.start+'–'+g.end+'頁';b.append(s);if(page>=g.start&&page<=g.end){b.className='current';b.setAttribute('aria-current','true')}b.onclick=()=>route(book,g.start);return b}));
}
$('book').onchange=()=>route(books.find(b=>b.id===$('book').value),1);$('go').onclick=()=>route(book,Math.floor(Number($('page').value)||1));$('page').onkeydown=e=>{if(e.key==='Enter')$('go').click()};
['prev','prevBottom'].forEach(id=>$(id).onclick=()=>route(book,page-1));['next','nextBottom'].forEach(id=>$(id).onclick=()=>route(book,page+1));
$('zoom').onclick=function(){const on=$('imageWrap').classList.toggle('zoom');this.setAttribute('aria-pressed',String(on));this.textContent=on?'回到適合寬度':'放大原頁'};$('original').onclick=()=>$('zoom').click();$('print').onclick=()=>window.print();
function search(){const q=$('search').value.replace(/\s/g,'');const results=$('results');results.replaceChildren();if(!q){results.textContent='請先輸入關鍵字。';return}
const found=[];books.forEach(b=>b.pages.forEach(p=>{const text=(p.topic+p.text).replace(/\s/g,'');if(text.includes(q))found.push({b,p})}));
const intro=document.createElement('p');intro.textContent='找到 '+found.length+' 頁'+(found.length>80?'，先顯示前80筆，請增加關鍵字縮小範圍。':'。');results.append(intro);
found.slice(0,80).forEach(({b,p})=>{const bt=document.createElement('button');bt.textContent=b.id+' · PDF '+p.page+'頁｜'+p.topic;bt.onclick=()=>{route(b,p.page);$('title').scrollIntoView({block:'start'})};results.append(bt)});
}
$('find').onclick=search;$('search').onkeydown=e=>{if(e.key==='Enter')search()};
document.addEventListener('keydown',e=>{if(e.target.closest('input,select,textarea')||e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowLeft'){e.preventDefault();route(book,page-1)}if(e.key==='ArrowRight'){e.preventDefault();route(book,page+1)}});
window.addEventListener('hashchange',readHash);window.addEventListener('popstate',readHash);readHash();
})();
