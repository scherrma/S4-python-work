#import matplotlib.pyplot as plt

from gratings.zcg2d import ZCG2D
from lib.generation import Generation

from shapely.geometry import Polygon, MultiPolygon

def main():
    #dimensions
    d = 4.95
    tblocks = 3.11
    tslab = 1.82

    g = ZCG2D((d, tblocks, tslab), Polygon([(1/2, 0), (1, 0), (1, 1), (0, 1), (0, 1/2), (1/2, 1/2)]), (8,12,1001))
    g.evaluate()
    print(g)

if __name__ == "__main__":
    main()
