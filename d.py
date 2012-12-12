#!/usr/bin/python
from __future__ import division
from numpy import *
import numpy as np
from matplotlib.pyplot import *
from time import clock, sleep

from mdp import *

# # # # # # # # # # # # # # # # # # # # # # 
# Learn
    
def short(s):
    return 'short' if s==s0 else 'next'

def long(s):
    return 'long' if s==s0 else 'next'


def Dlearning(mdp, n=inf, d=lambda t: 1/(1+t), alpha=0.1, eps=0.01, explore=0.1, debug=True):
    print
    print
    print 'D LEARNING...'

    # init
    D = { s : { a : 0  for a in mdp.A(s) }  for s in mdp.S }
    def V(s_): return max( D[s_][a_] for a_ in mdp.A(s_) )
    rho = { s : 0  for s in mdp.S }

    exploit = 1-explore

    i, diff, ms = 0, inf, zeros(n+1)

    # loop
    while i < n: #and diff > eps:
        i+=1

        if mdp.s == 'h1':
            on = pick( [True, False], [exploit, explore] )

            if on: # on policy
                P = short  if D['h1']['short'] > D['h1']['long']  else long
            else: # off policy
                P = short  if D['h1']['short'] < D['h1']['long']  else long

        s,a,r,s_ = mdp.run(P)

        D[s][a]  =  D[s][a] * (1-alpha)  +  alpha * (d(t) * r + todo)
        
        ms[i] = (ms[i-1]*i + r) / (i+1)
        if debug and i%100 == 0 and ms[i]<1.8: print i,ms[i]
        
    return D,i,ms

# # # # # # # # # # # # # # # # # # # # # # 
# Main

#TODO tune params: explore?, alpha, beta
def main():
    mdp = FeynmanFetch()

    global s0
    s0 = mdp.S[0]

    n       = 40
    alpha   = 0.1
    beta    = 0.1
    eps     = 0.01
    explore = 0.1

    begin = clock()
    D,iters,means = Dlearning(mdp, n=n, alpha=alpha, eps=eps, explore=explore, debug=False)
    finish = clock()
    
    print
    print 'time = %.3fs', (finish - begin)
    print 'mean =', means[-1]
    print 'iters =', iters
    Dlong, Dshort = D[s0]['long'], D[s0]['short']
    print 'Dlong =', Dlong
    print 'Dshort =', Dshort
    print Dlong > Dshort
    
    print
    print 'D ='
    print D
    
main()

sleep(60)
