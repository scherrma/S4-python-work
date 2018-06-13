import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
import lib.helpers as h


def main():

    saph_n = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_n.csv',1)]))
    saph_k = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_k.csv',1)]))
    
    kdat = [(wl, saph_n(wl)) for wl in np.linspace(2, 14, 251)]
    plt.plot(*zip(*kdat))
    plt.show()

if __name__ == "__main__":
    main()
