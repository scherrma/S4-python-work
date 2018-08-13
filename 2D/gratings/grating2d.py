import copy
from math import exp, isclose
import random
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import scale
from shapely.ops import unary_union
from lib.vector import Vector

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
        try:
            allpolys = [self.poly, Polygon([(-y, x) for (x, y) in self.poly.exterior.coords])]
            allpolys += [Polygon([(-x, -y) for (x, y) in k.exterior.coords]) for k in allpolys]
            allpolys = scale(unary_union(allpolys), self.d/2, self.d/2)
        except:
            self.poly.buffer(0, cap_style=2, join_style=2)
            print("buffered")
        try:
            allpolys = [self.poly, Polygon([(-y, x) for (x, y) in self.poly.exterior.coords])]
            allpolys += [Polygon([(-x, -y) for (x, y) in k.exterior.coords]) for k in allpolys]
            allpolys = scale(unary_union(allpolys), self.d/2, self.d/2)
        except:
            print("self.poly")
            raise SystemExit
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
            strrep += "\n\texterior polygon: "+str(list(map(lambda x: (round(x[0], 3), round(x[1], 3)), shape.exterior.coords)))
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
                peakedge = 1 - exp(-Grating2D.edge_supp*(peak[0]-self.wls[0])/(self.wls[1]-self.wls[0])) \
                             - exp(-Grating2D.edge_supp*(self.wls[1]-peak[0])/(self.wls[1]-self.wls[0]))
                self.fom *= peakedge*(peak[1]**2)/(rightwl-leftwl)
        else:
            self.fom = invrms([t for wl, t in self.trans])

        #debug
        if self.fom < 0:
            print("negative fom: "+str(self))
            self.fom = 0
    
    def mutate(self):
        childparams, childpoly = self.params, self.poly
        if random.random() < 1/2:
            childparams = [round(random.gauss(1, 0.1)*p, 4) for p in self.params]

        else:
            if len(self.poly.exterior.coords) < 5 or (len(self.poly.exterior.coords) < 15 and random.random() < 1/2): #add a point
                #find the edge of the polygon nearest the new point and add the point there
                mindist = float('inf')
                pt_new = Vector([round(random.uniform(-1/3, 1),3) for i in range(2)])
                for i in range(-1, len(self.poly.exterior.coords)-2):
                    pt_left, pt_center, pt_right = [Vector(self.poly.exterior.coords[1:][i+k]) for k in (-1, 0, 1)]
                    v_left, v_right, v_new = [pt - pt_center for pt in (pt_left, pt_right, pt_new)]
                    if (v_left.unit() + v_right.unit()).norm() > 10**(-4): #if the vectors are pointed nearly precisely opposite each other, ignore them
                       if v_new.dot(v_right) > 0 and (pt_new - pt_right).dot(pt_center - pt_right) > 0:
                           dist = v_new.reject(v_right).norm()
                           edge = i + 1
                       else:
                           dist = v_new.norm()
                           try:
                               edge = i + bool(v_new.reject(v_left.unit() + v_right.unit()).dot(v_right) > 0)
                           except ZeroDivisionError:
                               print("\n\n",colored("zero division error",'red'), "while adding", pt_new, "to", list(self.poly.exterior.coords), "\nconsidering pt_left, pt_center, pt_right:", pt_left, pt_center, pt_right)
                               raise SystemExit
                       if dist < mindist:
                           mindist = dist
                           nearedge = edge
                childpoly = Polygon(self.poly.exterior.coords[:nearedge+1] + [pt_new.val] + self.poly.exterior.coords[nearedge+1:-1])

            else: #remove a point
                pt = random.randint(0, len(self.poly.exterior.coords)-2)
                childpoly = Polygon(self.poly.exterior.coords[:pt]+self.poly.exterior.coords[pt+1:-1])
                while not (childpoly.is_valid and childpoly.is_simple):
                    pt = random.randint(0, len(self.poly.exterior.coords)-2)
                    childpoly = Polygon(self.poly.exterior.coords[:pt]+self.poly.exterior.coords[pt+1:-1])

        child = self.__class__(childparams, childpoly, self.wls)
        try:
            allpolys = [child.poly, Polygon([(-y, x) for (x, y) in child.poly.exterior.coords])]
            allpolys += [Polygon([(-x, -y) for (x, y) in k.exterior.coords]) for k in allpolys]
            allpolys = scale(unary_union(allpolys), self.d/2, self.d/2)
        except:
            print("this should systemexit; starting shape:",list(self.poly.exterior.coords),"\tnew shape:",child.poly)
            raise SystemExit
        return child
    
    def crossbreed(self, rhs):
        childparams = [p[random.randint(0, 1)] for p in zip(self.params, rhs.params)]

        childpoly = self.poly.intersection(rhs.poly)
        if not childpoly.is_valid or random.random() < 1/2:
            childpoly = self.poly.union(rhs.poly)

        child = self.__class__(childparams, childpoly, self.wls)
        return child
