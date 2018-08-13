import S4
from gratings.grating2d import Grating2D
import lib.helpers as h

import numpy as np
import scipy.interpolate as interp
import scipy.constants as consts
from shapely.geometry import Polygon


class ZCG2D(Grating2D):
    si_n = interp.interp1d(*zip(*[[((consts.speed_of_light*10**6)/float(f)),n] for f,n in h.opencsv('matdat/silicon_n.csv',1)]))
    si_k = interp.interp1d(*zip(*[[((consts.speed_of_light*10**6)/float(f)),n] for f,n in h.opencsv('matdat/silicon_k.csv',1)]))

    def evaluate(self, fbasis = 30):
        if self.fom is None:
            S = S4.New(Lattice = ((self.d, 0), (0, self.d)), NumBasis = fbasis)
          
            #materials
            S.AddMaterial("Vacuum",1)
            S.AddMaterial("Silicon",1) #edited later by wavelength
          
            #layers
            S.AddLayer('top',0,"Vacuum")
            S.AddLayer('blocks',self.tblocks,"Vacuum")
            S.AddLayer('slab',self.tslab,"Silicon")
            S.AddLayer('bottom', 0, "Vacuum")
          
            #patterning
            for shape in self.allpolys:
                coords = shape.exterior.coords[:-1] if shape.exterior.is_ccw else shape.exterior.coords[:0:-1]
                S.SetRegionPolygon('blocks', 'Silicon', (0, 0), 0, tuple(coords))
                for inner in shape.interiors:
                    coords = inner.coords[:-1] if inner.is_ccw else inner.coords[:0:-1]
                    S.SetRegionPolygon('blocks', 'Vacuum', (0, 0), 0, tuple(coords))
          
            #light
            S.SetExcitationPlanewave((0,0),0,1)
          
            self.trans = []
            for wl in np.linspace(*self.wls):
                S.SetFrequency(1/wl)
                S.SetMaterial('Silicon',complex(ZCG2D.si_n(wl), ZCG2D.si_k(wl))**2)
                self.trans.append((wl, float(np.real(S.GetPowerFlux('bottom')[0]))))
            self._calcfom()
        
        return self.fom                                                                 
