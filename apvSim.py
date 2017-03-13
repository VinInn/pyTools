from math import *

def shape(i) :
    return i/50.*exp(-i/50.)

def signal() :
    s = []
    for i in range(0,600) :
        s.append(shape(i))
    return s

def samples() :
    s = signal()
    sa = []
    off = 0
    for i in range(off,300+off,25) :
        a=0.
        for j in range(0,25) :
            if (i>0) :
                a+=s[i+j]
        sa.append(a)
    return sa



def dec(off) :
    s = samples()
    x = (12+12.5)/50.;
    w3 = exp(-x-1)/x
    x+=25./50.
    w2 = -2*exp(-1)/x
    x+=25./50.
    w1 = exp(x-1)/x
    return w3*s[off] + w2*s[off+1]+w1*s[off+2]
            
print dec(0), dec(1), dec(2),dec(3)

