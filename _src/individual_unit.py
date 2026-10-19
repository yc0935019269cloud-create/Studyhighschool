"""Render one individually authored handout in its subject's established Claude shell.
No content is taken from the bulk draft. Main text, questions and crops are reviewed per unit.
"""
from pathlib import Path
from PIL import Image
import re,json,html
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'_src/units'

def build(key):
 c=json.loads((SRC/(key+'.json')).read_text(encoding='utf-8'))
 subject=c['subject'];uid=c['id'];target='u'+uid+'.html'
 shell=(ROOT/subject/c['shell']).read_text(encoding='utf-8')
 shell=re.sub(r'<!-- handout-assets START -->.*?<!-- handout-assets END -->','',shell,flags=re.S)
 shell=re.sub(r'<ul class="subtoc">.*?</ul>','',shell,flags=re.S).replace(' class="on"','')
 toc='<ul class="subtoc">'+''.join('<li><a href="#s'+str(i+1)+'">'+v+'</a></li>' for i,v in enumerate(c['sections']))+'</ul>'
 pat=r'<a href="'+re.escape(target)+r'"><span>.*?</a>'
 def current(m):return m[0].replace('<a ','<a class="on" ',1)+toc
 shell,n=re.subn(pat,current,shell,count=1,flags=re.S);assert n==1,'sidebar target missing'
 body=(SRC/(key+'.html')).read_text(encoding='utf-8')
 for f in c['figures']:
  im=Image.open(ROOT/'source-pages'/c['source']/(str(f['page']).zfill(3)+'.webp'));w,h=im.size
  box=[round(v*(w if i%2==0 else h)/100) for i,v in enumerate(f['crop'])]
  crop=im.crop(box);dest=ROOT/subject/'img'/(key+'-'+f['key']+'.webp')
  crop.save(dest,'WEBP',quality=91,method=4)
  figure='<figure class="fig authored-figure fig-'+f['key']+'"><img class="figimg" src="img/'+dest.name+'" width="'+str(crop.width)+'" height="'+str(crop.height)+'" loading="lazy" alt="'+html.escape(f['caption'],quote=True)+'" data-page="'+c['source']+' PDF第'+str(f['page'])+'頁"><figcaption>'+f['caption']+'<span>原講義PDF第'+str(f['page'])+'頁・印刷第'+str(f['page']+c['offset'])+'頁・點圖放大</span></figcaption></figure>'
  body=body.replace('{{FIG_'+f['key']+'}}',figure)
 qs=json.loads((SRC/(key+'.questions.json')).read_text(encoding='utf-8'))
 for q in qs:
  ph='{{Q'+str(q['n'])+'}}'
  assert ph in body,'question placeholder missing from body: '+ph
  # Optional figure crops from the source page, shown under the typed question text.
  qfigs=''
  for i,f in enumerate(q.get('figs',[])):
   im=Image.open(ROOT/'source-pages'/c['source']/(str(f['page']).zfill(3)+'.webp'));w,h=im.size
   box=[round(v*(w if j%2==0 else h)/100) for j,v in enumerate(f['crop'])]
   crop=im.crop(box);dest=ROOT/subject/'img'/(key+'-q'+str(q['n'])+'-'+str(i+1)+'.webp')
   crop.save(dest,'WEBP',quality=91,method=4)
   qfigs+='<img class="qimg" src="img/'+dest.name+'" width="'+str(crop.width)+'" height="'+str(crop.height)+'" loading="lazy" alt="題目附圖" data-page="'+c['source']+' PDF第'+str(f['page'])+'頁">'
  if qfigs:qfigs='<div class="qimgs">'+qfigs+'</div>'
  qtext=q['q']
  if '{{FIG}}' in qtext:qtext,qfigs=qtext.replace('{{FIG}}',qfigs),''
  label=q.get('label','練習 '+str(q['n']))
  card='<article class="q q-pr" id="check-'+str(q['n'])+'"><header class="qh"><span class="qn">'+label+'</span><span class="qtag">'+q['tag']+'</span><button class="mark" type="button" title="標記不會" aria-label="標記'+label+'">☆</button></header><div class="qtext">'+qtext+'</div>'+qfigs+'<details class="sol micro-check"><summary><span class="sum-show">看答案與詳解</span><span class="sum-hide">收起</span></summary><div class="ans"><b>答</b>'+q['ans']+'</div><div class="exp"><b class="exp-h">解</b>'+q['exp']+'<div class="qsum"><span class="qsum-h">小結</span><p>'+q['sum']+'</p></div></div></details></article>'
  body=body.replace(ph,card)
 pages=''.join('<figure class="fig original-page"><img class="figimg" loading="lazy" src="../source-pages/'+c['source']+'/'+str(p).zfill(3)+'.webp" alt="'+c['source']+'PDF第'+str(p)+'頁完整原稿"><figcaption>PDF第'+str(p)+'頁／印刷第'+str(p+c['offset'])+'頁</figcaption></figure>' for p in c['pages'])
 body=body.replace('{{ORIGINALS}}','<details class="source-originals"><summary>核對原講義全頁（'+c['source']+' PDF'+str(c['pages'][0])+'–'+str(c['pages'][-1])+'）</summary><p class="fine-note">'+c['source_note']+'</p>'+pages+'</details>')
 assert '{{' not in body
 main='<main class="main"><header class="uh"><div class="crumb">'+c['chapter']+'</div><h1><span class="uid">'+uid+'</span>'+c['title']+'</h1><div class="tools"><span class="cnt">'+c['count_label']+'</span><button id="openAll">全部展開答案</button><button id="closeAll">全部收起</button><button id="onlyMarked">只看☆標記題</button></div></header><div class="content authored-unit">'+body+'</div><div class="pager"><a href="'+c['prev'][0]+'">← '+c['prev'][1]+'</a><a href="'+c['next'][0]+'">'+c['next'][1]+' →</a></div></main>'
 shell=re.sub(r'<main\b.*?</main>',lambda _:main,shell,count=1,flags=re.S)
 shell=re.sub(r'<title>.*?</title>','<title>'+uid+' '+c['title']+'｜'+c['subject_label']+'</title>',shell,count=1)
 css=(SRC/'individual-unit.css').read_text(encoding='utf-8')
 shell=re.sub(r'<style id="individual-unit">.*?</style>','',shell,flags=re.S)
 shell=shell.replace('</head>','<link rel="icon" href="../favicon.svg" type="image/svg+xml"><style id="individual-unit">'+css+'</style></head>')
 (ROOT/subject/target).write_text(shell,encoding='utf-8')
 print(key+': '+str(len(c['sections']))+' sections; '+str(len(qs))+' worked groups; '+str(len(c['figures']))+' source crops')
