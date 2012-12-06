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

def Qlearning(mdp, n=inf, gamma=0.9, alpha=0.001, eps=0.01, explore=0.001, debug=True):
    print
    print
    print 'Q LEARNING...'

    # init
    Q = { s : { a : 0  for a in mdp.A(s) }  for s in mdp.S }

    def V(s_): return max( Q[s_][a_] for a_ in mdp.A(s_) )
    
    exploit = 1-explore

    i, diff, rs = 0, inf, zeros(n)
    
    # loop
    while i < n: #and diff > eps:

        if mdp.s == s0:
            # on policy
            P = long  if Q[s0]['short'] < Q[s0]['long']  else short
            notP = short if P==long else long
            
            # off policy
            P = pick( [P, notP], [exploit, explore] ) # epsilon greedy exploration
            #print P.__name__
            
        s,a,r,s_ = mdp.run(P)
        
        #Qsa = Q[s][a]
        Q[s][a]  =  Q[s][a] * (1-alpha)  +  alpha * (r + gamma * V(s_) )
        #diff = Qsa - Q[s][a]

        rs[i] = r
        i+=1
        
    return Q,i,rs

# # # # # # # # # # # # # # # # # # # # # # 
# Main

#TODO tune params: explore?, alpha, beta
def main(gamma):
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
    alpha   = args.alpha if args.alpha else 0.9
    eps     = 0.01
    explore = 0.01

    begin = clock()
    Q,iters,rewards = Qlearning(mdp, n=n, gamma=gamma, alpha=alpha, eps=eps, explore=explore, debug=False)
    finish = clock()
    
    means1000(rewards, args.save)
    
    print
    print 'time = %.3fs' % (finish - begin)
    print 'gamma =', gamma
    print 'mean  =', mean(rewards)
    print 'iters =', iters
    Qlong, Qshort = Q[s0]['long'], Q[s0]['short']
    print 'Qlong  =', Qlong
    print 'Qshort =', Qshort
    print Qlong > Qshort
    
    print
    print 'Q ='
    print Q
    

if __name__=='__main__':
    for gamma in [0.7, 0.9, 0.99]:
        main(gamma)
    
    if args.save:
        show()
    else:
        sleep(60)

