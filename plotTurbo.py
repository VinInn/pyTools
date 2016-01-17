import sys
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from pylab import  show, gca, savefig

def pl(tax,x,y,l,c) :
  tax.plot(x,y,c)
  tax.set_ylabel(l,color=c)
  for tl in tax.get_yticklabels():
    tl.set_color(c)

fname='turbo.log'
sec,busy,freq,tmp,pw,rw = np.loadtxt(fname,skiprows=1,unpack=True)
fig, ax1 = plt.subplots()
ax1.set_xlabel('time (s)')
pl(ax1,sec,freq,'MHz','b')
pl(ax1.twinx(),sec,tmp,'T','r')
pl(ax1.twinx(),sec,pw+rw,'W','g')
pl(ax1.twinx(),sec,busy,'%','k')
plt.show()
