import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import matplotlib.pyplot as plt

from gratings.hcg import HCG
from gratings.zcg import ZCG
from gratings.blockzcg import BlockZCG
from gratings.bizcg import BiZCG
from lib.generation import Generation
from gratings.nirzcg import NIRZCG

def main():
    #dimensions
    d = 1053.7
    ff = 0.5904
    tline = 589.0957
    tslab = 296.6
    tstep = 10.5036

    g = NIRZCG((d, ff, tline, tslab, tstep), (1981, 1983, 1001), target = 2000)
    g.evaluate()
    print(g)
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
