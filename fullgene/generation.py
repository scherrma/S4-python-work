import itertools
from random import random, uniform

class Generation:
    def __init__(self, size, seed = None, mutation_rate = 0.1, elite = 0):
        if(seed):
            self.pop = [seed] + [seed.mutate() for i in range(size-1)]
        else:
            self.pop = size*[seed]

        self.elite = elite
        self.muta_rate = mutation_rate

    def _evaluate(self):
        self.pop = sorted(self.pop, key = lambda x: x.evaluate(), reverse=True)
        self.fitness = itertools.accumulate([g.evaluate() for g in self.pop])

    def best(self, n = 1):
        self._evaluate()
        return self.pop[:n]

    def progeny(self):
        self._evaluate()
        prog = self.pop[:elite]

