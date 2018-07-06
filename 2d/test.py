from grid import Fourgrid
from termcolor import colored

a = Fourgrid(7)
print("a.size:",a.size,"\ta.hsize:",a.hsize)
print(a)
for i in range(2):
    print("cooling a")
    a.cool()
    print(a)
