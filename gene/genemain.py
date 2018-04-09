import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h
from zcg import ZCG

def main():
    gensize = 50
    elite = round(gensize**(1/2))
    gencount = 100

    #dimensions
    d = 1.85
    ff = 0.575
    tslab = 1
    tline = 1
    tstep= 0.1

    g0 = ZCG((d, ff, tslab, tline, tstep),(3,5,2001))
    gen = [g0] + [g0.mutate() for i in range(gensize-1)]

    for i in range(gencount):
        nextgen = sorted(gen, key=lambda x: x.evaluate(), reverse=True)[:elite]
        print("gen",i,"best grating:",str(nextgen[0]))
        nextgen += [nextgen[i%elite].mutate() for i in range(elite, gensize)]
        gen = nextgen

if __name__ == "__main__":
    main()
