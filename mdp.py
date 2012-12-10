#!/usr/bin/python
from __future__ import division
from numpy import *
import numpy as np
from numpy.random import multinomial
from matplotlib.pyplot import *

# # # # # # # # # # # # # # # # # # # # # # # # 
# MDP

def argmax(xs, f):
    return xs[ np.argmax(f(xs)) ]

def pick(xs, ps):
    return xs[ np.argmax(multinomial(1, ps)) ]

def means1000(rewards, save=False):
    means1000 = zeros(rewards.size - 1000)
    for i in xrange(means1000.size):
        means1000[i] = mean(rewards[i-1000 : i])

    ioff() if save else ion()

    axis([0, rewards.size]+[0, 2.5])
    plot(means1000)
    draw()
    

class MDP:
    def __init__(self, s0=None):
        self.s     = s0 if s0 else self.S[0]
        
    S = []

    def A(self,s): pass

    def R(self, s,a): pass

    #:: State, Action => Multinomial(State)
    # (States, Probs) = Multinomial(State)
    def T(self, s,a): pass

    # Probs => multinomial => States
    def next(self, multistate):
        states, probs = multistate
        return pick(states, probs)

    # policy => (s,a,r,s')
    def run(self, P):
        s = self.s
        a = P(s)
        r = self.R(s,a)
        s_ = self.next(self.T(s,a))

        self.s = s_
        return s,a,r,s_



class FeynmanFetch(MDP):
    home   = ['h1']
    shorts = ['s2', 's3', 's4', 's5']
    longs  = ['l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'l10']
    S = home + shorts + longs

    def A(self, s):
        return ['short', 'long'] if s=='h1' else ['next']

    def R(self, s,a):
        if   (s,a) == (self.shorts[-1],'next'): return 5
        elif (s,a) == (self.longs [-1],'next'): return 20
        else: return 0

    def inc(self, s):
        x, i = s[0], int(s[1:])
        return x+str(i+1)
    
    def T(self, s,a):

        if s=='h1':
            return {'short' : ([self.shorts[0]],[1]) ,
                    'long'  : ([self.longs [0]],[1]) }[a] 

        elif s==self.shorts[-1]:
            return (['h1'],[1])

        elif s==self.longs[-1]:
            return (['h1'],[1])

        else:
            return ([self.inc(s)],[1])




class TimeInconsistent(mdp):
    pass



class AllaisParadox(mdp):
    pass

