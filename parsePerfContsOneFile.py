# grep -A20 "CPUs utilized" perfHWS6.log | awk '{print $1,$2}'
#grep -A29 "CPUs utilized" scimark2BW.log


def parseCountsNorm(di,denName):
    do = {}
    for wf in di :
      den = di[wf][denName]
      if (denName=='seconds') : den*=1000.*1000.*1000.
      for k in di[wf] :
        ko = k
        if (k=='msec') :
          ko='nsec'
        if(k=='seconds') : ko='wall-clock-ns'
        if not ko in do : do[ko] = {}
        do[ko][wf] = di[wf][k]/den
        if (ko=='nsec') :  do[ko][wf]*=1000.*1000.
        if (ko=='wall-clock-ns') :  do[ko][wf]*=1000*1000.*1000.
    return do


def doPrint(di) :
  s = '|' + ' | '
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
  nop=0
  d ={}
  with open(fname) as f:
    print('\n\n---++ '+fname)
    for line in f:
      try:
        (wf, val, key) = line.split()
        d[wf] = {}
      except:
        nop+=1
  with open(fname) as f:
    for line in f:
      try:
        (wf, val, key) = line.split()
        d[wf][key]= float(val)
      except:
        nop+=1
#
  dc = parseCountsNorm(d,'cycles')
  di = parseCountsNorm(d,'instructions')
  ds = parseCountsNorm(d,'seconds')
#
  print('\n---+++ Normalized to Cycles')
  doPrint(dc)
  print('\n---+++ Normalized to Instructions')
  doPrint(di)
  print('\n---+++ Normalized to Wall-Clock (ns)')
  doPrint(ds)


files = ["haswell.count","icelake.count","skylake.count"]

print('---+ Deep Dive in HepSpec\n\n')
for f in files:
  parseOne(f)

