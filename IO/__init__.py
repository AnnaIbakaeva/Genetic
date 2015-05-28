#-*- coding: utf-8 -*-
import tree_creation
from crossover import Crossover
from tree import Tree
from polish_notation import get_polish_notation, calculate_polish_notation, notation_to_str
from functions import TwoVariableFunction, Function
from reproduction import Reproductor
from random import choice, randint
from sets import variable_values_set, target_values
from copy import deepcopy


def generate_init_population(number):
    init_trees = []
    i = 0
    while i < number:
        depth = (i+100)/100
        tree_creator = tree_creation.TreeCreator(depth)
        if i % 2 == 0:
            tree_creator.create(False)
        else:
            tree_creator.create(True)
        t = tree_creator.tree
        init_trees.append(Tree(t.init_tree, t.tree_map))
        print(Tree.string_tree_map(t.tree_map))
        print(t.init_tree)
        print("")
        i += 1
    return list(init_trees)


def select_best_individuals(trees):
    reproductor = Reproductor(trees)
    return list(reproductor.select())


def cross_trees(population, number):
    i = 0
    result_trees = []
    while i < number-len(population):
        parent1 = choice(population)
        parent2 = choice(population)
        j = randint(1, 10)
        if j <= 9:
            cr = Crossover(parent1, parent2)
            if cr.cross():
                result_trees.append(cr.new_tree1)
                result_trees.append(cr.new_tree2)
                i += 1
    return result_trees


def mutate_trees(population):
    for individual in population:
        value = randint(1, 100)
        if value == 1:
            individual.mutate_from_term_to_term()
        else:
            value = randint(1, 100)
            if value == 1:
                individual.mutate_from_func_to_func()
            else:
                value = randint(1, 1000)
                if value == 1:
                    individual.mutate_from_func_to_term()
                else:
                    value = randint(1, 1000)
                    if value == 1:
                        individual.mutate_from_term_to_func()
    return population


def check_on_result(trees):
    reproductor = Reproductor(trees)
    result = False
    fitnesses= []
    for tree in trees:
        if len(tree.tree_map) == 0:
            continue
        i = 0
        fitness_result = 0
        while i < len(target_values):
            fitness_result += reproductor.get_fitness(tree, target_values[i], variable_values_set[i])
            i += 1
        # print(Tree.string_tree_map(tree.tree_map))
        # print(tree.init_tree)
        print("fitness_result ", fitness_result)
        fitnesses.append(fitness_result)
        if fitness_result < 0.00001:
            print("RESULT")
            print(Tree.string_tree_map(tree.tree_map))
            print(tree.init_tree)
            result = True
    print("MIN FINTESS RESULT: ", min(fitnesses))
    return result


population_number = 600
init_population = generate_init_population(population_number)
result = False
counter = 0
while not result and counter < 500:
    print("************************************************************************************************************"
          "************************************************************************************************************")
    print(counter)
    best_individuals = deepcopy(select_best_individuals(init_population))

    if len(best_individuals) == 0:
        print("Reproduction empty")
        result = True
        continue

    children = deepcopy(cross_trees(best_individuals, population_number))
    all_trees = best_individuals + children

    all_trees = deepcopy(mutate_trees(all_trees))

    result = check_on_result(all_trees)

    init_population = deepcopy(all_trees)
    if len(init_population) == 0:
        print("Empty population")
        result = True
    counter += 1

print("End")