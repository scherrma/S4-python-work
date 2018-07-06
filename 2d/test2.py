from grid2 import Fourgrid
from termcolor import colored

a = Fourgrid(7)
print("a.size:",a.size,"\ta.hsize:",a.hsize)
print("a[0,0]:",a[0,0])
print("setting a[0,0] to true")
a[0,0] = True
print("a[0,0]:",a[0,0])
