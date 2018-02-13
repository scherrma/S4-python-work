import lib.helpers as h
import scipy.interpolate as interp

SPEED_OF_LIGHT = 299792458*10**6 #in um/s

si_n = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_n.csv',1)]))
si_k = interp.interp1d(*zip(*[[(SPEED_OF_LIGHT/float(f)),n] for f,n in h.opencsv('matdat/silicon_k.csv',1)]))
