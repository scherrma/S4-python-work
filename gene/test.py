#!/usr/bin/env python3

import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h

from zcg import ZCG

def main():
    
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    #dimensions
    d = 1.7142
    ff= 0.4371
    tline = 1.1843
    tslab = 0.6664
    tstep= 0.073
    
    g = ZCG((d, ff, tslab, tline, tstep), (3,5,2001))
    g.evaluate()
    print(g.fom)
    plt.plot(*zip(*g.trans))
    plt.show()


if __name__ == "__main__":
    main()
