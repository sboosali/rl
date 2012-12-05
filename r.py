#!/usr/bin/python
from __future__ import division
from numpy import *
import numpy as np
from mdp import *

# # # # # # # # # # # # # # # # # # # # # # 
# Learn
    
def short(s):
    return 'short' if s==s0 else 'next'

def long(s):
    return 'long' if s==s0 else 'next'


def Rlearning(mdp, n=inf, beta=0.1, alpha=0.1, eps=0.01, explore=0.1, debug=True):
    print
    print
    print 'R LEARNING...'

    # init
    R = { s : dict.fromkeys(mdp.A(s), 0)  for s in mdp.S }
    def V(s_): return max( R[s_][a_] for a_ in mdp.A(s_) )
    rho = { s : 0  for s in mdp.S }

    exploit = 1-explore

    i, diff, m = 0, inf, 0

    # loop
    while i < n: #and diff > eps:
        i+=1

        if mdp.s == 'h1':
            on = pick( [True, False], [exploit, explore] )

            if on: # on policy
                P = short  if R['h1']['short'] > R['h1']['long']  else long
            else: # off policy
                P = short  if R['h1']['short'] < R['h1']['long']  else long

        s,a,r,s_ = mdp.run(P)

        if on:
            rho[s] = rho[s] * (1-alpha)  +  alpha * (r + V(s_) - V(s))
            
        R[s][a]  =  R[s][a] * (1-beta)   +  beta *  (r + V(s_) - rho[s])

        m = (m*i + r) / (i+1)
        if debug and i%100 == 0 and m<1.8: print i,m
        
    return R,i,m

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
    R,iters,mean = Rlearning(mdp, n=n, beta=beta, alpha=alpha, eps=eps, explore=explore, debug=False)

    print
    print 'mean =', mean
    print 'iters =', iters
    Rlong, Rshort = R[s0]['long'], R[s0]['short']
    print 'Rlong =', Rlong
    print 'Rshort =', Rshort
    print Rlong > Rshort
    
    print
    print 'R ='
    print R
    
main()
