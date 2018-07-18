import S4
from lib.grating import Grating
from math import exp

import numpy as np
import scipy.interpolate as interp
import lib.helpers as h


class BiZCG(Grating):
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths, angle = 5):
        Grating.__init__(self, params, wavelengths)
        self.d, self.ff, self.tline1, self.tline2, self.tslab = params
        if self.tline2 > self.tline1:
            self.tline2, self.tline1 = self.tline1, self.tline2
        self.angle = angle
        self.labels = ['d','ff','tline1','tline2','tslab']
    
    def __str__(self):
        strrep = ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(self.labels, self.params)])  
        strrep += ", angle = "+str(self.angle)+" deg"
        if self.fom:
            strrep += ', fom: '+str(round(self.fom, 4))
        return strrep


    def evaluate(self):
        if self.fom is None:
            S = S4.New(self.d, 20)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later per wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('line1',self.tline1 - self.tline2,"Vacuum")
            S.AddLayer('line2',self.tline2 - self.tslab,"Vacuum")
            S.AddLayer('slab',self.tslab,"Silicon")
            S.AddLayer('bottom', 0, "Vacuum")

            #patterning
            S.SetRegionRectangle('line1','Silicon',(-3*self.d*self.ff/8,0),0,(self.d*self.ff/8,0))
            S.SetRegionRectangle('line2','Silicon',(self.d*self.ff/8,0),0,(self.d*self.ff/8,0))
            S.SetRegionRectangle('line2','Silicon',(self.d*self.ff/8,0),0,(self.d*self.ff/8,0))


            foms, peaks = [], []
            for theta in (0, self.angle):
                self.trans = []
                
                #light
                S.SetExcitationPlanewave((0,0),np.sin(theta),np.cos(theta))
                
                for wl in np.linspace(*self.wls):
                    S.SetFrequency(1/wl)
                    S.SetMaterial('Silicon',complex(BiZCG.si_n(wl),BiZCG.si_k(wl))**2)
                    self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
                self._calcfom()
                foms.append(self.fom)
                peaks.append(self.peak)
            self.fom = min(foms)
            if self.fom > 20:
                self.fom *= exp(-(max(peaks) - min(peaks))/0.05)

        return self.fom
