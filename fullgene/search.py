from hcg import HCG
from zcg import ZCG
from blockzcg import BlockZCG
from lib.generation import Generation
from lib.helpers import writecsv

def main():
    gencount = 100

    #dimensions
    d = 4
    ff = 1/2
    tblock = 2
    tslab = 2
    #tstep = 0.1

    g0 = BlockZCG((d, ff, tblock, tslab),(8,12,1001))
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
