from termcolor import colored
from random import choice
from copy import deepcopy

class Fourgrid:
    def __init__(self, size):
        self.size = size
        self.hsize = (size-1)//2
        self.odd = size % 2
        self.data = [choice([True, False]) for i in range(size*size//4 + self.odd)]
        
        self._loc = [size*[0] for i in range(size)]
        for x in range(self.hsize + 1):
            for y in range(self.hsize + 1 - self.odd):
                val = x + y*(self.hsize+1)
                self._loc[x][y] = val
                self._loc[size-x-1][size-y-1] = val
                self._loc[y][size-x-1] = val
                self._loc[size-y-1][x] = val
        if self.odd:
            self._loc[self.hsize][self.hsize] = self.hsize*(self.hsize+1)
    
    def __getitem__(self, coords):
        x, y = [i % self.size for i in coords]
        return self.data[self._loc[x][y]]

    def __setitem__(self, coords, value):
        x, y = [i % self.size for i in coords]
        self.data[self._loc[x][y]] = value

    def __str__(self):
        return '\n'.join([''.join([colored(2*u"\u2588", "cyan" if self[x, y] else "yellow")\
                for x in range(self.size)]) for y in range(self.size)]) 

    def bigstr(self):
        return '\n'.join([''.join([colored(2*u"\u2588", "cyan" if self[x, y] else "yellow")\
                for x in range(2*self.size)]) for y in range(2*self.size)]) 

    def cool(self):
        newdata = deepcopy(self.data)
        for x in range(self.hsize):
            for y in range(self.hsize):
                nbors = sum([int(self[x+i, y+j]) for i in (-1, 0, 1) for j in (-1, 0, 1)])
                newdata[self._loc[x][y]] = (nbors > 4)
        self.data = newdata

    def altcool(self):
        coolrange = 3
        newdata = deepcopy(self.data)
        for x in range(self.hsize):
            for y in range(self.hsize):
                nbors = sum([(coolrange**2 > i**2 + j**2 if int(self[x+i, y+j]) else 0) for i in range(-coolrange, coolrange+1) for j in range(-coolrange, coolrange+1)])
                newdata[self.__loc((x, y))] = (nbors > 4)
        self.data = newdata
