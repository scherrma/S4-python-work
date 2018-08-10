import copy
from math import exp, isclose
import random
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale
from shapely.ops import unary_union

class Grating2D:
    edge_supp = 15 #peak near edge suppresion

    def __init__(self, params, poly, wavelengths):
        self.params = list(params) #order needs to match labels
        self.d, self.tblocks, self.tslab = params
        self.labels = ('d', 'tblocks', 'tslab')
        self.poly, self.wls = poly, wavelengths
        self._findpolys()
        self.fom, self.trans = None, None
    
    def _findpolys(self):
        allpolys = [self.poly, Polygon([(-y, x) for (x, y) in self.poly.exterior.coords])]
        allpolys += [Polygon([(-x, -y) for (x, y) in k.exterior.coords]) for k in allpolys]
        allpolys = scale(unary_union(allpolys), self.d/2, self.d/2)
        try:
            iter(allpolys)
        except TypeError:
            allpolys = MultiPolygon([allpolys])
        self.allpolys = [shape.simplify(tolerance = self.d/100) for shape in allpolys]

    def __str__(self):
        strrep = ', '.join([l+' = '+str(round(v, 4)) for l, v in zip(self.labels, self.params)])  
        if self.fom:
            strrep += ', fom: '+str(round(self.fom, 4))
        for shape in self.allpolys:
            strrep += "\n\texterior polygon: "+str(list(shape.exterior.coords))
            if shape.interiors:
                strrep += "\n\tinterior polygon"+("s" if len(shape.interiors) > 1 else "")+": "\
                        + '\n\t'.join([str(list(inner.coords)) for inner in shape.interiors])
        return strrep

    def __eq__(self, rhs):
        return self.__class__ != rhs.__class__ and self.wls != rhs.wls\
                and self.params == rhs.params and self.poly.almost_equals(rhs.poly)
    
    def _calcfom(self):
        invrms = lambda x: (sum([a**2 for a in x])/len(x))**(-1/2)

        peak = max(self.trans, key=lambda x:x[1])
        self.peak = peak[0]
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
            if self.fom > 20:
                peakedge = 1 - exp(-Grating.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                             - exp(-Grating.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                self.fom *= peakedge*(peak[1]**2)/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

        #debug
        if self.fom < 0:
            print("negative fom: "+str(self))
            self.fom = 0
    
   ## def mutate(self):
   ##     child = copy.deepcopy(self)
   ##     if random.random() < 1/2:
   ##         childpoly = self.poly
   ##         childparams = [round(random.gauss(1, 0.1)*p, 4) for p in self.params]
   ##     else:
   ##         childparams = self.params


   ##     child.__init__(childparams, self.wls)
   ##     return child
    
    def crossbreed(self, rhs):
        child = copy.deepcopy(self)
        childparams = [(self.params[i] if random.randint(0,1) else rhs.params[i]) for i in range(len(self.params))]
        childpoly = (self.poly.union(rhs.poly) if random.random() < 1/2 else self.poly.intersection(rhs.poly))
        child.__init__(childparams, childpoly, self.wls)
        return child
