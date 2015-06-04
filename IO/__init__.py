#-*- coding: utf-8 -*-
import tree_creation
from crossover import Crossover
from tree import Tree
from polish_notation import get_polish_notation, calculate_polish_notation, notation_to_str
from functions import TwoVariableFunction, Function
from reproduction import Reproductor
from random import choice, randint
from constants import POPULATION_NUMBER, VARIABLE_VALUES_SET, TARGET_VALUES, MUTATION_PROBABILITY, \
    NODAL_MUTATION_PROBABILITY, TARGET_RESULT, CROSS_PROBABILITY, REPRODUCTION_PROBABILITY, SECONDARY_INPUTS, \
    SECONDARY_OUTPUTS
from copy import deepcopy
from math import isinf

results = []


def generate_init_population():
    init_trees = []
    i = 0
    while i < POPULATION_NUMBER:
        depth = (i+100)/100 + 1
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
    print("")
    print "REPRODUCTION"
    reproductor = Reproductor(trees)
    return list(reproductor.select())


def cross_trees(population):
    result_trees = []
    parent1 = choice(population)
    parent2 = choice(population)
    j = randint(1, CROSS_PROBABILITY)
    if j <= 9:
        cr = Crossover(parent1, parent2)
        if cr.cross():
            result_trees.append(cr.new_tree1)
            result_trees.append(cr.new_tree2)
    return result_trees


def mutate_trees(population):
    for individual in population:
        value = randint(1, NODAL_MUTATION_PROBABILITY)
        if value == 1:
            individual.mutate_from_term_to_term()
        else:
            value = randint(1, NODAL_MUTATION_PROBABILITY)
            if value == 1:
                individual.mutate_from_func_to_func()
            else:
                value = randint(1, MUTATION_PROBABILITY)
                if value == 1:
                    individual.mutate_from_func_to_term()
                else:
                    value = randint(1, MUTATION_PROBABILITY)
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
        while i < len(TARGET_VALUES):
            fitness_result += reproductor.get_fitness(tree, TARGET_VALUES[i], VARIABLE_VALUES_SET[i])
            i += 1
        print("fitness_result ", fitness_result)
        if isinf(fitness_result):
            continue
        fitnesses.append(fitness_result)
        if fitness_result < TARGET_RESULT:
            print("RESULT")
            print(Tree.string_tree_map(tree.tree_map))
            print(tree.init_tree)
            tree.fitness = fitness_result
            results.append(tree)
    print("MIN FINTESS RESULT: ", min(fitnesses))
    print "AVERAGE FITNESS: ", sum(fitnesses)/len(fitnesses)
    print "length ", len(fitnesses)
    print "results "
    for r in results:
        print "fitness ", r.fitness
        print Tree.string_tree_map(r.tree_map)
    return result


def select(population):
    i = 0
    new_population = []
    while i < POPULATION_NUMBER:
        offspring = cross_trees(population)
        if len(offspring) > 0:
            new_population += offspring
            i += 2
        j = randint(1, REPRODUCTION_PROBABILITY)
        if j <= 2:
            new_population.append(choice(population))
            i += 1
    return new_population


def select_best_result(trees):
    fitnesses = []
    for individual in trees:
        i = 0
        fitness = 0
        while i < len(SECONDARY_INPUTS):
            fitness += Reproductor.get_fitness(individual, SECONDARY_OUTPUTS[i], SECONDARY_INPUTS[i])
            i += 1
        fitnesses.append(fitness)
    best_fitness = min(fitnesses)
    position = fitnesses.index(best_fitness)
    return trees[position]


init_population = generate_init_population()
result = False
counter = 0
while not result and counter < 500:
    print("************************************************************************************************************"
          "************************************************************************************************************")
    print(counter)
    best_individuals = deepcopy(select_best_individuals(init_population))

    if len(best_individuals) == 0:
        print("Reproduction empty")
        break

    new_generation = deepcopy(select(best_individuals))

    mutated_trees = deepcopy(mutate_trees(new_generation))

    result = check_on_result(mutated_trees)

    init_population = deepcopy(mutated_trees)
    if len(init_population) == 0:
        print("Empty population")
        result = True
    counter += 1

print("End")
# if results > 0:
#     best_tree = select_best_result(results)
#     print "Best result"
#     print Tree.string_tree_map(best_tree.tree_map)
#     print best_tree.init_tree
#     print best_tree.fitness
print("")
print "MIN RESULT"
print Tree.string_tree_map(min(results))
print min(results).init_tree
print min(results).fitness