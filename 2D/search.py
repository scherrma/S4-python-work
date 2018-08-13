from datetime import datetime as dt
from gratings.zcg2d import ZCG2D
from lib.generation import Generation
from lib.helpers import writecsv
from termcolor import colored
from shapely.geometry import Polygon

def main():
    gencount = 100

    #dimensions
    d = 4.65
    tblocks = 2
    tslab = 1.2
    seedpoly = Polygon([(0, 0), (0, 0.866), (0.433, 0.75), (0.835, 0.539), (0.75, 0.158), (0.866, 0)])
    g0 = ZCG2D((d, tblocks, tslab), seedpoly, (8,12,201))
    g0.evaluate()
    oldbest = g0
    print(str(dt.time(dt.now())).split('.')[0],colored("seed:", 'cyan'),g0)
    genbest = list(zip(*g0.trans))
    gen = Generation(25, g0)

    for i in range(gencount):
        gen = gen.progeny()
        genbest.append([t for wl,t in gen.best.trans])
        print(str(dt.time(dt.now())).split('.')[0],colored("gen "+str(i), 'cyan'),"best grating: "+str(gen.best))

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
