import copy
from math import exp
import random

class Grating:
    edge_supp = 15 #peak near edge suppresion

    def __init__(self, params, wavelengths):
        self.params = list(params) #order needs to match labels
        self.wls = wavelengths
        self.fom, self.trans = None, None

    def __str__(self):
        strrep = ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(self.labels, self.params)])  
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

        if leftloc > 0 and rightloc < len(self.trans)-1:
            bg = [t for wl, t in self.trans[:leftloc]] + [t for wl, t in self.trans[rightloc:]]
            self.fom = invrms(bg)
            if self.fom > 25:
                peakedge = 1 - exp(-Grating.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                             - exp(-Grating.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                peakedge = max(peakedge, 1/Grating.edge_supp) #if edge suppression is too small, peakedge can become negative at edges
                self.fom *= peakedge*(peak[1]**2)/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

        #debug
        if self.fom < 0:
            print("negative fom: "+str(self))
            self.fom = 0

    def mutate(self):
        child = copy.deepcopy(self)
        childparams = [round(random.gauss(1, 0.1)*p, 4) for p in self.params]
        child.__init__(childparams, self.wls)
        return child

    def crossbreed(self, rhs):
        child = copy.deepcopy(self)
        childparams = [(self.params[i] if random.randint(0,1) else rhs.params[i]) for i in range(len(self.params))]
        child.__init__(childparams, self.wls)
        return child
