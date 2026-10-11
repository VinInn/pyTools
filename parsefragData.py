#import re

def oneVal(elems,tag) :
  for elem in elems:
    if elem.find(tag) != -1 : return re.findall("\d+",elem)[0]
  return '0'

def buddy(elems,tag) :
  for elem in elems:
    if elem.find(tag) != -1 : return re.findall("\d+",elem.split(',')[1])
  return ['0','0','0','0','0','0','0','0','0','0']

def times(elems,tag) :
  uTime = 0
  sTime = 0
  for elem in elems:
    if elem.find(tag) != -1 :
      a = elem
      if elem.find(')') !=-1 : a = elem.split(')')[1]
      times =  re.findall("\d+",a)
      uTime += int(times[0])
      sTime += int(times[1])
  return [uTime,sTime] 

def parseOne(elems) :
  ret = []
  date = elems[0]
  time = elems[1]
  power = oneVal(elems,'power')
  heap = oneVal(elems,'AnonPages')
  huge = oneVal(elems,'AnonHugePages')
  buddy0 = buddy(elems,'Node 0')
  buddy1 = buddy(elems,'Node 1')
  cpu = times(elems,'cpu')
  job = times(elems,'cms')  


dir = '/Users/innocent/cernbox/HepSpec/fragData/'
file = dir+'dumpMemMon.log'
lines = open(file).read().split('END\n')
elems = lines[20].split('\n')
parseOne(elems)
