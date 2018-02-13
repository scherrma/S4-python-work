#!/usr/bin/env python3

import S4
import numpy as np
import matplotlib.pyplot as plt

def main():
    #dimensions
    d = 4.8
    tline = 3.3
    tslab = 1.7
    ff = 0.5

    #create simulation
    S = S4.New(1,20)

    #materials
    S.AddMaterial("Vacuum",1)
    S.AddMaterial("Silicon",complex(3.42,2*10**-4))

    #layers
    S.AddLayer('top',0,"Vacuum")
    S.AddLayer('lines',tline/d,"Vacuum")
    S.AddLayer('slab',tslab/d,"Silicon")
    S.AddLayerCopy('bottom',0,'top')

    #patterning
    S.SetRegionRectangle('lines','Silicon',(0,0),0,(ff/2,9999))

    #light
    S.SetExcitationPlanewave((0,0),0,1)

    trans = []
    wavelengths = np.linspace(8,12,200)
    for wl in wavelengths:
        S.SetFrequency(d/wl)
        trans.append(float(np.real(S.GetPowerFlux('bottom')[0]))) 

    plt.plot(wavelengths,trans)
    plt.show()


if __name__ == "__main__":
    main()
