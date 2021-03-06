import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from datetime import datetime as dt
from gratings.hcg import HCG
from gratings.zcg import ZCG
from gratings.nirzcg import NIRZCG
from gratings.bizcg import BiZCG
from gratings.blockzcg import BlockZCG
from generation import Generation
from lib.helpers import writecsv

from termcolor import colored

def main():
    gencount = 100

    #dimensions
    d = 1053.7
    ff = 0.5904
    tline = 589.0957
    tslab = 296.6
    tstep = 10.5036


    g0 = NIRZCG((d, ff, tline, tslab, tstep),(1750, 2250, 1001), target = 2000)
    g0.evaluate()
    oldbest = g0
    genbest = list(zip(*g0.trans))
    print(str(dt.time(dt.now())).split('.')[0],colored("seed:", 'cyan'),g0)

    gen = Generation(25, g0)
    for i in range(gencount): 
        #str(dt.time(dt.now())).split('.')[0],colored("gen "+str(i), 'cyan')
        gen._evaluate(progress_txt = (str(dt.time(dt.now())).split('.')[0]+colored(" gen "+str(i), 'cyan')))
        gen = gen.progeny()
        genbest.append([t for wl,t in gen.best.trans])
        if gen.best.fom > oldbest.fom:
            print(colored("new best grating\n", 'green')+str(gen.best))
            oldbest = gen.best

    writecsv("iter_best.csv",list(zip(*genbest)),tuple(["wl",0]+list(range(1,gencount+1))))

if __name__ == "__main__":
    main()
