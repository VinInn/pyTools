import json
j1 = json.load(open('singleMu23_2017F.json'))
c = j1['hist']['bins']['content']
k=0
q=0
for i in xrange(1,3565) :
      k+= c[i]-c[i-1]
      q+=c[i]
 
print q, k, float(k)/float(q)

j2 = json.load(open('singleMu23_2018B.json'))
a2 = np.array(j2['hist']['bins']['content'])
np.ediff1d((a2[a2>10000])))
