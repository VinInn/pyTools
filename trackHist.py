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


# cvsF = open('/Users/innocent/data/mva/ttbar.csv')
cvsF = open('/Users/innocent/data/mva/ttbarNewMVA.csv')


vtuple = csv.reader(cvsF)
header =  vtuple.next()

print header
chi2 = header.index('chi2')
dof = header.index('dof')
mva = header.index('mva')
mcfrac = header.index('mcfrac')
algo = header.index('algo')
pt = header.index('pt')
n3d = header.index('3DLayers')
hp = header.index('hp')


#fake rate
class fRate :
    def __init__(self) :
        self.all = []
        self.fake = []
        
    def fill(self, x, isFake) :
        self.all.append(x)
        if (isFake) : self.fake.append(x)

    def ratio(self,bins) :
        _cAll,_bin_edges = np.histogram(self.all,bins)
        _cFake,_bin_edges = np.histogram(self.fake,bins)
        # _bin_centres = (_bin_edges[:-1] + _bin_edges[1:])/2.
        _ratio = _cFake.astype(float,copy=False)/_cAll.astype(float,copy=False)
        _ratio.resize(len( _ratio)+1)
        return (_ratio,_bin_edges)


class multiPlot :
    def __init__(self, zbins,zlab):
        self.zlabel=zlab
        self.zbins = zbins
        self.hist = []
        for z in self.zbins : self.hist.append(fRate())
        self.hist.append(fRate())
        
    def fill(self, x, z, isFake) :
        _i = bisect_left(self.zbins, z)
        self.hist[_i].fill(x,isFake)
        # print _i, z

    def plot(self, bins) :
        k=0
        for h in self.hist:
            _y,_x = h.ratio(bins=bins)
            try :
                _label=self.zbins[k]
            except : _label='inf'
            plt.step(_x,_y,where='post',label=_label)
            k+=1

    

ntot=0

chi2H = fRate()
n3dH = fRate()
algoH = fRate()
mvaHpt = multiPlot([0.25,.5,2.,4.],'pt')
mvaH3d = multiPlot([1.1,2.1,3.1,4.1,6.1],'3d')
mvaHal = multiPlot([0.1,1.1,2.1,3.1,4.1,5.1,6.1],'algo')


while True:
    try :
        values = vtuple.next()
    except : break
    ntot+=1
    if float(values[dof]) >0 :
      chi2H.fill(float(values[chi2])/float(values[dof]),abs(float(values[mcfrac]))<0.5)
    # if float(values[pt]) >2 :
    n3dH.fill(float(values[n3d])+0.5, abs(float(values[mcfrac]))<0.5)
    algoH.fill(float(values[algo])+0.5, abs(float(values[mcfrac]))<0.5)
    mvaHpt.fill(float(values[mva]),float(values[pt]),abs(float(values[mcfrac]))<0.5)
    mvaH3d.fill(float(values[mva]),float(values[n3d]),abs(float(values[mcfrac]))<0.5)
    mvaHal.fill(float(values[mva]),float(values[algo]),abs(float(values[mcfrac]))<0.5)


print ntot
y,x = chi2H.ratio(bins=np.linspace(0, 40, 81))
print x
print y
plt.step(x,y,where='post')
plt.grid(True)
plt.show()

y,x = n3dH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post')
plt.grid(True)
plt.show()

y,x = algoH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post')
plt.grid(True)
plt.show()


mvaHpt.plot(bins=np.linspace(-1, 1,26))
plt.grid(True)
plt.legend(loc='upper right')
plt.show()


mvaH3d.plot(bins=np.linspace(-1, 1,26,endpoint=False))
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

mvaHal.plot(bins=np.linspace(-1, 1,26,endpoint=False))
plt.grid(True)
plt.legend(loc='upper right')
plt.show()



