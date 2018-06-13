import S4
from math import exp
import numpy as np
import scipy.interpolate as interp
import lib.helpers as h
import random
import copy

class HCG:
    edge_supp = 15 #peak near edge suppresion

    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))
    
    def __init__(self, params, wavelengths):
        self.d, self.ff, self.tline, self.tair, self.tstep = params
        self.wls = wavelengths
        self.fom, self.trans = None, None

    def __str__(self):
        lbls = ('d', 'ff', 'tline', 'tair','tstep') #, 'tstep')
        vals = (self.d, self.ff, self.tline, self.tair,self.tstep) #, self.tstep)

        strrep = ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(lbls, vals)])  
        strrep += ', fom: '+str(round(self.fom, 4)) if self.fom is not None else ''
        return strrep

    def _calcfom(self):
        invrms = lambda x: (sum([a**2 for a in x])/len(x))**(-1/2)

        peak = max(self.trans, key=lambda x:x[1])
        leftloc = rightloc = peakloc = self.trans.index(peak)
        while self.trans[leftloc][1] > peak[1]/2 and leftloc > 0:
            leftloc -= 1
        leftwl = self.trans[leftloc][0] + (self.trans[leftloc+1][0]-self.trans[leftloc][0])\
                *(peak[1]/2-self.trans[leftloc][1])/(self.trans[leftloc+1][1]-self.trans[leftloc][1])
        while self.trans[rightloc][1] > peak[1]/2 and rightloc < len(self.trans)-1:
            rightloc += 1
        rightwl = self.trans[rightloc][0] + (self.trans[rightloc][0]-self.trans[rightloc-1][0])\
                *(self.trans[rightloc][1]-peak[1]/2)/(self.trans[rightloc][1]-self.trans[rightloc-1][1])

        if leftloc > 0 and rightloc < len(self.trans):
            bg = [t for wl, t in self.trans[:leftloc]] + [t for wl, t in self.trans[rightloc:]]
            self.fom = invrms(bg)
            if self.fom > 25:
                peakedge = 1 - exp(-HCG.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                             - exp(-HCG.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                self.fom *= peakedge*(peak[1]**2)/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

    def evaluate(self):
        if self.fom is None:
            S = S4.New(self.d, 20)
        
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later per wavelength

            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('step',self.tstep,"Vacuum")
            S.AddLayer('lines',self.tline - self.tstep,"Vacuum")
            S.AddLayer('air gap',self.tair,"Vacuum")
            S.AddLayer('bottom',0,"Silicon")

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

    def mutate(self):
        child = copy.deepcopy(self)
        child.fom, child.trans = None, None

        z = lambda x: round(x*random.gauss(1, 0.05), 4)
        child.d = z(child.d)
        #child.ff = z(child.ff)
        child.tline = z(child.tline)
        child.tair = z(child.tair)
        child.tstep = z(child.tstep)
        return child
