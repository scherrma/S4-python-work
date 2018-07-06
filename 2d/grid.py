from termcolor import colored
from random import choice
from copy import deepcopy

class Fourgrid:
    def __init__(self, size):
        self.size = size
        self.hsize = (size-1)//2
        self.odd = (size % 2 == 1)
        self.data = [choice([True, False]) for i in range(size*size//4 + size%2)]

    def __loc(self, coords):
        x = coords[0] % self.size
        y = coords[1] % self.size

        if self.odd and x == self.hsize and y == self.hsize:
            return len(self.data)-1
        
        elif x > self.hsize or (x == self.hsize and y > self.hsize):
            x = self.size - x - 1
            y = self.size - y - 1
        if y >= self.hsize:
            y, x = x, self.size - y - 1
        return x + y*(self.hsize + int(self.odd))

    def __getitem__(self, coords):
        return self.data[self.__loc(coords)]

    def __setitem__(self, coords, value):
        self.data[self.__loc(coords)] = value

    def __str__(self):
        lines = []
        for y in range(self.size):
            lines.append(''.join([colored(2*u"\u2588", "cyan" if self[x, y] else "yellow") for x in range(self.size)]))
        #for y in range(self.size):
        #    lines.append(' '.join([str(self.__loc((x,y))) for x in range(self.size)]))
        return '\n'.join(lines)
        self.data = newdata
        
    def cool(self):
        newdata = deepcopy(self.data)
        for x in range(self.hsize):
            for y in range(self.hsize):
                nbors = sum([int(self[x+i, y+j]) for i in (-1, 0, 1) for j in (-1, 0, 1)])
                newdata[self.__loc((x, y))] = (nbors > 4)
        self.data = newdata

    def altcool(self):
        coolrange = 3
        newdata = deepcopy(self.data)
        for x in range(self.hsize):
            for y in range(self.hsize):
                nbors = sum([(coolrange**2 > i**2 + j**2 if int(self[x+i, y+j]) else 0) for i in range(-coolrange, coolrange+1) for j in range(-coolrange, coolrange+1)])
                newdata[self.__loc((x, y))] = (nbors > 4)
        self.data = newdata
