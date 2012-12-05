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

def argmax(xs, f):
    return xs[ np.argmax(f(xs)) ]

def Qlearning(mdp, n=inf, alpha=0.1, eps=0.01, explore=0.1, debug=True):
    print
    print
    print 'Q LEARNING...'

    # init
    Q = { s : dict.fromkeys(mdp.A(s), 0)  for s in mdp.S }
    gamma = mdp.gamma
    i, diff, m = 0, inf, 0
    exploit = 1-explore
    def V(s_): return max( Q[s_][a_] for a_ in mdp.A(s_) )
    
    # loop
    while i < n: #and diff > eps:
        i+=1

        if mdp.s == 'h1':
            # on policy
            P = short  if Q['h1']['short'] > Q['h1']['long']  else long
            exploration = short if P==long else long

            # off policy
            P = pick( [P, exploration], [exploit, explore] )
            
        s,a,r,s_ = mdp.run(P)

        m = (m*i + r) / (i+1)
        if debug and i%100 == 0 and m<1.8: print i,m
        
        #Qsa = Q[s][a]
        Q[s][a]  =  Q[s][a] * (1-alpha)  +  alpha * (r + gamma * V(s_) )
        #diff = Qsa - Q[s][a]
        
    return Q,i,m

# # # # # # # # # # # # # # # # # # # # # # 
# Main

for gamma in [0.7, 0.9, 0.99]:
    mdp = FeynmanFetch(gamma=gamma)
    s0 = mdp.S[0]

    n, alpha, eps, explore = 40*1000, 0.1, 0.01, 0.1
    Q,iters,mean = Qlearning(mdp, n=n, alpha=alpha, eps=eps, explore=explore, debug=False)

    print
    print 'gamma =', gamma
    print 'mean =', mean
    print 'iters =', iters
    Qlong, Qshort = Q[s0]['long'], Q[s0]['short']
    print 'Qlong =', Qlong
    print 'Qshort =', Qshort
    print Qlong > Qshort
    
    print
    print 'Q ='
    print Q
    
