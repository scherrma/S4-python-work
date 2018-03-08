#!/usr/bin/env python3

import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h
from zcg import ZCG

def main():

    #SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    #si_n = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    #si_k = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))

    #dimensions
    d = 4.8
    tline = 2.7
    tslab = 1.6
    ff= 2/3
    tstep= 0

    g = ZCG((d, ff, tslab, tline, tstep),(8,12,1000))
    print(g)
    print(g.evaluate())


    #plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
