import S4
import numpy as np
import scipy.interpolate as interp
import lib.helpers as h
import random

class ZCG:
    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))

    def __init__(self, params, wavelengths):
        self.d, self.ff, self.tslab, self.tline, self.tstep = params
        self.wavelengths = wavelengths
        self.fom, self.trans = None, None

    def __str__(self):
        lbls = ('d', 'ff', 'tline', 'tslab', 'tstep')
        vals = (self.d, self.ff, self.tline, self.tslab, self.tstep)
        return ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(lbls, vals)])
        #return ('d = '+str(self.d)+', ff = '+str(self.ff)+', tslab = '+str(self.tslab)+
        #       ', tline = '+str(self.tline)+', tstep = '+str(self.tstep))

    def _calcfom(self):
        self.fom = 100*(sum([t**2 for wl,t in self.trans])/len(self.trans))**(1/2)

    def evaluate(self):
        if self.fom is None:
            S = S4.New(self.d, 30)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later per wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('step',self.tstep,"Vacuum")
            S.AddLayer('lines',self.tline - self.tstep,"Vacuum")
            S.AddLayer('slab',self.tslab,"Silicon")
            S.AddLayerCopy('bottom',0,'top')

            #patterning
            S.SetRegionRectangle('step','Silicon',(-self.d*self.ff/4,0),0,(self.d*self.ff/4,0))
            S.SetRegionRectangle('lines','Silicon',(0,0),0,(self.d*self.ff/2,0))

            #light
            S.SetExcitationPlanewave((0,0),0,1)

            self.trans = []
            for wl in np.linspace(*self.wavelengths):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon',complex(ZCG.si_n(wl),ZCG.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
        
        return self.fom

    def mutate(self):

