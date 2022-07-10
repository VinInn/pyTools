# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
#grep -A29 "CPUs utilized" scimark2BW.log


def parseCountsNorm(di,denName):
    do = {}
    for wf in di :
      den = di[wf][denName]
      for k in di[wf] :
        if not k in do : do[k] = {}
        do[k][wf] = di[wf][k]/den
    return do


def doPrint(di) :
  s = '\n|' + ' | '
  for wf  in di['cycles'] :
    s+= ' ' + wf + ' |'
  s += '|'
  print(s)
  for k in di :
    s = '|' + k + ' | '
    for wf  in di[k] :
        v = di[k][wf]
        s+= ' ' + "{:6.4f}".format(v)  + ' | '
    s += '|'
    print(s)


def parseOne(fname) :

  d ={}
  with open(fname) as f:
    for line in f:
      try:
        (wf, val, key) = line.split()
        d[wf] = {}
      except:
        print("")      
  with open(fname) as f:
    for line in f:
      try:
        (wf, val, key) = line.split()
        d[wf][key]= float(val)
      except:
        print("")
#
  dc = parseCountsNorm(d,'cycles')
  di = parseCountsNorm(d,'instructions')
  ds = parseCountsNorm(d,'seconds')
#
  doPrint(dc)
  doPrint(di)
  doPrint(ds)


files = ["haswell.count","icelake.count","skylake.count"]

for f in files:
  parseOne(f)

