#!/usr/bin/env python3

import S4
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import lib.helpers as h

def main():

    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    #dimensions
    d = 4.8
    tline = 2.7
    tslab = 1.6
    ff=2/3

    si_n = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_k.csv',1)]))

    for a in 'a':#np.linspace(0, 0.3, 6):
        #create simulation
        S = S4.New(d,30)

        #materials
        S.AddMaterial("Vacuum",1)
        S.AddMaterial("Silicon",complex(12.1,2*10**-4))

        #layers
        S.AddLayer('top',0,"Vacuum")
        S.AddLayer('lines',tline,"Vacuum")
        S.AddLayer('slab',tslab,"Silicon")
        S.AddLayerCopy('bottom',0,'top')

        #patterning
        S.SetRegionRectangle('lines','Silicon',(0,0),0,(d*ff/2,0))

        #light
        S.SetExcitationPlanewave((0,0),0,1)

        trans = []
        wavelengths = np.linspace(7,13,500)
        for wl in wavelengths:
            S.SetFrequency(1/wl)
            S.SetMaterial('Silicon',complex(si_n(wl),si_k(wl))**2)
            trans.append(float(np.real(S.GetPowerFlux('bottom')[0]))) 

        h.writecsv('d48_tline27_tslab16_ff667.csv', zip(wavelengths, trans), ['Wavelength (um)','Transmittance'])
        plt.plot(wavelengths,trans, label='tline='+str(tline))

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

