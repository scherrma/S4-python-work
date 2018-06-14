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
    ff = 0.74
    fhi = 1/4
    
    #vertical dimensions
    tline = 2.7
    tair = 4
    tstep = 0.3

    #material properties
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))
    
    #S4
    for numG in range(1, 6):
        #create simulation, basic layers
        S = S4.New(d*numG,30)
        S.AddMaterial("Vacuum",1)
        S.AddMaterial("Silicon",complex(12.1,2*10**-4))
        
        S.AddLayer('top',0,"Vacuum")
        S.AddLayer('step',tstep,"Vacuum")
        S.AddLayer('lines',tline-tstep,"Vacuum")
        S.AddLayer('airgap',tair,"Vacuum")
        S.AddLayer('bottom',0,'Silicon')
        
        #patterning (remember, period is already baked into cent and fill)
        print("numG:",numG)
        for cent in [j + (0 if numG%2 else 1/2) for j in range((1-numG)//2, (1+numG)//2)]:
            print("line",cent,"is centered on", d*cent, "and is", d*ff/2, "halfwide")
            print("step",cent,"is centered on", d*(cent+ff*(1-fhi)/2), "and is", d*ff*fhi/2, "halfwide")
            S.SetRegionRectangle('lines','Silicon', Angle = 0,\
                    Center = (d*cent,0), Halfwidths = (d*ff/2,0))
            S.SetRegionRectangle('step','Silicon', Angle = 0,\
                    Center = (cent+ff*(1-fhi)/2,0), Halfwidths = (d*ff*fhi/2,0))
        
        #excitation and measurement
        S.SetExcitationPlanewave((0,0),0,1)
        
        trans = []
        wavelengths = np.linspace(7,13,21)
        for wl in wavelengths:
            S.SetFrequency(1/wl)
            S.SetMaterial('Silicon',complex(si_n(wl),si_k(wl))**2)
            trans.append(float(np.real(S.GetPowerFlux('bottom')[0]))) 
        plt.plot(wavelengths,trans, label = "numG: "+str(numG))
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
