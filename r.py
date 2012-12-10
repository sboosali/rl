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


def Rlearning(mdp, n=inf, beta=0.01, alpha=0.01, delta=0.0001, explore=0.01, debug=True):
    print
    print
    print 'R LEARNING...'
    
    # init
    R = { s : { a : 0  for a in mdp.A(s) }  for s in mdp.S }
    def V(s_): return max( R[s_][a_] for a_ in mdp.A(s_) )
    # unichain policy -> rho[s] == rho[s_] forall states s,s_ -> const rho
    rho = 0
    #rho = { s : 0  for s in mdp.S }
    
    exploit = 1-explore
    
    i, diff, rs = 0, inf, zeros(n)
    
    # loop
    while i < n: #and diff > delta:

        # epsilon greedy exploration "on policy"
        on = pick( [True, False], [exploit, explore] )

        if mdp.s == 'h1':
            if on:
                P = short  if R['h1']['short'] > R['h1']['long']  else long
            else:
                P = short  if R['h1']['short'] < R['h1']['long']  else long


        s,a,r,s_ = mdp.run(P)
        
        R[s][a] = R[s][a] * (1-beta)  +  beta  * (r + V(s_) - rho)

        if on:
            # on policy, V s = R s P(s) = R s a
            rho = rho *    (1-alpha)  +  alpha * (r + V(s_) - V(s))
                        
        rs[i] = r
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
    cl.add_argument('-save', action='store_true', dest='save', default=False)

    global args
    args = cl.parse_args()

    n       = args.n if args.n else 50*1000
    alpha   = args.alpha if args.alpha else 0.1
    beta    = 0.1
    delta   = 0.0001
    eps     = 0.001

    begin = clock()
    R,iters,rewards = Rlearning(mdp, n=n, beta=beta, alpha=alpha, delta=delta, explore=eps, debug=False)
    finish = clock()

    title(r'$n$=%d $\beta$=%.4f $\alpha$=%.4f $\epsilon$=%.4f' 
          % (n, beta, alpha, eps))
    means1000(rewards, args.save)
    
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

    show() if args.save else sleep(60)
