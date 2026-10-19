"""Rebuild the added reading layer without regenerating or replacing original questions."""
from pathlib import Path
import re,json,html
ROOT=Path(__file__).resolve().parent.parent
UNITS=json.loads((ROOT/'_src/continuation.json').read_text(encoding='utf-8'))
GUIDES=json.loads((ROOT/'_src/reading-guides.json').read_text(encoding='utf-8'))
E=html.escape
def marked(name,text): return '<!-- '+name+' START -->'+text+'<!-- '+name+' END -->'
def strip(text,name): return re.sub(r'<!-- '+name+r' START -->.*?<!-- '+name+r' END -->','',text,flags=re.S)
def flow(items):return '<div class="flow" aria-label="概念推理順序">'+('<b aria-hidden="true">→</b>'.join('<span>'+E(x)+'</span>' for x in items))+'</div>'
def source_url(subject,book=None,page=1):
 book=book or ('地科1' if subject=='earth' else '生物1')
 return '../sources.html#book='+book+'&page='+str(page)
def nav(subject):
 us=[u for u in UNITS if u['subject']==subject]
 return '<div class="extension-nav"><div class="nch">接著讀｜完整後續講義</div><ul>'+''.join('<li><a href="u'+u['id']+'.html"><span>'+u['id']+'</span>'+E(u['title'])+'</a></li>' for u in us)+'</ul><p><a href="'+source_url(subject)+'">原講義逐頁閱讀 →</a></p></div>'
def catalog(subject,prefix=''):
 return '<section class="ext-index"><h2>接著讀：'+('大氣・海洋・災害・氣候與探究' if subject=='earth' else '遺傳學')+'</h2><p>依原講義主題延伸，先理解，再練習；原頁可逐頁對照。</p><div class="lesson-links">'+''.join('<a href="'+prefix+'u'+u['id']+'.html"><b>'+u['id']+'　'+E(u['title'])+'</b><small>'+u['source']+'｜概念推理・比較表・六題檢核</small></a>' for u in UNITS if u['subject']==subject)+'</div></section>'
def reading(g):
 title,p1,p2,steps,q,a=g
 return '<section class="reader-guide"><div class="rg-top"><span class="rg-kicker">READ & REASON / 閱讀引導</span><h2>'+E(title)+'</h2><p>'+E(p1)+'</p></div><div class="rg-body">'+flow(steps.split('→'))+'<p>'+E(p2)+'</p><details><summary>先停一下：'+E(q)+'</summary><p>'+E(a)+'</p></details></div></section>'
def detail(q,a,topic):
 return '<details class="sol micro-check"><summary>'+E(q)+'</summary><dl class="micro-answer"><dt>考什麼</dt><dd>'+E(topic)+'</dd><dt>怎麼想</dt><dd>先辨認題目給的條件與要比較的量，再沿本節的機制判斷。</dd><dt>答案與理由</dt><dd>'+E(a)+'</dd><dt>常見錯誤</dt><dd>把名稱直接當原因，或忽略題目的範圍與前提。請用答案中的機制核對自己的說法。</dd><dt>再確認一次</dt><dd>遮住答案，試著用完整的一句話向同學說明理由，並指出題目中最關鍵的條件。</dd></dl></details>'
# Use established shell: inline original CSS, menu, image lightbox, and solution controls.
for subject in ('earth','biology'):
 base=(ROOT/subject/'u1-1.html').read_text(encoding='utf-8')
 base=strip(strip(base,'reading-guide'),'handout-assets')
 base=strip(base,'continuation-nav')
 base=re.sub(r'<ul class="subtoc">.*?</ul>','',base,flags=re.S)
 base=re.sub(r'<li><a href="u(?:[4-8]-[1-4]|3-[1-5])\.html".*?</li>','',base) if False else base
 for i,u in enumerate([x for x in UNITS if x['subject']==subject]):
  groups=[x for x in UNITS if x['subject']==subject]
  sections=''.join('<section class="lesson-section" id="learn-'+str(j+1)+'"><h2>'+str(j+1)+'　'+E(s['title'])+'</h2><p>'+E(s['text'])+'</p><h3>讀完就練</h3>'+''.join(detail(q,a,s['title']) for q,a in s['questions'])+'</section>' for j,s in enumerate(u['sections']))
  rows='<table class="lesson-table"><caption>本節比較表</caption><thead><tr><th>概念</th><th>判斷要點</th><th>使用時注意</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(x)+'</td>' for x in row)+'</tr>' for row in u['rows'])+'</tbody></table>'
  widget='<div class="lesson-widget" data-widget="'+u['widget']+'"></div>' if u['widget'] else ''
  book=u['source']; page=int(re.search(r'\d+',u['pages'])[0])
  source='<aside class="source-links"><b>回到原講義</b><p>'+book+'.pdf｜PDF第 '+u['pages']+' 頁（非印刷頁碼）。</p><a href="'+source_url(subject,book,page)+'">開啟原頁、練習題與手寫註記 →</a><p class="source-note">原講義全頁保留，沒有裁掉圖表、選項與附答。此頁六題為配合概念另編的檢核題。</p></aside>'
  if u['id']=='5-2' and subject=='earth': source+='<p class="source-note">機制核對：<a href="https://www.noaa.gov/jetstream/tropical/enso/enso-patterns">NOAA：聖嬰與海氣環流</a></p>'
  if u['id']=='3-5' and subject=='biology': source+='<p class="source-note">機制核對：<a href="https://openstax.org/books/biology-2e/pages/13-1-chromosomal-theory-and-genetic-linkage">OpenStax：基因連鎖與重組率</a></p>'
  teacher='<details class="reader-guide"><summary>帶課提示｜學生說不知道時</summary><div class="rg-body"><p>「我們先不急著回答整題。先看『'+E(u['sections'][0]['title'])+'』，把題目裡的對象和條件圈起來。接著只說第一個變化，再問它會讓下一步怎樣改變。最後回到比較表，檢查剛剛用了哪一條規則。」</p><p>先讓學生沿箭頭口述，再做每節兩題。若答案正確但無法說明理由，回到該節重新畫關係；能獨立解釋後，再到原講義做完整題組。</p></div></details>'
  pager='<div class="pager">'+('<a href="u'+groups[i-1]['id']+'.html">← '+E(groups[i-1]['title'])+'</a>' if i else '<a href="index.html">← 科目目錄</a>')+('<a href="u'+groups[i+1]['id']+'.html">'+E(groups[i+1]['title'])+' →</a>' if i+1<len(groups) else '<a href="index.html">回科目目錄 →</a>')+'</div>'
  main='<main class="main"><header class="lesson-hero"><div class="crumb">'+('地球科學' if subject=='earth' else '生物')+' / 電子講義 / '+u['id']+'</div><h1>'+E(u['title'])+'</h1><p>'+E(u['lead'])+'</p></header><div class="tools"><span class="cnt">六題自我檢核</span><button id="openAll">展開六題詳解</button><button id="closeAll">收起詳解</button></div><div class="content"><section class="reader-guide"><div class="rg-top"><span class="rg-kicker">先把因果順序接起來</span><h2>這一節，沿著這條線理解</h2>'+flow(u['flow'])+'</div><div class="rg-body"><p>先讀概念與比較表，再遮住答案自我檢核；原題圖表與完整頁面可從文末開啟。</p><nav aria-label="本頁目錄">'+''.join('<a href="#learn-'+str(j+1)+'">'+E(s['title'])+'</a>　' for j,s in enumerate(u['sections']))+'</nav></div></section>'+widget+sections+'<section class="lesson-section"><h2>帶走這張比較表</h2>'+rows+'</section>'+teacher+source+'</div>'+pager+'</main>'
  text=re.sub(r'<main\b.*?</main>',lambda _:main,base,count=1,flags=re.S)
  text=re.sub(r'<title>.*?</title>',lambda _:'<title>'+E(u['id']+' '+u['title'])+'｜'+('地球科學' if subject=='earth' else '生物')+'</title>',text,count=1)
  # Only the current unit may be highlighted.
  text=re.sub(r' class="on"','',text)
  (ROOT/subject/('u'+u['id']+'.html')).write_text(text,encoding='utf-8')
for subject in ('earth','biology'):
 for p in (ROOT/subject).glob('*.html'):
  text=p.read_text(encoding='utf-8')
  for name in ('handout-assets','continuation-nav','continuation-index','reading-guide'):
   text=strip(text,name)
  text=text.replace('</head>',marked('handout-assets','<link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../handout.css"><script defer src="../handout.js"></script>')+'</head>')
  # Sidebar exists on both index and lesson pages.
  text=re.sub(r'(</(?:aside|nav)>)(\s*<main)',lambda m:marked('continuation-nav',nav(subject))+m.group(1)+m.group(2),text,count=1)
  # The original shell uses aside.side; robust fallback if source tag changes.
  if 'continuation-nav START' not in text:
   text=re.sub(r'(<(?:aside|nav)[^>]*class="side"[^>]*>)',lambda m:m[0]+marked('continuation-nav',nav(subject)),text,count=1)
  key=p.stem[1:]
  if key in GUIDES[subject]:
   text=text.replace('<div class="content">','<div class="content">'+marked('reading-guide',reading(GUIDES[subject][key])),1)
  if p.name=='index.html':
   text=text.replace('</main>',marked('continuation-index',catalog(subject))+'</main>',1)
  else:
   text=text.replace('</main>',marked('continuation-index','<div class="source-note"><a href="'+source_url(subject)+'">原講義全頁對照閱讀</a>｜可切換冊別、跳頁與搜尋原文。</div>')+'</main>',1)
  # Highlight the added unit only in its own link.
  if any(u['subject']==subject and 'u'+u['id']+'.html'==p.name for u in UNITS):
   text=text.replace('<a href="'+p.name+'"><span>','<a class="on" href="'+p.name+'"><span>',1)
  p.write_text(text,encoding='utf-8')
home=ROOT/'index.html'
text=strip(home.read_text(encoding='utf-8'),'continuation-home')
text=text.replace('</head>','<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="handout.css"></head>') if 'href="handout.css"' not in text else text
extra='<section class="reader-guide"><div class="rg-top"><span class="rg-kicker">地科 × 生物 / 完整參考講義</span><h2>從原頁到理解，接著往下讀</h2><p>四份原講義共366頁完整收錄，可依冊別、單元與PDF頁碼對照。</p><a href="sources.html">開啟完整原頁閱讀器 →</a></div><div class="rg-body">'+catalog('earth','earth/')+catalog('biology','biology/')+'</div></section>'
text=text.replace('3 個單元 · 18 份講義','4 個單元 · 23 份講義').replace('4 個單元 · 21 份講義','9 個單元 · 32 份講義')
text=text.replace('</main>',marked('continuation-home',extra)+'</main>',1)
home.write_text(text,encoding='utf-8')
print(json.dumps({'new_units':len(UNITS),'new_checks':len(UNITS)*6,'existing_guides':sum(map(len,GUIDES.values()))}))
