#import matplotlib.pyplot as plt

from gratings.hcg import HCG
from gratings.zcg import ZCG
from gratings.blockzcg import BlockZCG
from gratings.bizcg import BiZCG
from lib.generation import Generation

def main():
    #dimensions
    d = 4.95
    ff = 0.57
    tline1 = 3.11
    tline2 = 1
    tslab = 1.82
    #tstep = 0.1177

    g = BiZCG((d, ff, tline1, tline2, tslab),(8,12,1001))
    g.evaluate()
    print("fom:",g.fom)
    print("bg: "+str(round(100*(sum([t*t for wl, t in g.trans])/len(g.trans))**(1/2),3))+"%")
    g.fom = None
    #plt.plot(*zip(*g.trans))
    #plt.show()

if __name__ == "__main__":
    main()
