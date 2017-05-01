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
    SECONDARY_OUTPUTS, ALLOWABLE_ERROR, VARIABLE_SET, MAX_DEPTH
from copy import deepcopy
from math import isinf
# from lxml import etree

results = []


def generate_init_population():
    init_trees = []
    i = 0
    while i < POPULATION_NUMBER:
        depth = (i+100)/100 + 1
        tree_creator = tree_creation.TreeCreator(depth, i)
        if i % 2 == 0:
            tree_creator.create(False)
        else:
            tree_creator.create(True)
        t = tree_creator.tree
        init_trees.append(Tree(t.init_tree, t.tree_map, t.id))
        print(t.id)
        print(Tree.tree_map_to_string(t.tree_map))
        print(t.init_tree)
        print("")
        i += 1
    return list(init_trees)


def reproduce(trees):
    rep = Reproductor(trees)
    return list(rep.select())


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


def check_fitness(trees):
    errors = []
    for one_tree in trees:
        if len(one_tree.tree_map) == 0:
            continue
        sum_error = 0
        good_individual = True
        for i in range(0, len(TARGET_VALUES)):
            error = Reproductor.get_error(one_tree, TARGET_VALUES[i], VARIABLE_VALUES_SET[i])
            if error > ALLOWABLE_ERROR:
                good_individual = False
            sum_error += error
        if isinf(sum_error):
            continue
        errors.append(sum_error)
        if good_individual or sum_error < TARGET_RESULT:
            print("RESULT")
            print(Tree.tree_map_to_string(one_tree.tree_map))
            print(one_tree.init_tree)
            one_tree.fitness = sum_error
            results.append(one_tree)
    print("MIN FITNESS RESULT: ", min(errors))
    print ("AVERAGE FITNESS: ", sum(errors)/len(errors))
    print ("length ", len(errors))
    print ("results ")
    for r in results:
        print ("fitness ", r.fitness)
        print (Tree.tree_map_to_string(r.tree_map))


def create_new_generation(population):
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


def select_best_result_with_secondary_data(trees):
    errors = []
    for individual in trees:
        fitness = 0
        for i in range(0, len(SECONDARY_INPUTS)):
            fitness += Reproductor.get_error(individual, SECONDARY_OUTPUTS[i], SECONDARY_INPUTS[i])
        errors.append(fitness)
    best_fitness = min(errors)
    position = errors.index(best_fitness)
    return trees[position]


# ev = etree.Element("Evolution", xmlns="http://ns.adobe.com/air/application/1.5")
#
# etree.SubElement(ev, "PopulationNumber").text = str(POPULATION_NUMBER)
# etree.SubElement(ev, "MaxDepth").text = str(MAX_DEPTH)
# etree.SubElement(ev, "AllowableError").text = str(ALLOWABLE_ERROR)
#
# variables = etree.SubElement(ev, "Variables")
# for variable in VARIABLE_SET:
#     etree.SubElement(variables, "item").text = variable
#
# input_values = etree.SubElement(ev, "InputValues")
# for item in VARIABLE_VALUES_SET:
#     itemElm = etree.SubElement(input_values, "Item")
#     for key in item.keys():
#         etree.SubElement(itemElm, "Variable", name=key, value=str(item[key]))
#
# output_values = etree.SubElement(ev, "OutputValues")
# for value in TARGET_VALUES:
#     etree.SubElement(output_values, "Value").text = str(value)
#
# probabilities = etree.SubElement(ev, "Probabilities")
# etree.SubElement(probabilities, "Crossover").text = str(CROSS_PROBABILITY)
# etree.SubElement(probabilities, "Reproduction").text = str(REPRODUCTION_PROBABILITY)
# mutation_probabilities = etree.SubElement(probabilities, "Mutation")
# etree.SubElement(mutation_probabilities, "Node").text = str(NODAL_MUTATION_PROBABILITY)
# etree.SubElement(mutation_probabilities, "Truncated").text = str(MUTATION_PROBABILITY)
# etree.SubElement(mutation_probabilities, "Increasing").text = str(MUTATION_PROBABILITY)
#
# functions = etree.SubElement(ev, "Functions")
# etree.SubElement(functions, "Function").text = "sin"
# etree.SubElement(functions, "Function").text = "cos"
# etree.SubElement(functions, "Function").text = "exp"
# etree.SubElement(functions, "Function").text = "log"
# etree.SubElement(functions, "Function").text = "+"
# etree.SubElement(functions, "Function").text = "-"
#
# handle = etree.tostring(ev, pretty_print=True, encoding='utf-8', xml_declaration=True)
# xml_file = open("evolution.xml", "w")
# xml_file.writelines(handle)
# xml_file.close()

# d = {'q': '23', 'w':'23'}
# tp = etree.parse('1.xml') # Парсинг файла
# nodes = tp.xpath('/soft/os/item') # Открываем раздел
# for node in nodes: # Перебираем элементы
#     print node.tag,node.keys(),node.values()
#     print 'name =',node.get('name') # Выводим параметр name
#     print 'text =',[node.text] # Выводим текст элемента




init_population = generate_init_population()
result = False
counter = 0
while counter < 500:
    print("************************************************************************************************************"
          "************************************************************************************************************")
    print(counter)
    best_individuals = deepcopy(reproduce(init_population))

    if len(best_individuals) == 0:
        print("Reproduction empty")
        break

    new_generation = deepcopy(create_new_generation(best_individuals))
    mutated_trees = deepcopy(mutate_trees(new_generation))
    check_fitness(mutated_trees)
    init_population = deepcopy(mutated_trees)

    if len(init_population) == 0:
        print("Empty population")
        break
    counter += 1

print("End")
if len(results) > 0:
    print("")
    print ("MIN RESULT")
    print (Tree.tree_map_to_string(min(results)))
    print (min(results).init_tree)
    print (min(results).fitness)