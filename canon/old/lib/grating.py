import copy
from math import exp, isclose
import random

class Grating:

    def __init__(self, params, wavelengths, target = None):
        self.params = list(params) #order needs to match labels
        self.wls = wavelengths
        self.target = target
        self.labels, self.fom, self.trans = None, None, None
        self.edge_supp = 15 #peak near edge suppresion

    def __str__(self):
        strrep = ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(self.labels, self.params)])  
        if self.peak:
            strrep += ', peak: ' + str(round(100*self.peak[1], 1)) + "% at " + str(round(self.peak[0]))\
                    + "; " + str(round(self.linewidth, 2)) + " wide"
        if self.fom:
            strrep += ', fom: ' + str(round(self.fom, 4))
        return strrep

    def __eq__(self, rhs):
        if self.__class__ != rhs.__class__:
            return False
        if self.wls != rhs.wls:
            return False
        for lhsval, rhsval in zip(self.params, rhs.params):
            if not isclose(lhsval, rhsval):
                return False
        return True

    def _calcfom(self):
        self.peak = None
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
        
        if leftloc > 0 and rightloc < len(self.trans) and (rightwl - leftwl)/(self.wls[1] - self.wls[0]) < 1/3:
            bg = [t for wl, t in self.trans[:leftloc]] + [t for wl, t in self.trans[rightloc:]]
            self.fom = invrms(bg)
            if self.fom > 20:
                self.peak = peak
                self.linewidth = rightwl - leftwl
                if self.target:
                    peakedge = exp(-self.edge_supp*abs(peak[0]-self.target)/(self.wls[1]-self.wls[0]))
                else:
                    peakedge = 1 - exp(-self.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                            - exp(-self.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                self.fom *= peakedge*(peak[1]**2)*(self.wls[1] - self.wls[0])/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

        #debug
        if self.fom < 0:
            print("target:", self.target)
            print("negative fom: "+str(self))
            print("peakedge: " + str(round(peakedge, 3)))
            self.fom = 0

    def mutate(self):
        child = copy.deepcopy(self)
        childparams = [round(random.gauss(1, 0.1)*p, 4) for p in self.params]
        child.__init__(childparams, self.wls, self.target)
        return child

    def crossbreed(self, rhs):
        child = copy.deepcopy(self)
        childparams = [(self.params[i] if random.randint(0,1) else rhs.params[i]) for i in range(len(self.params))]
        child.__init__(childparams, self.wls, self.target)
        return child
