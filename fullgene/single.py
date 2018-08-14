import matplotlib.pyplot as plt

from gratings.hcg import HCG
from gratings.zcg import ZCG
from gratings.blockzcg import BlockZCG
from gratings.bizcg import BiZCG
from lib.generation import Generation
from gratings.nirzcg import NIRZCG

def main():
    #dimensions
    #d = 4.95
    #ff = 0.57
    #tblocks = 3.11
    #tline2 = 1
    #tslab = 1.82
    #tstep = 0.1177

    d = 1053.7
    ff = 0.5658
    tline = 566.3
    tslab = 283.6
    tstep = 10.1
    g = NIRZCG((d, ff, tline, tslab, tstep), (1750, 2250, 2001), target = 2000)
    g.evaluate()
    print(g)
    #print("fom:",g.fom)
    #print("bg: "+str(round(100*(sum([t*t for wl, t in g.trans])/len(g.trans))**(1/2),3))+"%")
    #g.fom = None
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
