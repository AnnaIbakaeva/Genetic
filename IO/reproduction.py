#-*- coding: utf-8 -*-
import polish_notation
from math import isinf, ceil
from constants import VARIABLE_VALUES_SET, TARGET_VALUES
from functions import Function
import copy
from tree import Tree


class Reproductor(object):

    def __init__(self, population):
        self._init_population = list(population)
        self._selected_population = []
        self._del_individuals = set()
        self.adjusted_fitness_values = []
        self._get_sum_fitness_function()

    def _get_sum_fitness_function(self):
        i = 0
        while i < len(TARGET_VALUES):
            sum_adjusted_fitness = 0
            for individual in self._init_population:
                if len(individual.tree_map) > 0:
                    fitness = self.get_fitness(individual, TARGET_VALUES[i], VARIABLE_VALUES_SET[i])
                    if not isinf(fitness):
                        sum_adjusted_fitness += Reproductor.get_adjusted_fitness(fitness)
            if isinf(sum_adjusted_fitness):
                print("sum_adjusted_fitness ", sum_adjusted_fitness)
                print("length ", len(self._init_population))
                exit()
            self.adjusted_fitness_values.append(sum_adjusted_fitness)
            i += 1

    def get_fitness(self, individual, target, variable_values):
        # print "tree ", Tree.string_tree_map(individual.tree_map)
        # print individual.init_tree
        notation = polish_notation.get_polish_notation(individual)
        # print "notation ", polish_notation.notation_to_str(notation)
        value = polish_notation.calculate_polish_notation(notation, variable_values)
        # print "value ", value
        if isinf(value):
            self._del_individuals.add(individual)
            return value
        result = (target - value)*(target - value)
        if isinf(result):
            self._del_individuals.add(individual)
        return result

    def select(self):
        for individual in self._init_population:
            if not individual in self._del_individuals and len(individual.tree_map) > 0:
                i = 0
                counts = 0
                while i < len(TARGET_VALUES):
                    fitness = self.get_fitness(individual, TARGET_VALUES[i], VARIABLE_VALUES_SET[i])
                    adjusted_fitness = Reproductor.get_adjusted_fitness(fitness)
                    counts += int((adjusted_fitness/self.adjusted_fitness_values[i]) * len(self._init_population))
                    i += 1
                j = 0
                average_count = ceil(counts / len(TARGET_VALUES))
                while j < average_count and Reproductor.function_check(individual.tree_map):
                    self._selected_population.append(copy.deepcopy(individual))
                    j += 1

        return self._selected_population

    @staticmethod
    def function_check(tree_map):
        """Проверка, что в дереве есть функции"""
        for key in tree_map.keys():
            if isinstance(tree_map[key], Function):
                return True
        return False

    @staticmethod
    def get_adjusted_fitness(standardized_fitness):
        return 1/(1+standardized_fitness)

    @staticmethod
    def get_fitness(individual, target, variable_values):
        notation = polish_notation.get_polish_notation(individual)
        value = polish_notation.calculate_polish_notation(notation, variable_values)
        if isinf(value):
            return value
        result = (target - value)*(target - value)
        return result
