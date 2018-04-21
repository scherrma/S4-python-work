from hcg import HCG
from lib.generation import Generation

def main():
    gencount = 100

    #dimensions
    d = 4.86
    ff = 2/3
    tline = 2.25
    tair = 1.83
    tstep = 0.085

    g0 = HCG((d, ff, tline, tair, tstep),(8,12,2001))
    g0.evaluate()
    gen = Generation(25, g0, 0.1, 3)

    for i in range(gencount):
        print("gen",i,"best grating: "+str(gen.best()[0]))
        gen = gen.progeny()

if __name__ == "__main__":
    main()
