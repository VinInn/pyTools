
# grep -A29 "CPUs utilized" scimark2BW.log | awk '{print $1,$2}' | sed 's/,//g' | sed 's/.//g'

fname = "perfDb12hssimtk.counts"

def parseCountsNC(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            if len(line)<10 : continue
            (val, key) = line.split()
            if not key in d : d[key] = []
            d[key].append(float(val))
    cycles = d['cycles'][:]
    s = len(cycles)
    for k,v, in d.iteritems() :
       for i in range(s) :
         d[k][i] = v[i]/cycles[i]
    return d

def parseCountsNI(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            if len(line)<10 : continue
            (val, key) = line.split()
            if not key in d : d[key] = []
            d[key].append(float(val))
    cycles = d['instructions'][:]
    s = len(cycles)
    for k,v, in d.iteritems() :
       for i in range(s) :
         d[k][i] = v[i]/cycles[i]
    return d


# print '| | Hashwell ||||| IvyBridge |||||'
# print '| | !CMS tkreco 6 | !CMS sim 6 | !CMS sim 1 | !HSPEC 6 |!HSPEC 1 | !CMS tkreco 6 | !CMS sim 6 | !CMS sim 1 | !HSPEC 6 |!HSPEC 1 ||'  
# print d

dd = [parseCountsNC(fname),parseCountsNI(fname)]

for d in dd :
  for k in sorted(d.iterkeys()) :
    c = d[k]
    s = '|' + k + ' |'
    for v in c :
        s+= '  '+"{:6.4f}".format(v)  + '|'
    s += '|'
    print s
  print ' '
