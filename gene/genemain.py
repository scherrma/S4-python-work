import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h
from hcg import HCG

def main():
    gensize = 50
    elite = round(gensize**(1/2))
    gencount = 100

    #dimensions
    d = 4.86
    ff = 2/3
    tline = 2.25
    tair = 1.83
    tstep = 0.085

    g0 = HCG((d, ff, tline, tair, tstep),(8,12,3001))
    gen = [g0] + [g0.mutate() for i in range(gensize-1)]

    for i in range(gencount):
        nextgen = sorted(gen, key=lambda x: x.evaluate(), reverse=True)[:elite]
        print("gen",i,"best grating:",str(nextgen[0]))
        nextgen += [nextgen[i%elite].mutate() for i in range(elite, gensize)]
        gen = nextgen

if __name__ == "__main__":
    main()
