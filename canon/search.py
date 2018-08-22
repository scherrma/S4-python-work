from datetime import datetime as dt
from lib.generation import Generation
from lib.helpers import writecsv
from termcolor import colored

from gratings.zcg import ZCG
from gratings.hcg import HCG
from gratings.nirzcg import NIRZCG

def main():
    gencount = 100
    gensize = 20

    #dimensions
    d = 4.448
    ff = 0.6516
    tline1 = 2
    tline2 = 1
    tslab = 2
    angle = 3
    g = BiZCG((d, ff, tline1, tline2, tslab, angle), (8, 12, 21), target = 10)


    g0.evaluate()
    print(colored("seed:", "cyan"), g0)

    oldbest = g0
    genbest = list(zip(*g0.trans))
    gen = Generation(gensize, g0)

    thetime = lambda: str(dt.time(dt.now())).split('.')[0]
    for i in range(gencount): 
        genheader = thetime() + colored( " gen " + str(i), "cyan")
        gen.evaluate(progress_txt = genheader)
        gen = gen.progeny()
        print(genheader)
        genbest.append([t for wl,t in gen.best.trans])
        if gen.best.fom > oldbest.fom:
            print(colored("new best grating\n", 'green') + str(gen.best))
            oldbest = gen.best

    writecsv("iter_best.csv",list(zip(*genbest)), ("wl",0) + tuple(range(1,gencount+1)))

if __name__ == "__main__":
    main()
