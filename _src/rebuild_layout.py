"""Match the established handouts: source screenshot, prose explanation, worked checks."""
from pathlib import Path
import json,re,html
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
U=json.loads((ROOT/'_src/continuation.json').read_text(encoding='utf-8'))
FIGS=json.loads((ROOT/'_src/layout-figures.json').read_text(encoding='utf-8'))
books=json.loads((ROOT/'source-pages.js').read_text(encoding='utf-8')[len('window.SOURCE_BOOKS='):-1])
E=html.escape
# PDF ranges for source pages embedded directly in each new handout.
RANGES={'earth/4-1':('地科2',1,5),'earth/4-2':('地科2',6,12),'earth/4-3':('地科2',13,18),'earth/4-4':('地科2',19,34),'earth/5-1':('地科2',35,45),'earth/5-2':('地科2',46,51),'earth/5-3':('地科2',52,57),'earth/6-1':('地科2',75,102),'earth/7-1':('地科3',1,8),'earth/7-2':('地科3',9,30),'earth/8-1':('地科3',31,56),'biology/3-1':('生物1',85,88),'biology/3-2':('生物1',89,93),'biology/3-3':('生物1',94,96),'biology/3-4':('生物1',97,99),'biology/3-5':('生物1',100,106)}
def para(t):return ''.join('<p>'+E(s)+'。</p>' for s in t.rstrip('。').split('。') if s)
def fig(u,j):
 book=u['source'];p,y0,y1,x0,x1,caption=FIGS[u['subject']+'/'+u['id']][j]
 dest=ROOT/u['subject']/'img'/('source_'+u['id']+'_'+str(j+1)+'.webp')
 src=ROOT/'source-pages'/book/(str(p).zfill(3)+'.webp')
 im=Image.open(src);w,h=im.size
 box=(round(w*x0/100),round(h*y0/100),round(w*x1/100),round(h*y1/100))
 crop=im.crop(box);crop.save(dest,'WEBP',quality=88,method=4)
 return '<figure class="fig source-figure"><img class="figimg" src="img/'+dest.name+'" width="'+str(crop.width)+'" height="'+str(crop.height)+'" loading="lazy" alt="'+E(caption)+'，'+book+' PDF第'+str(p)+'頁"><figcaption><b>'+E(caption)+'</b><span>'+book+' · PDF第'+str(p)+'頁截圖</span><a href="../sources.html#book='+book+'&page='+str(p)+'">對照完整原頁 ↗</a></figcaption></figure>'
def fullpages(u):
 key=u['subject']+'/'+u['id'];book,a,b=RANGES[key]
 nums=list(range(a,b+1))
 # The ocean interaction and exercise pages belong to ocean circulation, not the tides chapter.
 if key=='earth/5-2':nums+=list(range(58,75))
 pages={p['page']:p for bk in books if bk['id']==book for p in bk['pages']}
 out='<h2 class="section" id="original-pages">本節原頁與原題</h2><p>以下依PDF頁序保留完整題幹、圖表、選項與原附答。先看題目、遮住原附答作答，再回上面的觀念與例題核對思路。</p>'
 for n in nums:
  p=pages[n];out+='<details class="original-page" id="original-'+str(n)+'" data-book="'+book+'" data-page="'+str(n)+'"><summary>'+book+'｜PDF第 '+str(n)+' 頁　'+E(p['topic'])+'</summary><figure class="fig"><img class="figimg" loading="lazy" src="../'+p['image']+'" alt="'+book+' PDF第'+str(n)+'頁完整原圖"><figcaption>原講義PDF第'+str(n)+'頁；圖表、選項與附答完整保留。<a href="../sources.html#book='+book+'&page='+str(n)+'">放大閱讀 ↗</a></figcaption></figure></details>'
 return out
for u in U:
 p=ROOT/u['subject']/('u'+u['id']+'.html');t=p.read_text(encoding='utf-8')
 parts=[]
 for j,s in enumerate(u['sections']):
  # Same sequence as existing source handouts: title, source figure, corresponding explanation, practice.
  text='<h2 class="section" id="learn-'+str(j+1)+'">'+E(s['title'])+'</h2>'+fig(u,j)+'<div class="source-explanation"><h3>這張圖怎麼看</h3>'+para(s['text'])+'</div>'
  for k,(q,a) in enumerate(s['questions']):
   n=j*2+k+1
   text+='<article class="check-card" id="check-'+str(n)+'"><header class="qh"><span class="qn">隨堂練習 '+str(n)+'</span><span class="qtag">'+E(s['title'])+'</span></header><div class="qtext"><p>'+E(q)+'</p></div><details class="sol micro-check"><summary>看答案與詳解</summary><div class="exp"><b class="exp-h">解</b><p>'+E(a)+'</p></div></details></article>'
  if j==0 and u['widget']:text+='<details class="optional-widget"><summary>用數值驗證這個觀念</summary><div class="lesson-widget" data-widget="'+u['widget']+'"></div></details>'
  parts.append(text)
 rows='<h2 class="section" id="compare">最後一起比較</h2><table><thead><tr><th>概念</th><th>判讀重點</th><th>注意條件</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(v)+'</td>' for v in row)+'</tr>' for row in u['rows'])+'</tbody></table>'
 header='<header class="uh"><div class="crumb">'+('地球科學' if u['subject']=='earth' else '生物')+'｜'+u['source']+'｜原圖與講解</div><h1><span class="uid">'+u['id']+'</span>'+E(u['title'])+'</h1><p>'+E(u['lead'])+'</p><div class="tools"><span class="cnt">3個觀念 · 6題隨堂練習 · 原頁對照</span><button id="openAll">展開六題詳解</button><button id="closeAll">收起詳解</button></div></header>'
 toc='<nav class="inline-toc" aria-label="本頁內容">'+''.join('<a href="#learn-'+str(i+1)+'">'+E(s['title'])+'</a>' for i,s in enumerate(u['sections']))+'<a href="#original-pages">本節原頁與原題</a></nav>'
 pager=re.search(r'<div class="pager">.*?</div>',t,re.S).group()
 main='<main class="main">'+header+toc+'<div class="content source-handout">'+''.join(parts)+rows+fullpages(u)+'</div>'+pager+'</main>'
 t=re.sub(r'<main\b.*?</main>',lambda _:main,t,count=1,flags=re.S)
 p.write_text(t,encoding='utf-8')
# Remove the large added front-matter cards from original pages: their original flow was already accepted.
for subject in ('earth','biology'):
 for p in (ROOT/subject).glob('*.html'):
  t=p.read_text(encoding='utf-8');t=re.sub(r'<!-- reading-guide START -->.*?<!-- reading-guide END -->','',t,flags=re.S);p.write_text(t,encoding='utf-8')
import runpy
module=runpy.run_path(str(ROOT/'_src/integrate_navigation.py'));module['integrate']()
print('Rebuilt 16 source-image handouts; integrated 180 subsequent source pages and all chapter cards.')

# Individually authored overrides always win over the initial bulk drafts.
runpy.run_path(str(ROOT/"_src/build_biology_3_1.py"))["build"]()

# Carefully authored, one-unit overrides. Render no other content here.
import sys
sys.path.insert(0,str(ROOT/"_src"))
from individual_unit import build as build_individual
build_individual("earth-4-1")
build_individual("biology-3-2")
build_individual("earth-4-2")
build_individual("biology-3-3")
build_individual("earth-4-3")
build_individual("earth-4-4")
build_individual("earth-4-綜")
build_individual("biology-3-4")
build_individual("biology-3-5")
build_individual("biology-4-1")
build_individual("biology-4-2")
build_individual("biology-4-3")
build_individual("biology-4-4")
build_individual("biology-4-5")
