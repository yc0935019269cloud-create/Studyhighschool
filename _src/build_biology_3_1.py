"""Individually maintained Mendelian-inheritance handout, following the original biology units."""
from pathlib import Path
from PIL import Image
import json,re,html
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'_src/units'
FIGURES={
'experiment':(87,(19,29,85,72),'孟德爾七組豌豆雜交實驗：F₁與F₂的觀察結果'),
'mono':(88,(37,9.0,79,31),'高莖、矮莖的單性雜交：從親代到F₂'),
'di':(88,(54,44.3,91,79),'兩對因子雜交：四種配子與十六種受精組合'),
'probability':(89,(15,38,85,60),'四個豚鼠子代的排列數與機率')
}
def figure(key):
 page,box,caption=FIGURES[key]
 src=ROOT/'source-pages/生物1'/(str(page).zfill(3)+'.webp')
 im=Image.open(src);w,h=im.size;x0,y0,x1,y1=box
 crop=im.crop((round(w*x0/100),round(h*y0/100),round(w*x1/100),round(h*y1/100)))
 dest=ROOT/'biology/img'/('mendel_'+key+'.webp');crop.save(dest,'WEBP',quality=90,method=4)
 return '<figure class="fig mendel-figure mfigure-'+key+'"><img class="figimg" src="img/'+dest.name+'" width="'+str(crop.width)+'" height="'+str(crop.height)+'" loading="lazy" alt="'+caption+'" data-page="生物1 PDF第'+str(page)+'頁"><figcaption>'+caption+'<span>原講義PDF第'+str(page)+'頁・印刷第'+str(page+2)+'頁・點圖放大</span></figcaption></figure>'
def question(q):
 return '<article class="q q-pr" id="check-'+str(q['n'])+'"><header class="qh"><span class="qn">隨堂練習 '+str(q['n'])+'</span><span class="qtag">'+q['tag']+'</span><button class="mark" type="button" title="標記不會" aria-label="標記練習'+str(q['n'])+'">☆</button></header><div class="qtext">'+q['q']+'</div><details class="sol micro-check"><summary><span class="sum-show">看答案與詳解</span><span class="sum-hide">收起</span></summary><div class="ans"><b>答</b>'+q['ans']+'</div><div class="exp"><b class="exp-h">解</b>'+q['exp']+'<div class="qsum"><span class="qsum-h">小結</span><p>'+q['sum']+'</p></div></div></details></article>'
def build():
 # Use Claude's established page as the shell, including its original typography, boxes and controls.
 shell=(ROOT/'biology/u1-5.html').read_text(encoding='utf-8')
 shell=re.sub(r'<!-- handout-assets START -->.*?<!-- handout-assets END -->','',shell,flags=re.S)
 shell=re.sub(r'<ul class="subtoc">.*?</ul>','',shell,flags=re.S)
 shell=shell.replace(' class="on"','')
 shell=shell.replace('<a href="u3-1.html"><span>','<a class="on" href="u3-1.html"><span>',1)
 titles=['先分清楚：性狀與基因型','孟德爾的實驗觀察','分離律與配子','1：2：1與3：1','試交與交配名稱','兩對因子與獨立分配','機率：且、或與已知','四個子代的排列','本單元整理']
 toc='<ul class="subtoc">'+''.join('<li><a href="#s'+str(i+1)+'">'+title+'</a></li>' for i,title in enumerate(titles))+'</ul>'
 shell=shell.replace('<a class="on" href="u3-1.html"><span>3-1</span>孟德爾遺傳：配子與子代機率</a></li>','<a class="on" href="u3-1.html"><span>3-1</span>孟德爾遺傳：配子與子代機率</a>'+toc+'</li>',1)
 body=(SRC/'biology-3-1.html').read_text(encoding='utf-8')
 for key in FIGURES:body=body.replace('{{FIG_'+key+'}}',figure(key))
 for q in json.loads((SRC/'biology-3-1.questions.json').read_text(encoding='utf-8')):body=body.replace('{{Q'+str(q['n'])+'}}',question(q))
 assert '{{' not in body
 main='<main class="main"><header class="uh"><div class="crumb">第3單元 遺傳學</div><h1><span class="uid">3-1</span>孟德爾遺傳：配子與子代機率</h1><div class="tools"><span class="cnt">本單元 6 題</span><button id="openAll">全部展開答案</button><button id="closeAll">全部收起</button><button id="onlyMarked">只看☆標記題</button></div></header><div class="content mendel-unit">'+body+'</div><div class="pager"><a href="u2-5.html">← 2-5 能量單元練習</a><a href="u3-2.html">3-2 顯性關係的延伸 →</a></div></main>'
 shell=re.sub(r'<main\b.*?</main>',lambda _:main,shell,count=1,flags=re.S)
 shell=re.sub(r'<title>.*?</title>','<title>3-1 孟德爾遺傳：配子與子代機率｜生物</title>',shell,count=1)
 css=(SRC/'biology-3-1.css').read_text(encoding='utf-8')
 shell=shell.replace('</head>','<link rel="icon" href="../favicon.svg" type="image/svg+xml"><style id="mendel-specific">'+css+'</style></head>')
 (ROOT/'biology/u3-1.html').write_text(shell,encoding='utf-8')
 print('biology/3-1: 9 sections; 6 worked questions; 4 source figures. Other unit files unchanged.')
if __name__=='__main__':build()
