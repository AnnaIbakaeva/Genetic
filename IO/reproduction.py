import polish_notation
from sets import variable_values
from math import isinf, fabs


class Reproductor(object):

    def __init__(self, population, target):
        self.sum_fitness = 0
        self._init_population = population
        self._selected_population = []
        self._target = target
        self._average = 0
        self._get_sum_fitness_function()

    def _get_sum_fitness_function(self):
        for individual in self._init_population:
            self.sum_fitness += self._get_fitness(individual)
        self._average = self.sum_fitness / len(self._init_population)
        if isinf(self._average):
            self._average = max(self._init_population)

    def _get_fitness(self, individual):
        notation = polish_notation.get_polish_notation(individual)
        value = polish_notation.calculate_polish_notation(notation, variable_values)
        result = (self._target - value)*(self._target - value)
        if isinf(result):
            result = fabs(self._target - value)
        return result

    def select(self):
        for individual in self._init_population:
            value = self._get_fitness(individual)
            if value < self._average:
                self._selected_population.append(individual)
                if value / self._average < 0.5:
                    self._selected_population.append(individual)
        return self._selected_population
