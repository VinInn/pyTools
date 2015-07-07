import sys
import os
import csv
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
# from pylab import  show, gca, savefig
import scipy
import pylab
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

def onlyBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)



def bitCount(int_type):
    count = 0
    while(int_type):
        int_type &= int_type - 1
        count += 1
    return(count)



#sample= r'$t \bar t$ + 35PU 25ns'
#cvsF = open('/Users/innocent/data/mva/ttbar.csv')
#cvsF = open('/Users/innocent/data/mva/r74x.csv')

sample= r'boosted $J\psi$ gun + 35PU 25ns'
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
eta = header.index('eta')
pt = header.index('pt')
n3d = header.index('3DLayers')
npixels = header.index('npixels')
hp = header.index('hp')

earlyMask =  int('1111111',2)
promptMask = int(  '11111',2)

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")

def testAlgo(values,al) :
   return testBit(int(values[algoMask]),al)
def onlyAlgo(values,al) :
   return onlyBit(int(values[algoMask]),al)
def earlyAlgo(values) :
    return int(values[algoMask]) & earlyMask
def promptAlgo(values) :
    return int(values[algoMask]) & promptMask

def countEarly(values) :
    return bitCount(earlyAlgo(values))

def fill(h,values,x):
    h.append(float(values[x]))

npixH=[]
n3dH=[]
etaH=[]
ptH=[]

algoX=np.arange(0,12)
algoH=np.zeros(12)
oriAlgoH=np.zeros(12)
onlyAlgoH=np.zeros(12)

earlyCountH=np.zeros(12)

allAlgoH=np.zeros((12,12))
def fillAll(values) :
    am = int(values[algoMask])
    for i in range(0,11) :
        if not onlyBit(am,i) : onlyAlgoH[i]+=1
        if testBit(am,i) : 
            for j in range(0,11):
                if testBit(am,j) : allAlgoH[i][j]+=1 


ntot=0
nmu=0
nmuhp=0
n9=0
n9all=0
neall=0
nhp=0
n10=0
ne=0
npx=0
n10ori=0

sample += ' (signal only)'

while True:
    try :
        values = vtuple.next()
    except : break
    ntot+=1
    if abs(float(values[mcfrac]))<0.5 : continue
    # if (not testAlgo(values,10)) : continue
    nmu+=1
    if (not str2bool(values[hp])) : continue
    nmuhp+=1

    fillAll(values)
    if earlyAlgo(values)==0 : print values
    if (str2bool(values[hp])) :
      algoH[int(values[algo])]+=1
      oriAlgoH[int(values[oriAlgo])]+=1
      earlyCountH[countEarly(values)]+=1

    if (testAlgo(values,9)) : n9all+=1
    if earlyAlgo(values) : neall+=1
    if (not testAlgo(values,10)) : continue
    n10+=1
    if (str2bool(values[hp])) : nhp+=1
    if (testAlgo(values,9)) : n9+=1
    if earlyAlgo(values) : ne+=1
    if promptAlgo(values) : npx+=1
    if (int(values[oriAlgo])==10) :
        n10ori+=1
        fill(npixH,values,npixels)
        fill(n3dH,values,n3d)
        fill(etaH,values,eta)
    

print 'ntot,nmu,nmuhp,n9all,neall,n10,nhp,n9,ne,npx,n10-ne,n10ori'
print ntot,nmu,nmuhp,n9all,neall,n10,nhp,n9,ne,npx,n10-ne,n10ori

allAlgoH /=(0.01*float(nmuhp))
print oriAlgoH
print allAlgoH


plt.style.use('fivethirtyeight') # 'ggplot')

algoNames =[
    "initialStep",
    "lowPtTripletStep",
    "pixelPairStep",
    "detachedTripletStep",
    "mixedTripletStep",
    "pixelLessStep",
    "tobTecStep",
    "jetCoreRegionalStep",
    "conversionStep",
    "muonSeededStepInOut",
    "muonSeededStepOutIn",
        ]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.2, right=0.9)
ax.set_xlim(0,11)
ax.set_ylim(0,11)
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocator   = MultipleLocator(1)
ax.xaxis.set_major_locator(majorLocator)
ax.yaxis.set_major_locator(majorLocator)
#ylpos = np.arange(11)+0. 
#ax.set_yticklabels(ylpos,algoNames)
#pylab.yticks(ylpos,algoNames)
for i in range(0,11) :
    plt.annotate(algoNames[i],xy=(0.0,i+0.25), horizontalalignment='right')
    for j in range(i,11):
        plt.annotate('%4.1f'%allAlgoH[i][j],xy=(i+0.25,j+0.25),
                     # horizontalalignment='left', verticalalignment='bottom'
                     )
    
ax.set_title(sample,fontsize=20, fontweight='bold')
plt.grid(True,which='both')
#plt.legend(loc='upper right')
plt.show()

# savefig('algotable.png')

plt.style.use('ggplot')

plt.step(algoX,algoH,where='post',label='final algo', linewidth=2)
plt.step(algoX,oriAlgoH,where='post',label='original algo', linewidth=2)
plt.step(algoX,onlyAlgoH,where='post',label='only algo', linewidth=2)
plt.grid(True)
plt.annotate(('inefficiency: %4.2f'%float(oriAlgoH[10]/(0.01*n10)))+r'$\%$',
             xy=(algoX[10]+0.5,oriAlgoH[10]+0.1), xytext=(algoX[10]-2.0,0.5*algoH[10]),
            arrowprops=dict(facecolor='black', shrink=0.05),fontsize=16
            )

plt.title(sample,fontsize=20, fontweight='bold')
plt.legend(loc='upper right')
plt.show()

plt.step(algoX,earlyCountH,where='post',label='count early interations', linewidth=2)
print earlyCountH
plt.grid(True)
plt.title(sample,fontsize=20, fontweight='bold')
plt.legend(loc='upper right')
plt.annotate(('not found in early iterations: %4.2f'%float(earlyCountH[0]/(0.01*ne)))+r'$\%$',
             xy=(algoX[0]+0.5,earlyCountH[0]+0.1), xytext=(algoX[0]+2.0,0.5*earlyCountH[1]),
            arrowprops=dict(facecolor='black', shrink=0.05),fontsize=16
            )

plt.show()



y,x = np.histogram(npixH,np.linspace(0.,6.,7))
y.resize(len(x))
plt.step(x,y,where='post',label='N pixel')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

y,x = np.histogram(n3dH,np.linspace(0.,15,16))
y.resize(len(x))
plt.step(x,y,where='post',label='N 3Dlayers')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

y,x = np.histogram(etaH,np.linspace(-2.5,2.5,26))
y.resize(len(x))
plt.step(x,y,where='post',label='eta')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

