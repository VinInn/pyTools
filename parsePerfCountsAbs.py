
# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
# grep -A29 "CPUs utilized" scimark2BW.log

d = {}
files = []
files.append('tkperfHSW.counts')
files.append('simperfHSW6.counts')
files.append('simperfHSW.counts')
files.append('perfHWS6.counts')
files.append('perfHWS.counts')

files.append('tkperfIVB.counts')
files.append('simperfIVB6.counts')
files.append('simperfIVB.counts')
files.append('perfIV6.counts')
files.append('perfIV.counts')

def parseCounts(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            (val, key) = line.split()
            d[key] = float(val)
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
print '| freq    ||'   
print '| threads | 4 | 8 | 4 | 8 | 2+2 | 4 | 8 | 4+4 ||'  
# print d
d =[]
for f in files:
    d.append(parseCounts(f))

for k,c in d[0].iteritems() :
    s = '|' + k + ' | '
    for v in d :
        if not k in v : v[k] = 0.
        s+= "{:6.4f}".format(v[k])  + ' |'
    s += '|'
    print s

