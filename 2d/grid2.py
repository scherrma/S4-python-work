from termcolor import colored
from random import choice
from copy import deepcopy

class Fourgrid:
    def __init__(self, size):
        self.size = size
        self.hsize = (1+size)//2
        self.odd = (size % 2 == 1)
        self.data = [choice([True, False]) for i in range(size*size)]

    def __getitem__(self, coords):
        print("coords:",coords)
        return self.data[coords[0] + coords[1]*self.size]

    def __setitem__(self, coords, value):
        self.data[coords[0] + coords[1]*self.size] = value
#    def at(self, x, y):
#        x %= self.size
#        y %= self.size
#        if(y >= self.hsize):
#            y = self.size - y - 1
#            x = self.size - x - 1
#        if(x >= self.hsize):
#            x = self.size - x - 1
#            x, y = y, x
#        return self.data[y][x]
#
#    def __str__(self):
#        lines = []
#        for i in range(-self.hsize, self.size+self.hsize):
#            lines.append(''.join([colored(2*u"\u2588", "cyan" if self.at(j, i) else "yellow") for j in range(-self.hsize,self.size+self.hsize)]))
#        return '\n'.join(lines)
#
#    def cool(self):
#        newdata = deepcopy(self.data)
#        for x in range(self.hsize):
#            for y in range(self.hsize):
#                nbors = sum([int(self.at(x+i, y+j)) for i in (-1, 0, 1) for j in (-1, 0, 1)])
#                newdata[y][x] = (nbors > 4)
#        self.data = newdata
