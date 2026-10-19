"""Export every supplied PDF page; verify page coverage before writing the catalog."""
from pathlib import Path
import fitz,re,json,csv,hashlib
ROOT=Path(__file__).resolve().parent.parent
BASE=Path('E:/家教備課/男生')
SPECS=[
 ('earth','地科','地科1',[(1,18,'地球的歷史','u1-1.html'),(19,72,'天文','u2-3.html'),(73,102,'地質與板塊','u3-1.html')]),
 ('earth','地科','地科2',[(1,5,'大氣溫壓與分層','u4-1.html'),(6,12,'水氣與雲雨','u4-2.html'),(13,18,'風與氣壓','u4-3.html'),(19,34,'天氣圖與天氣題組','u4-4.html'),(35,45,'海水性質與波浪','u5-1.html'),(46,51,'海流與湧升流','u5-2.html'),(52,57,'潮汐','u5-3.html'),(58,74,'海洋綜合練習與歷屆題','u5-2.html'),(75,102,'天然災害與練習','u6-1.html')]),
 ('earth','地科','地科3',[(1,6,'古氣候、機制與證據','u7-1.html'),(7,30,'氣候、資源與綜合題','u7-2.html'),(31,56,'進階探究與整合圖表','u8-1.html')]),
 ('biology','生物','生物1',[(1,11,'生命現象與基本物質','u1-1.html'),(12,16,'酵素','u1-3.html'),(17,26,'細胞構造','u1-4.html'),(27,30,'膜與運輸','u1-5.html'),(31,38,'細胞分裂與分化','u1-6.html'),(39,44,'細胞學實驗','u1-7.html'),(45,55,'細胞學綜合題','u1-8.html'),(56,64,'光合作用','u2-1.html'),(65,70,'呼吸與能量','u2-2.html'),(71,75,'能量實驗','u2-4.html'),(76,84,'能量綜合練習','u2-5.html'),(85,88,'孟德爾遺傳','u3-1.html'),(89,93,'顯性、血型與環境','u3-2.html'),(94,96,'染色體與核型','u3-3.html'),(97,98,'性聯遺傳','u3-4.html'),(99,106,'連鎖、互換與遺傳綜合題','u3-5.html')])
]
data=[]; coverage=[]
for subject,folder,book,ranges in SPECS:
 pdf=BASE/folder/'講義'/(book+'.pdf'); md=pdf.with_suffix('.md')
 doc=fitz.open(pdf); text=md.read_text(encoding='utf-8')
 chunks=re.split(r'## 第 (\d+) 頁',text)
 ocr={int(chunks[i]):chunks[i+1].strip() for i in range(1,len(chunks),2)}
 assert set(ocr)==set(range(1,len(doc)+1)),book+' OCR page mismatch'
 pages=[]; out=ROOT/'source-pages'/book;out.mkdir(parents=True,exist_ok=True)
 for i,p in enumerate(doc,1):
  group=[r for r in ranges if r[0]<=i<=r[1]]
  assert len(group)==1,(book,i)
  group=group[0]; dest=out/(str(i).zfill(3)+'.webp')
  if not dest.exists():
   pix=p.get_pixmap(matrix=fitz.Matrix(1600/p.rect.width,1600/p.rect.width))
   from PIL import Image
   im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
   im.save(dest,'WEBP',quality=84,method=4)
  assert dest.stat().st_size>1000
  item={'page':i,'topic':group[2],'lesson':subject+'/'+group[3],'image':dest.relative_to(ROOT).as_posix(),'text':ocr[i]}
  pages.append(item);coverage.append([book,i,group[2],item['lesson'],item['image'],'included'])
 data.append({'id':book,'subject':subject,'total':len(doc),'source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':pages})
 print(book,len(doc),'complete',flush=True)
(ROOT/'source-pages.js').write_text('window.SOURCE_BOOKS='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
with (ROOT/'_src/source-coverage.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['book','PDF_page','topic','lesson','image','status']);w.writerows(coverage)
print('ALL',len(coverage),'pages')
