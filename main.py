#!/usr/bin/python

import q
import r
import time
from matplotlib.pyplot import *

import argparse
cl = argparse.ArgumentParser()
cl.add_argument('-save', action='store_true', dest='save', default=False)
args = cl.parse_args()

for gamma in [0.70, 0.90, 0.99]: q.main(gamma)
r.main()

show() if args.save else time.sleep(60)
