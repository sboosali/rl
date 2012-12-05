#!/usr/bin/python
from __future__ import division
from numpy import *
import numpy as np
from mdp import *

# # # # # # # # # # # # # # # # # # # # # # 
# Learn
    
def short(s):
    return 'short' if s==0 else 'next'

def long(s):
    return 'long' if s==0 else 'next'

def argmax(xs, f):
    return xs[ np.argmax(f(xs)) ]

def Qlearning(mdp, n=inf, alpha=0.1, eps=0.01, explore=0.1):
    # init
    print 'init..'
    Q = dict( (s, dict.fromkeys(mdp.A(s), 0)) for s in mdp.S )
    print Q
    print Q[0]
    print Q[0]['short']
    gamma = mdp.gamma
    i, diff = 0, inf
    exploit = 1-explore
    def V(s_): return max( Q[s_][a_] for a_ in mdp.A(s_) )
    
    # loop
    print
    print 'iter...'
    while i < n: #and diff > eps:
        i+=1
        print i
        
        if mdp.s == 0:
            # on policy
            P = short  if Q[0]['short'] > Q[0]['long']  else long
            exploration = short if P==long else long

            # off policy
            P = pick( [P, exploration], [exploit, explore] )
            
        s,a,r,s_ = mdp.run(P)
        print 'sars', s,a,r, s_
        
        #Qsa = Q[s][a]
        Q[s][a]  =  Q[s][a] * (1-alpha)  +  alpha * (r + gamma * V(s_) )
        #diff = Qsa - Q[s][a]
        
    return Q,i

# # # # # # # # # # # # # # # # # # # # # # 
# Main

mdp = FeynmanFetch(gamma=0.99, s0=0)
n, alpha, eps, explore = 40*1000, 0.1, 0.01, 0.1

Q,i = Qlearning(mdp, alpha=alpha, n=n, eps=eps, explore=explore)

Qlong, Qshort = Q[0]['long'], Q[0]['short']
print 'Qlong', Qlong
print 'Qshort', Qshort
print Qlong > Qshort

print Q

