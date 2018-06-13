#!/usr/bin/env python3

import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h

from hcg import HCG

def main():
    
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    #dimensions
    d = 4.7333
    ff= 2/3
    tline = 2.5925
    tair = 2.2285
    tstep= 0.1071
    
    g = HCG((d, ff, tline, tair, tstep), (9.55,9.6,3001))
    g.evaluate()
    print(g)
    plt.plot(*zip(*g.trans))
    plt.show()


if __name__ == "__main__":
    main()
