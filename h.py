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

def Hlearning(mdp, n=inf, beta=0.8, delta=0.9, alpha=0.01, diff=0.0001, explore=0.01, debug=True):
    print
    print
    print 'H LEARNING...'
    
    # init
    Q = { s : { a : 0  for a in mdp.A(s) }  for s in mdp.S }
    H = { s : { a : 0  for a in mdp.A(s) }  for s in mdp.S }

    def V(s_): return max( H[s_][a_] for a_ in mdp.A(s_) )
    
    exploit = 1-explore

    i, rs = 0, zeros(n)
    
    # loop
    while i < n: #and diff > delta:

        if mdp.s == s0:
            # on policy
            P    = long  if H[s0]['short'] < H[s0]['long']  else short
            notP = short if P==long                         else long
            
            # off policy
            P = pick( [P, notP], [exploit, explore] ) # epsilon greedy exploration
            #print P.__name__
            
        s,a,r,s_ = mdp.run(P)

        H[s][a]  =  H[s][a] * (1-alpha)  +  alpha * (r + beta * delta * V(s_) )
        Q[s][a]  =  Q[s][a] * (1-alpha)  +  alpha * (r + delta        * V(s_) )

        rs[i] = r
        i+=1

    # H is a monotonic function of Q, thus trivial
    return H,Q,i,rs

# # # # # # # # # # # # # # # # # # # # # # 
# Main

#TODO tune params: explore?, alpha, beta
def main(beta, delta, mdp):
    
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
    alpha   = args.alpha if args.alpha else 0.5
    eps     = 0.01
    
    begin = clock()
    H, Q, iters, rewards = Hlearning(mdp, n=n, beta=beta, delta=delta, alpha=alpha, diff=diff, explore=eps, debug=False)
    finish = clock()
    
    title(r'n=%d $\beta=%.4f$ $\delta=%.4f$ $\alpha$=%.4f $\epsilon$=%.4f' 
          % (n, beta, delta, alpha, eps))
    means1000(rewards, args.save)
    
    print
    print 'time = %.3fs' % (finish - begin)
    print 'beta  =', beta
    print 'delta =', delta
    print 'mean  =', mean(rewards)
    print 'iters =', iters
    Hlong, Hshort = H[s0]['long'], H[s0]['short']
    print 'Hlong  =', Hlong
    print 'Hshort =', Hshort
    print Hlong > Hshort
    
    print
    print 'H ='
    print H

    print
    print 'H s a  =  R s a * (1-beta)  +  beta * Q s a'

    print
    print 'H[l10][next] =', H['l10']['next']
    print 'Q[l10][next] =', Q['l10']['next'] * beta + mdp.R('l10','next') * (1-beta)

    print
    print 'H[s5][next] =', H['s5']['next']
    print 'Q[s5][next] =', Q['s5']['next'] * beta + mdp.R('s5','next') * (1-beta)

    return H,Q
    

if __name__=='__main__':
    for beta,delta in [(0.80, 0.90), (0.90, 0.95)]:
        mdp = FeynmanFetch()
        #mdp = AllaisParadox()
        main(beta, delta, mdp)

    show() if args.save else sleep(60)

