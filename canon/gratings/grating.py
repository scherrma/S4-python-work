import copy
from math import exp, isclose
import random

class Grating:

    def __init__(self, params, wavelengths, target = None):
        self.params, self.wls = list(params), wavelengths
        self.labels, self.fom, self.trans, self.peak = 4*(None,)
        if target is not None:
            self.target = target
        else:
            self.target = ((self.wls[0] + self.wls[1]) / 2, 0.01 * (self.wls[1] - self.wls[0]))
        self.edge_supp = 15 #peak near edge suppresion

    def __str__(self):
        strrep = ', '.join(["{} = {:.4g}".format(l, v) in zip(self.labels, self.params)])
        if self.peak:
            strrep += ", peak at {:.2f}; {:.1%} tall and {:.3g} wide".format(*self.peak, self.linewidth)
        if self.fom:
            strrep += ', fom: {:.4g}'.format(self.fom)
        return strrep

    def __eq__(self, rhs):
        if self.__class__ != rhs.__class__ or self.wls != rhs.wls:
            return False
        if any([not isclose(l, r) for (l, r) in zip(self.params, rhs.params)]):
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


    def findpeak(self):
        self.peak = max(self.trans, key = lambda x: x[1])
        peakloc = self.trans.index(peak)
        leftpt = next((pt for pt in self.trans[:peakloc - 1:-1] if pt[1] < self.peak[1]/2), None)
        rightpt = next((pt for pt in self.trans[peakloc + 1:] if pt[1] < self.peak[1]/2), None)
        leftloc, rightloc = map(self.trans.index(leftpt), self.trans.index(rightpt)

    def mutate(self):
        childparams = [round(random.gauss(1, 0.1)*p, 4) for p in self.params]
        child = self.__class__(childparams, self.wls, self.target)
        return child

    def crossbreed(self, rhs):
        childparams = [p[random.randint(0, 1)] for p in zip(self.params, rhs.params)]
        child = self.__class__(childparams, self.wls, self.target)
        return child
