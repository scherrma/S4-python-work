import numpy as np
import scipy.interpolate as interp
import lib.helpers as h
import matplotlib.pyplot as plt
import numpy as np

SPEED_OF_LIGHT = 299792458*10**6 #in um/s
si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))
    
saph_n = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_n.csv',1)]))
saph_k = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_k.csv',1)]))
    

sidat = [(wl, si_n(wl)) for wl in np.linspace(3,5,200)]
saphdat = [(wl, saph_n(wl)) for wl in np.linspace(3,5,200)]
print([float(si_n(wl)) for wl in np.linspace(3,5,10)])
print([float(saph_n(wl)) for wl in np.linspace(3,5,10)])
plt.plot(*zip(*sidat), label='Silicon')
plt.plot(*zip(*saphdat), label='Sapphire')
plt.legend()
plt.show()
