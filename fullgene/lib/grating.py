from math import exp
import scipy.interpolate as interp
import lib.helpers as h
import random
import copy

class Grating:
    edge_supp = 15 #peak near edge suppresion

    SPEED_OF_LIGHT = 299792458*10**6 #in um/s
    si_n = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((299792458*10**6)/float(f)),n] for f,n in h.opencsv('../matdat/silicon_k.csv',1)]))
    
    saph_n = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_n.csv',1)]))
    saph_k = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/al2o3_k.csv',1)]))
    
    caf2_n = interp.interp1d(*zip(*[[float(f)*(10**6),n] for f,n in h.opencsv('../matdat/caf2_n.csv',1)]))

    def __init__(self, params, wavelengths):
        self.params = params #list of pairs, form: [('name', value), ...]
        self.wls = wavelengths
        self.fom, self.trans = None, None

    def __str__(self):
        strrep = ', '.join([l+' = '+str(v) for l, v in params])  
        if self.fom:
            strrep += ', fom: '+str(round(self.fom, 4))
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
                peakedge = 1 - exp(-ZCG.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                             - exp(-ZCG.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                self.fom *= peakedge*(peak[1]**2)/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

    def mutate(self):
        child = copy.deepcopy(self)
        child.fom, child.trans = None, None

        for i in range(len(params)):
            self.params[i][1] = round(random.gauss(1, 0.05)*self.params[i][1], 4)

        return child
