d = {}
ori= 'tk140reco900.txt'
pgo = 'tk200reco900.txt'
with open(ori) as f:
    for line in f:
       (val, key) = line.split()
       if not key in d : d[key] = [0.,0.]
       d[key][0] = float(val)

with open(pgo) as f:
    for line in f:
       (val, key) = line.split()
       if not key in d : d[key] = [0.,0.]
       d[key][1] = float(val)

# print d
for k,c in d.iteritems() :
  if(c[0]>0) :
    print "{:10.7f}".format(c[0]),'|',k,'| ',"{:6.4f}".format(c[0]),'| ',"{:6.4f}".format(c[1]),'| ', "{:6.2f}".format((c[1])/c[0]),'||'


#for k,c in d.iteritems() :
#  if(c[0]>0.001) :
#    print "{:6.2f}".format(100*(c[0]-c[1])/c[0]),'|',k,'| ',"{:6.4f}".format(c[0]),'| ',"{:6.4f}".format(c[1]),'| ', "{:6.2f}".format(100*(c[0]-c[1])/c[0]),'||'

