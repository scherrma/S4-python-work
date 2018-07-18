from datetime import datetime as dt
from gratings.hcg import HCG
from gratings.zcg import ZCG
from gratings.bizcg import BiZCG
from gratings.blockzcg import BlockZCG
from lib.generation import Generation
from lib.helpers import writecsv

def main():
    gencount = 100

    #dimensions
    d = 4.8
    ff = 0.63
    tline1 = 4.65
    tline2 = 1.25
    tslab = 2
    #tstep = 0.1
    base_muta_rate = 0.1
    muta_growth_rate = 1.1

    g0 = BiZCG((d, ff, tline1, tline2, tslab),(8,12,1001), angle = 3)
    g0.evaluate()
    oldbest = g0
    print("seed:",g0)
    genbest = list(zip(*g0.trans))
    gen = Generation(25, g0, mutation_rate = base_muta_rate, elite = 3)

    for i in range(gencount):
        gen = gen.progeny()
        genbest.append([t for wl,t in gen.best.trans])
        if gen.best == oldbest:
            gen.muta_rate = round(min(gen.muta_rate*muta_growth_rate, 0.9-(0.9-gen.muta_rate)*(2-muta_growth_rate)), 4)
        else:
            gen.muta_rate = base_muta_rate
            oldbest = gen.best
        print(str(dt.time(dt.now())).split('.')[0],"gen",i,"best grating: "+str(gen.best))

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
