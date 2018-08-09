#import matplotlib.pyplot as plt

from gratings.zcg2d import ZCG2D
from lib.generation import Generation

from shapely.geometry import Polygon, MultiPolygon
import S4
import numpy as np

def main():
    #dimensions
    d = 4.95
    tblocks = 3.11
    tslab = 1.82
    wls = (8, 12, 2001)
    
    poly = Polygon([(1, 0), (0, 1), (-1, 0), (0, -1)])

    S = S4.New(Lattice = ((d, 0), (0, d)), NumBasis = 20)
    
    #materials
    S.AddMaterial("Vacuum", 11)
    S.AddMaterial("Silicon", 1) #edited later by wavelength
          
    #layers
    S.AddLayer('top', 0, "Vacuum")
    S.AddLayer('blocks', tblocks, "Vacuum")
    S.AddLayer('slab', tslab, "Silicon")
    S.AddLayer('bottom', 0, "Vacuum")
    
    #patterning
    #print("exterior coords:",list(poly.exterior.coords),("is" if poly.exterior.is_simple else "isn't"),"simple",\
    #        ("and is" if poly.exterior.is_ccw else "but isn't"),"ccw")
    #S.SetRegionPolygon('blocks', 'Silicon', (0, 0), 0, tuple(poly.exterior.coords))
    #for inner in poly.interiors:
    #    print("interior coords:",list(inner.coords))
    #    S.SetRegionPolygon('blocks', 'Vacuum', (0, 0), 0, tuple(inner.coords))

    S.SetRegionPolygon('blocks', 'Vacuum', (0, 0), 0, ((d/4, d/4), (-d/4, d/4), (-d/4, -d/4), (d/4, -d/4)))

    #light
    S.SetExcitationPlanewave((0,0),0,1)
    
    for wl in np.linspace(*wls):
        S.SetFrequency(1/wl)
        #S.SetMaterial('Silicon',complex(ZCG2D.si_n(wl), ZCG2D.si_k(wl))**2)
        print("wl:",wl,"\ttrans:",float(np.real(S.GetPowerFlux('bottom')[0])))

if __name__ == "__main__":
    main()
