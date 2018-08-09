import copy
import numpy
import random 

class Generation:
    def __init__(self, size, seed = None, mutation_rate = 0.1, elite = 0):
        if(seed):
            self.pop = [seed] + [seed.mutate() for i in range(size-1)]
        else:
            self.pop = size*[seed]

        self.best = None
        self.elite = elite
        self.muta_rate = mutation_rate

    def __str__(self):
        return '\n'.join([str(g) for g in self.pop])

    def _evaluate(self):
        self.pop.sort(key = lambda x: x.evaluate(), reverse=True)
        self.best = self.pop[0]

    def progeny(self):
        self._evaluate()
        childpop = self.pop[:self.elite]
        fitnesses = [g.evaluate()/sum([x.evaluate() for x in self.pop]) for g in self.pop]

        for i in range(len(self.pop) - self.elite):
            parents = numpy.random.choice(range(len(self.pop)), 2, False, fitnesses)
            child = self.pop[parents[0]].crossbreed(self.pop[parents[1]])
            childpop.append(child.mutate() if random.random() < self.muta_rate else child)

        child = copy.deepcopy(self)
        child.pop = childpop
        return child
