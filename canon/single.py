from lib.generation import Generation
import matplotlib.pyplot as plt

from gratings.zcg import ZCG
from gratings.nirzcg import NIRZCG
from gratings.hcg import HCG
from gratings.blockzcg import BlockZCG
from gratings.bizcg import BiZCG


def main():
    #dimensions
    d = 4.448
    ff = 0.6516
    tline1 = 2
    tline2 = 1
    tslab = 2
    angle = 3

    g = BiZCG((d, ff, tline1, tline2, tslab, angle), (8, 12, 21), target = 10)
    g.evaluate()
    print(g)
    #print("RMS trans: {:.1%}".format((sum([t**2 for (wl, t) in g.trans])/len(g.trans))**(1/2)))
    #plt.plot(*zip(*g.trans))
    #plt.show()

if __name__ == "__main__":
    main()
