from pathlib import Path
import re,json,html
ROOT=Path(__file__).resolve().parent.parent
UNITS=json.loads((ROOT/'_src/continuation.json').read_text(encoding='utf-8'))
TITLES={'biology':{'3':'遺傳學'},'earth':{'4':'大氣與天氣','5':'海洋','6':'天然災害','7':'氣候變遷與資源','8':'進階探究'}}
def strip(t,n):return re.sub(r'<!-- '+n+r' START -->.*?<!-- '+n+r' END -->','',t,flags=re.S)
def marked(n,s):return '<!-- '+n+' START -->'+s+'<!-- '+n+' END -->'
def groups(subject):
 return [(key,title,[u for u in UNITS if u['subject']==subject and u['id'].split('-')[0]==key]) for key,title in TITLES[subject].items()]
def home_groups(subject):
 out=''
 for n,title,us in groups(subject):
  out+='<details><summary>第'+n+'單元　'+title+'<em>'+str(len(us))+'</em></summary><ul>'+''.join('<li><a href="'+subject+'/u'+u['id']+'.html"><span>'+u['id']+'</span>'+html.escape(u['title'])+'</a></li>' for u in us)+'</ul></details>'
 book='地科1' if subject=='earth' else '生物1'
 return out+'<p class="card-source-link"><a href="sources.html#book='+book+'&page=1">完整原講義與逐頁對照 →</a></p>'
def integrate_home(t):
 t=strip(strip(t,'continuation-home'),'integrated-home')
 for subject in TITLES:
  pattern=r'<section class="card"[^>]*>\s*<a class="head" href="'+subject+r'/index.html">.*?</section>'
  def repl(m):
   card=m[0];return re.sub(r'</div></section>\s*$',lambda _:marked('integrated-home',home_groups(subject))+'</div></section>',card)
  t,n=re.subn(pattern,repl,t,flags=re.S)
  assert n==1,(subject,'root card missing')
 return t
def integrate():
 for subject in TITLES:
  for p in (ROOT/subject).glob('*.html'):
   t=p.read_text(encoding='utf-8')
   for n in ('continuation-nav','integrated-nav','integrated-index'):t=strip(t,n)
   if p.name=='index.html':t=strip(t,'continuation-index')
   nav=''
   for n,title,us in groups(subject):
    nav+='<div class="nch">第'+n+'單元　'+title+'</div><ul>'+''.join('<li><a'+(' class="on"' if p.name=='u'+u['id']+'.html' else '')+' href="u'+u['id']+'.html"><span>'+u['id']+'</span>'+html.escape(u['title'])+'</a></li>' for u in us)+'</ul>'
   nav+='<p class="source-note"><a href="../sources.html#book='+('地科1' if subject=='earth' else '生物1')+'&page=1">完整原講義逐頁對照</a></p>'
   t=re.sub(r'(<nav class="side"[^>]*>.*?)(</nav>)',lambda m:m[1]+marked('integrated-nav',nav)+m[2],t,count=1,flags=re.S)
   if p.name=='index.html':
    cards=''
    for n,title,us in groups(subject):
     cards+='<section class="chcard"><h2>第'+n+'單元<br><span>'+title+'</span></h2><ul>'+''.join('<li><a href="u'+u['id']+'.html"><b>'+u['id']+'</b> '+html.escape(u['title'])+'<em>6 題</em></a></li>' for u in us)+'</ul></section>'
    t=re.sub(r'(<div class="chgrid">.*?)(</div>)',lambda m:m[1]+marked('integrated-index',cards)+m[2],t,count=1,flags=re.S)
    if subject=='biology':t=t.replace('共 18 個單元、254 題。','共 23 份講義，原有254題與新增30題概念檢核。')
    else:t=t.replace('地科 1：地球的歷史・天文・地質','地科 1–3：歷史・天文・地質・大氣・海洋・氣候')
   p.write_text(t,encoding='utf-8')
 p=ROOT/'index.html';p.write_text(integrate_home(p.read_text(encoding='utf-8')),encoding='utf-8')
if __name__=='__main__':integrate()
