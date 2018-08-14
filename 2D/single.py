import matplotlib.pyplot as plt

from gratings.zcg2d import ZCG2D
from lib.generation import Generation

from shapely.geometry import Polygon, MultiPolygon

def main():
    #dimensions
    d = 4.5
    tblocks = 2.23
    tslab = 1.17
    
    seedpoly = Polygon([(0, 0), (0, 0.7515), (0.7515, 0.7515), (0.792, 0.36), (0.9675, 0.126), (0.7515, 0.108), (0.7515, 0.0405), (0.648, 0)])

    g = ZCG2D((d, tblocks, tslab), seedpoly, (8,12,1001))
    g.evaluate()
    print(g)
    plt.plot(*zip(*g.trans))
    plt.show()

if __name__ == "__main__":
    main()
