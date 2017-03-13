
# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
import math
d = {}
files = []
files.append('seedTripESKL.log')
files.append('seedCASKL.log')
ref = 'seedNoSKL.log'


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
    return d

def norm(d) :
    return math.pow(10.,-int(math.log10(d['cycles'])-4))

def normalize(d, norm) :
    for k,v, in d.iteritems() :
        d[k] = v*norm

def printAbs(d) :
    n = norm(d[0])
    for v in d :
        normalize(v,n)
        
    for k,c in d[0].iteritems() :
        s = '|' + k 
        for v in d :
            if not k in v : v[k] = 0.
            s+= ' | ' + "{:6.4f}".format(v[k])
        s += ' ||'
        print s

def printRel(d) :
    print '| | relative |||'
    n = norm(d[0])
    for v in d :
        n = 1./v['cycles']
        normalize(v,n)
        
    for k,c in d[0].iteritems() :
        s = '|' + k 
        for v in d :
            if not k in v : v[k] = 0.
            s+= ' | ' + "{:6.4f}".format(v[k])
        s += ' ||'
        print s


#print '| | Hashwell ||||| IvyBridge |||||'
print '| | !TriplExt | !CA ||'
d =[]
for f in files:
    d.append(parseCounts(f))

refd = parseCounts(ref)

for k,c in refd.iteritems() :
    for v in d:
        if not k in v : v[k] = 0.
        v[k]-=c


# printAbs(d)

printRel(d)

