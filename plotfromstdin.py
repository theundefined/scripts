#!/usr/bin/python
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

fig=plt.figure()
plt.axis([0,1000,0,255])

i=0

plt.ion()
plt.show()

for value in sys.stdin:
    plt.scatter(i,int(value),s=1)
    i+=1
    plt.draw()
#    time.sleep(0.05)
