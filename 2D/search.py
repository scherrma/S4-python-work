import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from datetime import datetime as dt
from gratings.zcg2d import ZCG2D
from lib.generation import Generation
from lib.helpers import writecsv
from termcolor import colored
from shapely.geometry import Polygon

def main():
    gencount = 100

    #dimensions
    d = 4.5
    tblocks = 2.23
    tslab = 1.17
    #seedpoly = Polygon([(0, 0), (0, 3/4), (3/4, 3/4), (3/4, 0)])
    seedpoly = Polygon([(0, 0), (0, 0.7515), (0.7515, 0.7515), (0.792, 0.36), (0.9675, 0.126), (0.7515, 0.108), (0.7515, 0.0405), (0.648, 0)])
    g0 = ZCG2D((d, tblocks, tslab), seedpoly, (8,12,201))
    g0.evaluate()
    oldbest = g0
    genbest = list(zip(*g0.trans))
    print(str(dt.time(dt.now())).split('.')[0],colored("seed:", 'cyan'),g0)

    gen = Generation(25, g0)
    for i in range(gencount):
        gen = gen.progeny()
        genbest.append([t for wl,t in gen.best.trans])
        print(str(dt.time(dt.now())).split('.')[0],colored("gen "+str(i), 'cyan'),\
                colored("new best grating\n", 'green')+str(gen.best) if gen.best.fom > oldbest.fom + 0.001 else "")
        oldbest = gen.best

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
