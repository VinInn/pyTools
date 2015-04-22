import sys
import os
import csv
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
# from pylab import  show, gca, savefig
import scipy

def ploterr(values,bins,color,label,xLabel) :
    counts,bin_edges = np.histogram(values,bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    err = np.sqrt(counts)
    norm = np.sum(counts)
    plt.errorbar(bin_centres, counts.astype(float,copy=False)/norm, yerr=err/norm, fmt='o',color=color,label=label)
    plt.xlabel(xLabel)
    return (bin_centres, counts.astype(float,copy=False)/norm, err/norm)

from numpy.random import normal
from scipy.special import wofz
from kapteyn import kmpfit
ln2 = np.log(2)


def voigt(x, y):
   # The Voigt function is also the real part of 
   # w(z) = exp(-z^2) erfc(iz), the complex probability function,
   # which is also known as the Faddeeva function. Scipy has 
   # implemented this function under the name wofz()
   z = x + 1j*y
   I = wofz(z).real
   return I

def Voigt(nu, alphaD, alphaL, nu_0, A, a=0, b=0):
   # The Voigt line shape in terms of its physical parameters
   f = np.sqrt(ln2)
   x = (nu-nu_0)/alphaD * f
   y = alphaL/alphaD * f
   backg = a + b*nu 
   V = A*f/(alphaD*np.sqrt(np.pi)) * voigt(x, y) + backg
   return V

def funcV(p, x):
    # Compose the Voigt line-shape
    alphaD, alphaL, nu_0, I, a, b = p
    scale = nu_0/91.2
    return Voigt(x, scale*alphaD, scale*alphaL, nu_0, I, a, b)


def residualsV(p, data):
   # Return weighted residuals of Voigt
   x, y, err = data
   return (y-funcV(p,x)) / err


def fitZshape(x,y,err) :

    A = 0.5
    alphaD = 1.4
    alphaL = 2.5/2
    a = 0.001
    b = 0
    nu_0 = 91.2
    p0 = [alphaD, alphaL, nu_0, A, a, b]

    # Do the fit
    fitter = kmpfit.Fitter(residuals=residualsV, data=(x,y,err))
  #  fitter.parinfo = [{}, {}, {}, {}, {}, {'fixed':True}]  # Take zero level fixed in fit
    fitter.parinfo = [{}, {'fixed':True}, {}, {}, {}, {}] 
    fitter.fit(params0=p0)

    print "\n========= Fit results Voigt profile =========="
    print "Initial params:", fitter.params0
    print "Params:        ", fitter.params
    print "Iterations:    ", fitter.niter
    print "Function ev:   ", fitter.nfev 
    print "Uncertainties: ", fitter.xerror
    print "dof:           ", fitter.dof
    print "chi^2, rchi2:  ", fitter.chi2_min, fitter.rchi2_min
    print "stderr:        ", fitter.stderr   
    print "Status:        ", fitter.status
    
    alphaD, alphaL, nu_0, I, a_back, b_back = fitter.params
    c1 = 1.0692
    c2 = 0.86639
    hwhm = 0.5*(c1*alphaL+np.sqrt(c2*alphaL**2+4*alphaD**2))
    print "\nFWHM Voigt profile:     ", 2*hwhm
    f = np.sqrt(ln2)
    Y = alphaL/alphaD * f
    amp = I/alphaD*np.sqrt(ln2/np.pi)*voigt(0,Y)
    print "Amplitude Voigt profile:", amp
    print "Area under profile:     ", I
    return fitter.params




#bins = numpy.linspace(-10, 10, 100)
#pl.hist(data, bins=np.logspace(0.1, 1.0, 50))
#pl.gca().set_xscale("log")

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_xlim(23.5, 28)
#ax.set_ylim(0, 30)
#ax.grid(True)
#plt.yscale('log')

#gaussian_numbers = normal(size=1000)
#plt.hist(gaussian_numbers, bins=20, histtype='step')
#plt.title("Gaussian Histogram")
#plt.xlabel("Value")
#plt.ylabel("Frequency")

# plt.draw_if_interactive()
#plt.show()


dm53f = open('/Users/innocent/data/ZZ/histos/DoubleMu2012_53X.csv','rb')
dm74f = open('/Users/innocent/data/ZZ/histos/DoubleMu2012_74X.csv','rb')
dm53 = csv.reader(dm53f, delimiter=',')
dm74 = csv.reader(dm74f)

#          writer.writerow([i,mass,diMu.pt(),URSP,URES,
#          pt,e,p, mu1.dB(2)/mu1.edB(2),mu1.dB(1)/mu1.edB(1),mu1.track().dxy(pvp)/mu1.track().dxyError(),mu1.track().dz(pvp)/mu1.track().dzError(),
#          mu2.dB(2)/mu2.edB(2),mu2.dB(1)/mu2.edB(1),mu2.track().dxy(pvp)/mu2.track().dxyError(),mu2.track().dz(pvp)/mu2.track().dzError()])




mass53=[]
mass74=[]
pt53=[]
pt74=[]
sip3d53=[]
sip3d74=[]
for row in dm53f :
    r = row.split(',')
  #  if (float(r[2])<10) : continue
    if (abs(float(r[5]))<15) : continue
    if (abs(float(r[5+7]))<15) : continue
    if (abs(float(r[6]))<1.0) : continue
    if (abs(float(r[6+7]))<1.0) : continue
    if (abs(float(r[9]))<4 and abs(float(r[6+7]))<4) :
      mass53.append(float(r[1]))
      if (float(r[1])>87 and float(r[1])<95) : pt53.append(float(r[2]))
    sip3d53.append(float(r[9]))
    sip3d53.append(float(r[9+7]))
for row in dm74f :
    r = row.split(',')
 #   if (float(r[2])<10) : continue
    if (abs(float(r[5]))<15) : continue
    if (abs(float(r[5+7]))<15) : continue
    if (abs(float(r[6]))<1.0) : continue
    if (abs(float(r[6+7]))<1.0) : continue
    if (abs(float(r[9]))<4 and abs(float(r[9+7]))<4) :
      mass74.append(float(r[1]))
      if (float(r[1])>87 and float(r[1])<95) : pt74.append(float(r[2]))
    sip3d74.append(float(r[9]))
    sip3d74.append(float(r[9+7]))


plt.rc('legend', fontsize=18)
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_xlim(23.5, 28)
#ax.set_ylim(0.0001, 1.)
ax.grid(True)
#plt.hist([mass53,mass74],bins=np.linspace(70, 120, 100), normed=1,color=['b','r'], histtype='step',label=['53','74'])
ax.legend(loc='upper right')
# plt.yscale('log')
#plt.show()

ax.set_title('$\mu^+\mu^-$ Mass')

bin_centres, yval,err =ploterr(values=mass53,bins=np.linspace(80, 100, 50),color='b',label='53',xLabel='$\mu^+\mu^-$ Mass (GeV)')
alphaD, alphaL, nu_0, I, a_back, b_back = fitZshape(bin_centres, yval,err)
f = Voigt(nu=bin_centres, alphaD=alphaD, alphaL=alphaL, nu_0=nu_0, A=I,a=a_back,b=b_back)
plt.plot(bin_centres, f, 'g--', linewidth=1)
ax.text(81, 0.06, '\n$Z^o$ mass = %4.2f'%nu_0+'\n$\sigma_{p_t}/p_t$ = %4.3f'%(alphaD/nu_0), fontsize=15, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})


bin_centres, yval,err = ploterr(values=mass74,bins=np.linspace(80, 100, 50),color='r',label='74',xLabel='$\mu^+\mu^-$ Mass (GeV)')
def zshape(x) :
    gamma=2.5
    x0 = 91.2
    g = np.sqrt((gamma**2+x0**2)*(x0**2))
    k = 2.*np.sqrt(2.)*x0*gamma*g/(3.1415*np.sqrt(x0**2+g))
    # return 0.25*gamma/(2.*3.1415*((x-x0)**2+gamma**2/4))
    return 0.25*k /( (x0*gamma)**2 + (x**2-x0**2)**2)
#f= zshape(bin_centres)

alphaD, alphaL, nu_0, I, a_back, b_back = fitZshape(bin_centres, yval,err)

f = Voigt(nu=bin_centres, alphaD=alphaD, alphaL=alphaL, nu_0=nu_0, A=I,a=a_back,b=b_back)
plt.plot(bin_centres, f, 'g--', linewidth=1)
ax.text(81, 0.04, '\n$Z^o$ mass = %4.2f'%nu_0+'\n$\sigma_{p_t}/p_t$ = %4.3f'%(alphaD/nu_0), fontsize=15, bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

plt.legend(loc='upper right')

plt.show()

ploterr(values=sip3d53,bins=np.linspace(-6, 6, 60),color='b',label='53',xLabel='Sip3d')
ploterr(values=sip3d74,bins=np.linspace(-6, 6, 60),color='r',label='74',xLabel='Sip3d')
plt.grid(True)
ax.set_ylim(0.0001, 1.)
plt.legend(loc='upper right')
plt.yscale('log')
plt.show()


ploterr(values=pt53,bins=np.linspace(0, 100, 100),color='b',label='53',xLabel='Z pt (GeV)')
ploterr(values=pt74,bins=np.linspace(0, 100, 100),color='r',label='74',xLabel='Z pt (GeV)')
ax.set_ylim(0.0001, 1.)
plt.legend(loc='upper right')
plt.yscale('log')
plt.grid(True)
plt.show()
