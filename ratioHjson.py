import json
c = json.loads(open('L1_SingleMu25_278957').read())['hist']['bins']['content']

all=0
nall=0
ffb=0
fb=0
nfb=0
lb=0;
nlb=0
for i in range(0, 3490): 
  if (c[i]) >1000 :
    ffb+=c[i]
    break

for i in range(0, 3500): 
  if (c[i]) >1000 :
    all+=c[i]
    nall+=1

for i in range(0, 3499):
  if c[i] >1000 and c[i+1]<1000 :
    nlb+=1
    lb+=c[i]
  if c[i] < 1000 and c[i+1]>1000 :
    nfb+=1
    fb+=c[i+1]


print nall,nlb,nfb
la = all/float(nall)
print all/float(nall), ffb, fb/float(nfb),lb/float(nlb)
print ffb/la, fb/float(nfb)/la,lb/float(nlb)/la

