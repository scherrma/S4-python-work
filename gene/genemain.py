#!/usr/bin/env python3

import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h
from zcg import ZCG

def main():
    #dimensions
    d = 4.548
    tline = 2.7
    tslab = 1.685
    ff = 2/3
    tstep= 0

    g0 = ZCG((d, ff, tslab, tline, tstep),(8,12,1000))
    gen = [g0] + [g0.mutate() for i in range(10)]

    for g in gen:
        g.evaluate()
        print(g)

    #plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
