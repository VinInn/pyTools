# grep -A35 "CPUs utilized" tkhl8.log | awk '{print $1,$2}'
#grep -A1 "CPUs utilized" tkhl8.log | awk '{print $4,$5,$6}'

d = {}
files = ['i7_tkhl4.txt', 'i7_tkhl8.txt',\
'gold_tkhl4.txt',   'gold_tkhl8.txt',  'gold_tkhl4p4.txt',\
'silver_tkhl4.txt',  'silver_tkhl8.txt', 'silver_tkhl4p4.txt'\
]

def parseCounts(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            (val, key) = line.split()
            d[key] = float(val) if float(val)<1000000. else float(val)/float(1000000)
    return d


def parseCountsNC(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            (val, key) = line.split()
            d[key] = float(val)
    cycles = d['cycles']
    for k,v, in d.iteritems() :
        d[k] = v/cycles
    return d

def parseCountsNI(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            (val, key) = line.split()
            d[key] = float(val)
    cycles = d['instructions']
    for k,v, in d.iteritems() :
        d[k] = v/cycles
    return d


print '| | i7-6700K ||| Gold 5122 |||| Silver 4110 ||'
print '| threads | 4 | 8 | 4 | 8 | 2+2 | 4 | 8 | 4+4 ||'  
# print d
d =[]
for f in files:
    d.append(parseCounts(f))

for k,c in d[0].iteritems() :
    s = '|' + k + ' |'
    for v in d :
        if not k in v : v[k] = 0.
        s+= '  '
        s+= "{:6.3f}".format(v[k]) if v[k]<1000 else "{:6.0f}".format(v[k])
        s+= '|'
    s += '|'
    print s

