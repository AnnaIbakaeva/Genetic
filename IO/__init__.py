#-*- coding: utf-8 -*-
import tree_creation
from crossover import Crossover
from tree import Tree
from polish_notation import get_polish_notation, calculate_polish_notation, notation_to_str
from functions import TwoVariableFunction, Function
from reproduction import Reproductor
from random import randint

trees = []
i = 0
while i < 5:
    tree_creator = tree_creation.TreeCreator(5)
    if i % 2 == 0:
        tree_creator.create(False)
    else:
        tree_creator.create(True)
    tree = tree_creator.tree
    trees.append(tree)
    print(Tree.string_tree_map(tree.tree_map))
    print(tree.init_tree)
    print("")
    i += 1

result = False
while not result:
    reproductor = Reproductor(trees, 20)
    population = list(reproductor.select())
    print("REPRODUCTOR")
    for tree in population:
        print(Tree.string_tree_map(tree.tree_map))
        print(tree.init_tree)
        print("")

    i = 0
    cross_trees = []
    while i+1 < len(population):
        crossover = Crossover(population[i], population[i+1])
        crossover.cross()
        print("CROSSOVER")
        print(Tree.string_tree_map(crossover.new_tree1.tree_map))
        print(crossover.new_tree1.init_tree)
        print("")
        cross_trees.append(crossover.new_tree1)
        print(Tree.string_tree_map(crossover.new_tree2.tree_map))
        print(crossover.new_tree2.init_tree)
        print("")
        cross_trees.append(crossover.new_tree2)
        i += 1

    # for tree in cross_trees:
    #     value = randint(1, 10)
    #     if value == 1:
    #         tree.mutate_from_term_to_term()
    #     else:
    #         value = randint(1, 50)
    #         if value == 1:
    #             tree.mutate_from_func_to_func()
    #         else:
    #             value = randint(1, 100)
    #             if value == 1:
    #                 tree.mutate_from_func_to_term()
    #             else:
    #                 value = randint(1, 150)
    #                 if value == 1:
    #                     tree.mutate_from_term_to_func()

    for tree in cross_trees:
        if reproductor.get_fitness(tree) < 0.00001:
            print("RESULT")
            print(Tree.string_tree_map(tree.tree_map))
            print(tree.init_tree)
            result = True

    trees = list(cross_trees)
    if len(trees) == 0:
        print("Empty population")
        result = True

# cr = Crossover(full_tree, grow_tree)
# cr.cross()
# print("")
# print("CROSS TREE1")
# print(cr.new_tree1.init_tree)
# print(Tree.string_tree_map(cr.new_tree1.tree_map))
# print("")
# print("CROSS TREE2")
# print(cr.new_tree2.init_tree)
# print(Tree.string_tree_map(cr.new_tree2.tree_map))
# print("")

# print("POLISH NOTATION1")
# notation = get_polish_notation(cr.new_tree1)
# notation_str = notation_to_str(notation)
# print(notation_str)
# print("")
# print("POLISH NOTATION2")
# notation = get_polish_notation(cr.new_tree2)
# notation_str = notation_to_str(notation)
# print(notation_str)
# print("")
# print(calculate_polish_notation(notation, variable_values))