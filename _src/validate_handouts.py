from pathlib import Path
import re,json,subprocess,hashlib
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parent.parent
errors=[]; report={'new_units':0,'new_checks':0,'original_questions_preserved':0,'pages_checked':0,'source_pages':0,'errors':errors}
units=json.loads((ROOT/'_src/continuation.json').read_text(encoding='utf-8'))
for u in units:
 p=ROOT/u['subject']/('u'+u['id']+'.html');t=p.read_text(encoding='utf-8')
 report['new_units']+=1
 n=len(re.findall('class="sol micro-check"',t));report['new_checks']+=n
 if n!=6:errors.append(f'{p.name}: check count {n}')
 if len(re.findall('class="on"',t))!=1:errors.append(str(p)+': current nav')
for subject in ('earth','biology'):
 for p in (ROOT/subject).glob('*.html'):
  t=p.read_text(encoding='utf-8');report['pages_checked']+=1
  ids=re.findall(r'\bid="([^"]+)"',t)
  if len(ids)!=len(set(ids)):errors.append(str(p)+': duplicate IDs')
  for tag,v in re.findall(r'\b(href|src)="([^"]+)"',t):
   if v.startswith(('http','data:','mailto:','javascript:')):continue
   url=urlsplit(v);dest=p.parent/unquote(url.path) if url.path else p
   if url.path and not dest.exists():errors.append(str(p)+': missing '+v)
   if url.fragment and not url.fragment.startswith('book=') and dest.suffix=='.html' and dest.exists():
    if not re.search(r'\bid="'+re.escape(unquote(url.fragment))+'"',dest.read_text(encoding='utf-8')):errors.append(str(p)+': missing anchor '+v)
  rel=p.relative_to(ROOT).as_posix()
  r=subprocess.run(['git','show','HEAD:'+rel],cwd=ROOT,capture_output=True)
  if r.returncode==0:
   before=r.stdout.decode('utf-8').replace('\r\n','\n')
   qs=lambda s:re.findall(r'<article class="q\b.*?</article>',s,re.S)
   if qs(before)!=qs(t) and rel not in {'biology/u3-1.html','earth/u4-1.html','biology/u3-2.html'}:errors.append(rel+': existing questions changed')
   if rel not in {'biology/u3-1.html','earth/u4-1.html','biology/u3-2.html'}:report['original_questions_preserved']+=len(qs(before))
raw=(ROOT/'source-pages.js').read_text(encoding='utf-8')
books=json.loads(raw.removeprefix('window.SOURCE_BOOKS=').removesuffix(';'))
for b in books:
 if [p['page'] for p in b['pages']]!=list(range(1,b['total']+1)):errors.append(b['id']+': discontinuous pages')
 for p in b['pages']:
  if not (ROOT/p['image']).exists():errors.append(p['image']+': missing')
  if not (ROOT/p['lesson']).exists():errors.append(p['lesson']+': missing')
  if not p['text'].strip():errors.append(b['id']+str(p['page'])+': empty OCR')
 report['source_pages']+=b['total']
assert report['source_pages']==366
(ROOT/'_src/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(bool(errors))
