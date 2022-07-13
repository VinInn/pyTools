#!/usr/bin/env python3

import sys
def fturbo(f) :
   col=[1,0,2,14,18,19]
   # f=open(fname,'r')
   h = f.readline().split()
   lo = 'sec'
   for c in col:
     lo+=' '+h[c]
   print(lo)
   s=0
   while True :
     l= f.readline()
     lo = str(s)
     e=l.split()
     try :
       for c in col:
         lo+=' '+e[c]
       print(lo)
     except: 
       return
     s+=1
     sys.stdout.flush()



fturbo(sys.stdin)

