#!/usr/bin/env python3
import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h

from random import gauss
from itertools import accumulate

def main():
    #parameters
    #numG = 3
    
    #horizontal dimensions
    d = 4.3
    d_stddev = 0/100
    ff = 0.74
    ff_stddev = 0/100
    fhi = 1/2
    
    #vertical dimensions
    tline = 2.7
    tair = 4
    tstep = 0.3

    #material properties
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_k.csv',1)]))

    for numG in (1,3,5):
        #generate the grating lines; period is baked in
        pds = list(accumulate([0]+[d*gauss(1, d_stddev) for i in range(numG-1)]))
        pds = [i - (pds[0]+pds[-1])/2 for i in pds]
        fills = [round(d*ff*gauss(1, ff_stddev),3) for i in range(numG)]
        lines = list(zip(pds, fills))
        
        #S4
        #create simulation, basic layers
        print("size (ish):",2*pds[-1] + d)
        S = S4.New(2*pds[-1] + d*gauss(1, d_stddev),30)
        S.AddMaterial("Vacuum",1)
        S.AddMaterial("Silicon",complex(12.1,2*10**-4))
        
        S.AddLayer('top',0,"Vacuum")
        S.AddLayer('step',tstep,"Vacuum")
        S.AddLayer('lines',tline-tstep,"Vacuum")
        S.AddLayer('airgap',tair,"Vacuum")
        S.AddLayer('bottom',0,'Silicon')
        
        #patterning (remember, period is already baked into cent and fill)
        print(lines)
        for (cent, fill) in lines:
            S.SetRegionRectangle('lines','Silicon',(cent,0),0,(fill/2,0))
            S.SetRegionRectangle('step','Silicon',(cent+fill*(1-fhi)/2,0),0,(fill*fhi/2,0))
        
        #excitation and measurement
        S.SetExcitationPlanewave((0,0),0,1)
        
        trans = []
        wavelengths = np.linspace(7,13,1001)
        for wl in wavelengths:
            S.SetFrequency(1/wl)
            S.SetMaterial('Silicon',complex(si_n(wl),si_k(wl))**2)
            trans.append(float(np.real(S.GetPowerFlux('bottom')[0]))) 
        plt.plot(wavelengths,trans, label = "numG: "+str(numG))
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
