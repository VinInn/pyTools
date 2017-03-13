
# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
import math
d = {}
files = []
files.append('simperfHSW6.log')



def parseCounts(fname):
    d = {}
    with open(fname) as f:
        for line in f:
            a = line.split()
            if len(a)>2 :
                (val, key, hash) = a[0:3]
                # print val, key
                if hash == '#' :
                   d[key] = float(val)
    norm = math.pow(10.,-int(math.log10(d['cycles'])-4))
    for k,v, in d.iteritems() :
        d[k] = v*norm
    return d

print '| | Hashwell ||||| IvyBridge |||||'
print '| | !CMS tkreco 6 | !CMS sim 6 | !CMS sim 1 | !HSPEC 6 |!HSPEC 1 | !CMS tkreco 6 | !CMS sim 6 | !CMS sim 1 | !HSPEC 6 |!HSPEC 1 ||'  
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

