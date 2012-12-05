#!/usr/bin/python
from __future__ import division
from numpy import *
import numpy as np
from numpy.random import multinomial

# # # # # # # # # # # # # # # # # # # # # # # # 
# MDP


def pick(xs, ps):
    return xs[ argmax(multinomial(1, ps)) ]


class MDP:
    def __init__(self, gamma=0.9, s0=None):
        self.gamma = gamma
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
    S = range(16)

    def A(self, s):
        return ['short', 'long'] if s==0 else ['next']

    def R(self, s,a):
        if   (s,a) == (15,'next'): return 5
        elif (s,a) == (10,'next'): return 20
        else: return 0

    def T(self, s,a):
        if s==0:
            return {'short' : ([11],[1]) , 'long' : ([1],[1]) }[a] 
        elif s==10:
            return ([0],[1])
        elif s==15:
            return ([0],[1])
        else:
            return ([s+1],[1])

