#-*- coding: utf-8 -*-
__author__ = 'Анна'
from tree_creation import TreeCreator
from functions import Function


def create_grow_tree_population(count, creator):
    population = []
    for i in count:
        creator.create(False)
        population.append(tree_creator.tree)
    return population


def create_full_tree_population(count, creator):
    population = []
    for i in count:
        creator.create(True)
        population.append(tree_creator.tree)
    return population


tree_creator = TreeCreator(5)
full_trees = create_full_tree_population(10, tree_creator)
grow_trees = create_grow_tree_population(10, tree_creator)
init_population = full_trees + grow_trees

# for key in tree_creator.tree_map.keys():
#     if isinstance(tree_creator.tree_map[key], Function):
#         print(str(key)+": "+ tree_creator.tree_map[key].function_name)
#     else:
#         print(str(key)+": "+ str(tree_creator.tree_map[key]))
#
# print(tree_creator.tree)