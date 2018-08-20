from lib.generation import Generation
from gratings.zcg import ZCG

import matplotlib.pyplot as plt

def main():
    #dimensions
    d = 4.448
    ff = 0.6516
    tline = 2.268
    tslab = 1.358
    tstep = 0.1785

    g = ZCG((d, ff, tline, tslab, tstep), (8, 12, 2001), target = 10.4)
    g.evaluate()
    print(g)
    print("total trans:",(sum([t**2 for (wl, t) in g.trans])/len(g.trans))**(1/2))
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
