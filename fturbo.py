cat fturbo.py 
#!python

import sys
def fturbo(fname) :
   col=[1,2,10,22,23]
   f=open(fname,'r')
   h = f.readline().split()
   lo = 'sec'
   for c in col:
     lo+=' '+h[c]
   print lo
   s=0
   for l in f :
     lo = str(s)
     e=l.split()
     for c in col:
       lo+=' '+e[c]
     print lo
     s+=2

fturbo('turbo.log')

