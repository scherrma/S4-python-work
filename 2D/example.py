import S4

d = 4.95
tblocks = 2
tslab = 1
wls = (8, 12, 2001)

S = S4.New(Lattice = ((d, 0), (0, d)), NumBasis = 20)

S.AddMaterial('vacuum', 1)
S.AddMaterial('silicon', 12+0.01j)

S.AddLayer('top', 0, 'vacuum')
S.AddLayer('slab', tslab, 'silicon')
S.AddLayerCopy('bottom', 0, 'top')
S.SetRegionCircle('slab', 'vacuum', (0, 0), 0.2)

S.SetExcitationPlanewave((0, 0), 1, 0)
S.SetFrequency(0.4)
tx = S.GetPowerFlux('bottom')
print(tx)
