"""Independent scientific checks: enumerate allele contributions, not page-renderer answers."""
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

def cross(mother,father):
 # Each parental tuple contains the two alleles at each locus.
 mg=list(product(*mother));fg=list(product(*father))
 counts=Counter(tuple(tuple(sorted([x,y])) for x,y in zip(a,b)) for a,b in product(mg,fg))
 total=len(mg)*len(fg)
 return {g:F(n,total) for g,n in counts.items()}

def phenotype(g,second_incomplete=False):
 color='red' if 'HA' in g[0] else 'yellow' if 'Ha' in g[0] else 'white'
 return color,('tall' if 'B' in g[1] else 'short')

m=(('HA','Ha'),('B','b'))
test=cross(m,(('h','h'),('b','b')))
assert len(test)==4 and len({phenotype(g) for g in test})==4 and set(test.values())=={F(1,4)}
flowers=cross(m,(('Ha','h'),('B','b')))
phenos=Counter()
for g,p in flowers.items():phenos[phenotype(g)]+=p
assert len(flowers)==12 and len(phenos)==4 and phenos['yellow','tall']==F(3,8)
di=cross((('A','a'),('B','b')),(('A','a'),('B','b')))
assert len(di)==9
p11={(('A' in g[0]),g[1]) for g in di}
assert len(p11)==6
p12=sum(p for g,p in di.items() if ('A' in g[0])!=('B' in g[1]))
assert p12==F(3,8)
pigment=Counter()
for g,p in di.items():pigment[sum(a.isupper() for locus in g for a in locus)]+=p
assert [pigment[n] for n in range(5)]==[F(1,16),F(4,16),F(6,16),F(4,16),F(1,16)]
incomplete=cross((('R','W'),),(('R','W'),))
assert sorted(incomplete.values())==[F(1,4),F(1,4),F(1,2)]
abo=cross((('A','i'),),(('B','i'),))
assert len(abo)==4 and set(abo.values())=={F(1,4)}
abo2=cross((('A','B'),),(('i','i'),))
assert set(abo2)=={(('A','i'),),(('B','i'),)}
cards=cross((('T','t'),),(('t','t'),))
assert set(cards.values())=={F(1,2)}
assert round((1013-250)/10,1)==76.3 and (70-20)/10==5
mass=(F(1013)-F(250))/F(1013)
assert F(74,100)<mass<F(76,100)
report={'flower_testcross':{'genotypes':len(test),'phenotypes':4,'probability_each':'1/4'},'flower_cross':{'genotypes':len(flowers),'phenotypes':len(phenos),'yellow_tall':str(phenos['yellow','tall'])},'two_loci':{'genotypes':len(di),'one_incomplete_phenotypes':len(p11),'one_dominant_one_recessive':str(p12)},'pigment_counts_out_of_16':[int(pigment[n]*16) for n in range(5)],'ABO_cross':'4 types each 1/4; AB x O gives A/B only','card_model':'2 genotypes each 1/2','pressure_drop_hPa_per_km':[76.3,5],'mass_below_10km_percent':round(float(mass)*100,2),'errors':[]}
dest=Path(__file__).resolve().parent/'units/pair-numeric-review.json'
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
