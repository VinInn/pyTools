d = {}
ori= 'hltPerf_ori.txt'
pgo = 'hltPerf_pgo.txt'
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
  print '|',k,'| ',"{:15.0f}".format(c[0]),'| ',"{:15.0f}".format(c[1]),'| ', "{:6.2f}".format(100*(c[0]-c[1])/c[0]),'||'
