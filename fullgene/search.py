from hcg import HCG
from zcg import ZCG
from lib.generation import Generation
from lib.helpers import writecsv

def main():
    gencount = 100

    #dimensions
    d = 4
    ff = 2/3
    tline = 2
    tslab = 2
    tstep = 0.1

    g0 = HCG((d, ff, tline, tslab, tstep),(8,12,2001))
    g0.evaluate()
    genbest = list(zip(*g0.trans))
    gen = Generation(50, g0, elite = 3)

    for i in range(gencount):
        genbest.append([t for wl,t in gen.best()[0].trans])
        print("gen",i,"best grating: "+str(gen.best()[0]))
        gen = gen.progeny()

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
