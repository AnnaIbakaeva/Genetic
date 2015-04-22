

class Reproductor(object):
    sum_fitness = 0

    def __init__(self, population):
        self._init_population = population
        self._selected_population = []
        self.get_sum_fitness_function()

    def get_sum_fitness_function(self):
        for individual in self._init_population:
            self.sum_fitness += self._get_fitness(individual)

    def _get_fitness(self, individual):
        return 0

    def select(self):
        for individual in self._init_population:
            count = round(self._get_fitness(individual) / self.sum_fitness)
            while count > 0:
                self._selected_population.append(individual)
                count -= 1
