#!/usr/bin/python

import q
import r
import time
from matplotlib.pyplot import *

import argparse
cl = argparse.ArgumentParser()
cl.add_argument('-save', action='store_true', dest='save', default=False)
args = cl.parse_args()

curves = {}
for gamma in [0.70, 0.90, 0.99]:
    _, (curves['g'+('%.2f' % gamma)[2:]],) = q.main(gamma)
_, (curves['r'],) = r.main()

legend(curves.values(), curves.keys(), loc=1)
print
print curves
show() if args.save else time.sleep(60)
