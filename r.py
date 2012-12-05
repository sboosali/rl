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


def Rlearning(mdp, n=inf, beta=0.1, alpha=0.1, eps=0.01, explore=0.1, debug=True):
    print
    print
    print 'R LEARNING...'

    # init
    R = { s : dict.fromkeys(mdp.A(s), 0)  for s in mdp.S }
    def V(s_): return max( R[s_][a_] for a_ in mdp.A(s_) )
    rho = 0 # assume unichain policy -> rho[s] == rho[s_] forall states s,s_ -> const rho
    #rho = { s : 0  for s in mdp.S }
    
    exploit = 1-explore
    
    i, diff, rs = 0, inf, zeros(n)
    
    # loop
    while i < n: #and diff > eps:

        on = pick( [True, False], [exploit, explore] )

        if mdp.s == 'h1':
            if on: # on policy
                P = short  if R['h1']['short'] > R['h1']['long']  else long
            else: # off policy
                P = short  if R['h1']['short'] < R['h1']['long']  else long


        s,a,r,s_ = mdp.run(P)
        
        R[s][a]  =  R[s][a] * (1-beta)   +  beta  * (r + V(s_) - rho)

        if on:
            rho = rho * (1-alpha)  +  alpha * (r + V(s_) - V(s))

            
        rs[i] = r
        #if debug and i%100 == 0 and ms[i]<1.8: print i,ms[i]
        i+=1
        
    return R,i,rs

# # # # # # # # # # # # # # # # # # # # # # 
# Main

#TODO tune params: explore?, alpha, beta
def main():
    mdp = FeynmanFetch()

    global s0
    s0 = mdp.S[0]

    import argparse
    cl = argparse.ArgumentParser()
    cl.add_argument('-alpha', type=float, default=None)
    cl.add_argument('-n', type=int, default=None)
    args = cl.parse_args()

    n       = args.n if args.n else 50*1000
    alpha   = args.alpha if args.alpha else 0.9
    beta    = 0.1
    eps     = 0.01
    explore = 0.1

    begin = clock()
    R,iters,rewards = Rlearning(mdp, n=n, beta=beta, alpha=alpha, eps=eps, explore=explore, debug=False)
    finish = clock()

    means1000(rewards)
    
    print
    print 'time = %.3fs' % (finish - begin)
    print 'mean =', mean(rewards)
    print 'iters =', iters
    Rlong, Rshort = R[s0]['long'], R[s0]['short']
    print 'Rlong =', Rlong
    print 'Rshort =', Rshort
    print Rlong > Rshort
    
    print
    print 'R ='
    print R

if __name__=='__main__':
    main()

    sleep(60)
