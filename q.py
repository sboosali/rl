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

def Qlearning(mdp, n=inf, gamma=0.9, alpha=0.1, eps=0.01, explore=0.1, debug=True):
    print
    print
    print 'Q LEARNING...'

    # init
    Q = { s : dict.fromkeys(mdp.A(s), 0)  for s in mdp.S }
    def V(s_): return max( Q[s_][a_] for a_ in mdp.A(s_) )

    exploit = 1-explore

    i, diff, ms = 0, inf, zeros(n+1)
    
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
        
        #Qsa = Q[s][a]
        Q[s][a]  =  Q[s][a] * (1-alpha)  +  alpha * (r + gamma * V(s_) )
        #diff = Qsa - Q[s][a]

        ms[i] = (ms[i-1]*i + r) / (i+1)
        if debug and i%100 == 0 and ms[i]<1.8: print i,ms[i]
        
    return Q,i,ms

# # # # # # # # # # # # # # # # # # # # # # 
# Main

#TODO tune params: explore?, alpha, beta
def main(gamma):
    mdp = FeynmanFetch()

    global s0
    s0 = mdp.S[0]

    n       = 40*1000
    alpha   = 0.9
    eps     = 0.01
    explore = 0.1

    begin = clock()
    Q,iters,means = Qlearning(mdp, n=n, gamma=gamma, alpha=alpha, eps=eps, explore=explore, debug=False)
    finish = clock()

    ion()
    plot(means)
    draw()

    print
    print 'time = %.3fs' % (finish - begin)
    print 'gamma =', gamma
    print 'mean  =', means[-1]
    print 'iters =', iters
    Qlong, Qshort = Q[s0]['long'], Q[s0]['short']
    print 'Qlong  =', Qlong
    print 'Qshort =', Qshort
    print Qlong > Qshort
    
    print
    print 'Q ='
    print Q
    

for gamma in [0.7, 0.9, 0.99]:
    main(gamma)

sleep(60)
