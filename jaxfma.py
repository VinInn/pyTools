import numpy as np
import jax.numpy as jnp
from jax import jit

x = np.array([884279719003555.0,1.2,2.4,2.1,2.0], dtype=np.float32);
y = np.array([884279719003555.0,1.2,2.4,2.1,2.0], dtype=np.float32);
xj = jnp.array(x) # [884279719003555.0,1.2,2.4,2.1,2.0]);
yj = jnp.array(y) # [884279719003555.0,1.2,2.4,2.1,2.0]);

def fma(a,b,c) :
    return a*b+c

fmaj = jit(fma)

print("numpy fma",fma(xj,yj,-xj*yj))
print("jax fma", fmaj(xj,yj,-xj*yj))



def fast2Prod(b,c) :
   w = b*c 
   e = fmaj(b,c,-w)
   return [w,e]

f2pj = jit(fast2Prod)

print("numpy f2p (jit-fma)",fast2Prod(xj,yj))
print("jax f2p (jit-fma)",f2pj(xj,yj))
