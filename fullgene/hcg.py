import S4
from lib.grating import Grating

import numpy as np
import scipy.interpolate as interp
import lib.helpers as h

class HCG(Grating):
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths):
        Grating.__init__(self, params, wavelengths)
        self.d, self.ff, self.tline, self.tair, self.tstep = params
        self.labels = ['d','ff','tline','tair','tstep']
    
    def evaluate(self):
        if self.fom is None:
            self.tstep = max(self.tstep, 0.3) #force minimum step size

            S = S4.New(self.d, 20)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later per wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('step',self.tstep,"Vacuum")
            S.AddLayer('lines',self.tline - self.tstep,"Vacuum")
            S.AddLayer('gap',self.tair,"Vacuum")
            S.AddLayer('bottom', 0, "Silicon")

            #patterning
            S.SetRegionRectangle('step','Silicon',(-self.d*self.ff/4,0),0,(self.d*self.ff/4,0))
            S.SetRegionRectangle('lines','Silicon',(0,0),0,(self.d*self.ff/2,0))

            #light
            S.SetExcitationPlanewave((0,0),0,1)

            self.trans = []
            for wl in np.linspace(*self.wls):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon',complex(HCG.si_n(wl),HCG.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
        
        return self.fom
