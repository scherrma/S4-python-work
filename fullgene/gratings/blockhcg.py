import S4
from lib.grating import Grating

import numpy as np
import scipy.interpolate as interp
import lib.helpers as h


class BlockHCG(Grating): #2D block HCG
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths):
        Grating.__init__(self, params, wavelengths)
        self.d, self.ff, self.tblocks, self.tair = params
        self.labels = ['d','ff','tblocks', 'tair']
    
    def evaluate(self):
        if self.fom is None:
            S = S4.New(Lattice=((self.d,0), (0, self.d)), NumBasis=20)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later by wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('blocks',self.tblocks,"Vacuum")
            S.AddLayer('airgap',self.tair,"Vacuum")
            S.AddLayer('bottom', 0, "Silicon")

            #patterning
            S.SetRegionRectangle('blocks','Silicon',(0,0),0,(self.d*self.ff/2,self.d*self.ff/2))

            #light
            S.SetExcitationPlanewave((0,0),0,1)

            self.trans = []
            for wl in np.linspace(*self.wls):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon',complex(BlockHCG.si_n(wl),BlockHCG.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
        
        return self.fom
