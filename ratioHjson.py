import json
c = json.loads(open('L1_SingleMu25.htm').read())['hist']['bins']['content']

k1=0
n1=0;
for i in range(0, 150): 
  if (c[i]) >10000 :
    k1+=c[i]
    n1+=1

k2=0
n2=0;
for i in range(2000, 3500): 
  if (c[i]) >10000 :
    k2+=c[i]
    n2+=1

r1 = float(k1)/float(n1)
r2 = float(k2)/float(n2)

print r1,r2

