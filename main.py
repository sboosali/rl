#!/usr/bin/python

import q
import r
import time

#r.main()
#for gamma in [0.70, 0.90, 0.99]: q.main(gamma)

r.main()
for gamma in [0.70, 0.75, 0.80, 0.85, 0.90]:
    print gamma
    q.main(gamma)

time.sleep(60)
