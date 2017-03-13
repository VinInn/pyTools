
# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
d = {}
files = []
files.append('tkperfHSW.counts')
files.append('perfHWS6.counts')
files.append('perfHWS.counts')


def parseCounts(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            (val, key) = line.split()
            d[key] = float(val)
    cycles = d['cycles']
    for k,v, in d.iteritems() :
        d[k] = v/cycles
    return d

print '| | !CMS 6 | !HSPEC 6 |!HSPEC 1 ||'  
# print d
d =[]
for f in files:
    d.append(parseCounts(f))

for k,c in d[0].iteritems() :
    s = '|' + k + ' | '
    for v in d :
        s+= "{:6.4f}".format(v[k])  + ' |'
    s += '|'
    print s

