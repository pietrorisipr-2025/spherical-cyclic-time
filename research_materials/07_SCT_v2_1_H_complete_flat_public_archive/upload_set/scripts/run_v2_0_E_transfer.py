#!/usr/bin/env python3
"""
SCT v2.0-E compact C2 matched power-law transfer execution.

Protocol:
a(y)=|y|^alpha for |y|>=1
a(y)=a0+b*y^2+c*y^4 for |y|<1
c=alpha*(alpha-2)/8
b=alpha*(4-alpha)/4
a0=1-alpha*(6-alpha)/8
u_k'' + [k^2 - a''/a] u_k = 0
k=logspace(-2,2,121), y in [-50,50].
Transfer metric: integrate basis (1,0), (0,k), use norm u^2+(u'/k)^2, average basis powers,
then define T_shape=(raw_transfer/raw_transfer[k_min])^2.
"""
import numpy as np

def potential_compact(y, alpha):
    sy=abs(y)
    if sy >= 1.0:
        return alpha*(alpha-1)/(y*y)
    c=alpha*(alpha-2)/8.0
    b=alpha*(4-alpha)/4.0
    a0=1-alpha*(6-alpha)/8.0
    a=a0 + b*y*y + c*y**4
    add=2*b + 12*c*y*y
    return add/a

def run(alpha=0.2, h=0.0005):
    ks=np.logspace(-2,2,121)
    U=np.zeros((2,len(ks))); V=np.zeros_like(U)
    U[0]=1.0; V[0]=0.0
    U[1]=0.0; V[1]=ks
    y0=-50.0; y1=50.0
    n=int(round((y1-y0)/h))
    h=(y1-y0)/n
    y=y0
    for _ in range(n):
        w1=ks*ks - potential_compact(y, alpha)
        k1u=V; k1v=-w1*U
        yh=y+0.5*h
        w2=ks*ks - potential_compact(yh, alpha)
        u2=U+0.5*h*k1u; v2=V+0.5*h*k1v
        k2u=v2; k2v=-w2*u2
        u3=U+0.5*h*k2u; v3=V+0.5*h*k2v
        k3u=v3; k3v=-w2*u3
        yf=y+h
        w4=ks*ks - potential_compact(yf, alpha)
        u4=U+h*k3u; v4=V+h*k3v
        k4u=v4; k4v=-w4*u4
        U=U+h*(k1u+2*k2u+2*k3u+k4u)/6.0
        V=V+h*(k1v+2*k2v+2*k3v+k4v)/6.0
        y=yf
    norms=np.sqrt(U*U + (V/ks)**2)
    raw=np.sqrt((norms[0]**2 + norms[1]**2)/2.0)
    shape=(raw/raw[0])**2
    return ks, raw, shape

if __name__ == "__main__":
    for a in [0.20,0.10,0.50]:
        ks, raw, shape = run(a)
        print(a, shape.min(), shape[-10:].mean())
