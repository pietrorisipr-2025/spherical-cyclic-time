#!/usr/bin/env python3
import numpy as np, math
ALPHAS=[0.10,0.20,0.50]; K=np.logspace(-2,2,121); YI,YF=-50.,50.
def V(y,alpha): return alpha*(1+(alpha-1)*y*y)/(1+y*y)**2
def integrate(h=0.0005):
    A=np.array(ALPHAS)[:,None,None]; k=K[None,:,None]
    u=np.zeros((len(ALPHAS),len(K),2)); v=np.zeros_like(u); u[:,:,0]=1.; v[:,:,1]=K[None,:]
    n=int(round((YF-YI)/h)); h=(YF-YI)/n; y=YI
    def f(yy,uu,vv): return vv, -(k*k-V(yy,A))*uu
    for _ in range(n):
        k1u,k1v=f(y,u,v); k2u,k2v=f(y+h/2,u+h*k1u/2,v+h*k1v/2); k3u,k3v=f(y+h/2,u+h*k2u/2,v+h*k2v/2); k4u,k4v=f(y+h,u+h*k3u,v+h*k3v)
        u += h*(k1u+2*k2u+2*k3u+k4u)/6; v += h*(k1v+2*k2v+2*k3v+k4v)/6; y += h
    A_norm=u[:,:,0]**2+(v[:,:,0]/K[None,:])**2; B_norm=u[:,:,1]**2+(v[:,:,1]/K[None,:])**2
    return 0.5*(A_norm+B_norm)
def fit(k,shape):
    x=k*k-k[0]*k[0]; y=np.log(np.maximum(shape,1e-300)); beta=max(-float(np.sum(x*y)/np.sum(x*x)),0.0); pred=-beta*x; sst=float(np.sum((y-y.mean())**2)); r2=float(1-np.sum((y-pred)**2)/sst) if sst>0 else float('nan'); mono=float(np.mean(np.diff(shape)<=0)); cls='GAUSSIAN_COMPATIBLE_TOY' if r2>=0.95 and mono>=0.90 and np.max(shape)<=10 else 'NON_GAUSSIAN_TRANSFER'; return cls,r2,mono,float(1/math.sqrt(beta)) if beta>0 else float('inf')
if __name__=='__main__':
    PT=integrate();
    for i,a in enumerate(ALPHAS):
        shape=PT[i]/PT[i,0]; print(a, fit(K,shape), 'PT(kmin)=',PT[i,0], 'PT(kmax)=',PT[i,-1], 'T_highk=',shape[-1])
