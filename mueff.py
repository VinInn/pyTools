import sys
import os
import csv
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
# from pylab import  show, gca, savefig
import scipy
from bisect import *

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)



# cvsF = open('/Users/innocent/data/mva/ttbar.csv')
cvsF = open('/Users/innocent/data/mva/jpsi.csv')


vtuple = csv.reader(cvsF)
header =  vtuple.next()

print header
chi2 = header.index('chi2')
dof = header.index('dof')
mva = header.index('mva')
mcfrac = header.index('mcfrac')
algo = header.index('algo')
oriAlgo = header.index('orialgo')
algoMask = header.index('algoMask')
pt = header.index('pt')
n3d = header.index('3DLayers')
npixels = header.index('npixels')
hp = header.index('hp')

earlyMask =  int('1111111',2)
promptMask = int(  '11111',2)


def testAlgo(values,al) :
   return testBit(int(values[algoMask]),al)
def earlyAlgo(values) :
    return int(values[algoMask]) & earlyMask
def promptAlgo(values) :
    return int(values[algoMask]) & promptMask

def fill(h,values,x):
    h.append(float(values[x]))

npixH=[]
n3dH=[]

ntot=0
nmu=0
n9=0
nhp=0
n10=0
ne=0
npx=0
while True:
    try :
        values = vtuple.next()
    except : break
    ntot+=1
    if float(values[mcfrac])<0.5 : continue
    nmu+=1
    if (not testAlgo(values,9)) : continue
    n9+=1
    if (bool(values[hp])) : nhp+=1
    if (testAlgo(values,10)) : n10+=1
    if earlyAlgo(values) : ne+=1
    if promptAlgo(values) : npx+=1
    fill(npixH,values,npixels)
    fill(n3dH,values,n3d)

print ntot,nmu,n9,nhp,n10,ne,npx

y,x = np.histogram(npixH,np.linspace(0.,6.,7))
y.resize(len(x))
plt.step(x,y,where='post')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

y,x = np.histogram(n3dH,np.linspace(0.,15,16))
y.resize(len(x))
plt.step(x,y,where='post')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

