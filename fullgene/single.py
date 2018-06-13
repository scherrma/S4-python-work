import matplotlib.pyplot as plt

from hcg import HCG
from zcg import ZCG
from lib.generation import Generation

def main():
    #dimensions
    d = 4.7656
    ff = 0.7447
    tline = 3.051
    tslab = 2.3809
    tstep = 0.1177

    g = HCG((d, ff, tline, tslab, tstep),(8,12,2001))
    g.evaluate()
    print(g)
    print("bg: "+str(round(100*(sum([t*t for wl, t in g.trans])/len(g.trans))**(1/2),3))+"%")
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
