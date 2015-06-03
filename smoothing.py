#!/usr/bin/python

from numpy import *
from scipy import weave
from scipy.weave import converters

#uses a guassian smooth convoluted with finite differences to get an absurdly smooth line but with edge effects
superSmoothCode="""
double pre=0.3989422804014327/sigma;
double dx,xmus;

for(int a=0;a<N;a++){
    for(int b=0;b<N;b++){
        if(b==0)
            dx = xs[b+1]-xs[b];
        if(b==N-1)
            dx = xs[b]-xs[b-1];
        if(b>1 && b<N-1)
            dx = (xs[b+1]-xs[b-1])/2.0;

        xmus = (xs[a]-xs[b])/sigma;
        smoothys[a] += pre * exp( xmus * xmus * -0.5) * ys[b] * dx;
}}
"""
def superSmooth(xs,ys,sigma=0.1):
    N=len(ys)
    smoothys=zeros(N)
    xs=array(xs)
    ys=array(ys)
    weave.inline(superSmoothCode,['xs','ys','N','smoothys','sigma'])
    return smoothys

#1D data
def windowAvg(a,n=11,option='same'):
    #a: the list/array to run the window average over
    #n: the size of the window
    return convolve(a, ones(n)/n,option)
