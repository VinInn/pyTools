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


cvsF = open('/Users/innocent/data/mva/ttbar.csv')
# cvsF = open('/Users/innocent/data/mva/ttbarNewMVA.csv')


vtuple = csv.reader(cvsF)
header =  vtuple.next()

print header
chi2 = header.index('chi2')
dof = header.index('dof')
mva = header.index('mva')
mcfrac = header.index('mcfrac')
algo = header.index('algo')
oriAlgo = header.index('orialgo')
eta = header.index('eta')
pt = header.index('pt')
n3d = header.index('3DLayers')
nl = header.index('Layers')
nm = header.index('missingLayers')
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
        _ratio = _cFake.astype(float,copy=False)/np.fmax(_cAll.astype(float,copy=False),1.)
        _ratio.resize(len( _ratio)+1)
        _eff = _cAll.astype(float,copy=False)/float(len(self.all))
        _eff.resize(len(_bin_edges))
        return (_ratio,_bin_edges, _eff)

    def cum(self,bins) :
        _cAll,_bin_edges = np.histogram(self.all,bins)
        _cFake,_bin_edges = np.histogram(self.fake,bins)
        _sig = np.cumsum(_cAll, dtype=float)
        _ratio = np.cumsum(_cFake, dtype=float)/_sig
        _eff = _sig/float(len(self.all))
        _ratio.resize(len(_bin_edges))
        _eff.resize(len(_bin_edges))
        return (_ratio,_bin_edges, _eff)

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
            _y,_x,_z = h.ratio(bins=bins)
            try :
                _label=self.zbins[k]
            except : _label='inf'
            plt.step(_x,_y,where='post',label=_label)
            k+=1

    

ntot=0

etaH=fRate()
chi2H = fRate()
chi2lH = fRate()
n3dH = fRate()
nlH = fRate()
nmH = fRate()
algoH = fRate()
orialgoH = fRate()
mvaHpt = multiPlot([0.25,.5,2.,4.],'pt')
mvaH3d = multiPlot([1.1,2.1,3.1,4.1,6.1],'3d')
mvaHal = multiPlot([0.1,1.1,2.1,3.1,4.1,5.1,6.1],'algo')
etaHal = multiPlot([0.1,1.1,2.1,3.1,4.1,5.1,6.1],'algo')


nhp=0
while True:
    try :
        values = vtuple.next()
    except : break
    ntot+=1
    if  values[hp] != 'True' : continue
    nhp+=1
    if float(values[dof]) <0.5 : continue;
    if float(values[nl])  <0.5 : continue;
#    if float(values[pt]) <2 : continue
#    if float(values[n3d])  <2.5 : continue;
#    if float(values[chi2]) >0.4*float(values[dof]) : continue

    etaH.fill(float(values[eta]),abs(float(values[mcfrac]))<0.5)
    chi2H.fill(float(values[chi2])/float(values[dof]),abs(float(values[mcfrac]))<0.5)
    chi2lH.fill(float(values[chi2])/(float(values[dof])*float(values[nl])),abs(float(values[mcfrac]))<0.5)
    # if float(values[pt]) >2 :
    n3dH.fill(float(values[n3d])+0.5, abs(float(values[mcfrac]))<0.5)
    nlH.fill(float(values[nl])+0.5, abs(float(values[mcfrac]))<0.5)
    nmH.fill(float(values[nm])+0.5, abs(float(values[mcfrac]))<0.5)
    algoH.fill(float(values[algo])+0.5, abs(float(values[mcfrac]))<0.5)
    orialgoH.fill(float(values[oriAlgo])+0.5, abs(float(values[mcfrac]))<0.5)
    mvaHpt.fill(float(values[mva]),float(values[pt]),abs(float(values[mcfrac]))<0.5)
    mvaH3d.fill(float(values[mva]),float(values[n3d]),abs(float(values[mcfrac]))<0.5)
    mvaHal.fill(float(values[mva]),float(values[oriAlgo]),abs(float(values[mcfrac]))<0.5)
    etaHal.fill(float(values[eta]),float(values[oriAlgo]),abs(float(values[mcfrac]))<0.5)


print ntot,nhp

y,x,z = etaH.ratio(bins=np.linspace(-2.5, 2.5, 51))
print x
print y
print z
plt.step(x,y,where='post',label='eta fake')
plt.step(x,z,where='post',label='eff')
plt.grid(True)
plt.legend(loc='upper right')
#plt.yscale('log')
plt.show()

etaHal.plot(bins=np.linspace(-2.5, 2.5, 51))
plt.grid(True)
plt.legend(loc='upper right')
plt.show()


y,x,z = chi2H.cum(bins=np.linspace(0, 10, 81))
print x
print y
print z
plt.step(x,y,where='post',label='chi2 fake')
plt.step(x,z,where='post',label='chi2 eff')
plt.grid(True)
plt.legend(loc='upper right')
#plt.yscale('log')
plt.show()




y,x,z = chi2lH.cum(bins=np.linspace(0, 1, 81))
print x
print y
plt.step(x,y,where='post',label='chi2/nlayer')
plt.step(x,z,where='post',label='eff')
plt.grid(True)
plt.legend(loc='upper right')
#plt.yscale('log')
plt.show()



y,x,z = n3dH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post',label='3dLayers')
plt.step(x,z,where='post',label='eff')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

y,x,z = nlH.ratio(bins=np.linspace(0., 20., 21))
print x
print y
plt.step(x,y,where='post',label='Layers')
plt.step(x,z,where='post',label='eff')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

y,x,z = nmH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post',label='missing Layers')
plt.step(x,z,where='post',label='eff')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()


y,x,z = algoH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post',label='algo')
plt.step(x,z,where='post',label='eff')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

y,x,z = orialgoH.ratio(bins=np.linspace(0., 12., 13))
print x
print y
plt.step(x,y,where='post',label='ori-algo')
plt.step(x,z,where='post',label='eff')
plt.legend(loc='upper right')
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



