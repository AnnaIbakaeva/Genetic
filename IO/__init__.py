#-*- coding: utf-8 -*-
import tree_creation
from crossover import Crossover
from tree import Tree
from polish_notation import get_polish_notation, calculate_polish_notation, notation_to_str
from functions import TwoVariableFunction, Function

# def create_grow_tree_population(count, creator):
#     population = []
#     for i in count:
#         creator.create(False)
#         population.append(tree_creator.tree)
#     return population
#
#
# def create_full_tree_population(count, creator):
#     population = []
#     for i in count:
#         creator.create(True)
#         population.append(tree_creator.tree)
#     return population


tree_creator = tree_creation.TreeCreator(5)
tree_creator.create(False)
grow_tree = tree_creator.tree

tree_creator2 = tree_creation.TreeCreator(5)
tree_creator2.create(True)
full_tree = tree_creator2.tree
# full_trees = create_full_tree_population(1, tree_creator)
# grow_trees = create_grow_tree_population(1, tree_creator)
# init_population = full_trees + grow_trees
#tree_maps = [grow_map, full_map]
#trees = [grow_tree, full_tree]

print("GROW TREE")
print(Tree.string_tree_map(grow_tree.tree_map))
print(grow_tree.init_tree)

print("")
print("FULL TREE")
print(Tree.string_tree_map(full_tree.tree_map))
print(full_tree.init_tree)
print("")

cr = Crossover(full_tree, grow_tree)
cr.cross()
print("")
print("CROSS TREE1")
print(cr.new_tree1.init_tree)
print(Tree.string_tree_map(cr.new_tree1.tree_map))
print("")
print("CROSS TREE2")
print(cr.new_tree2.init_tree)
print(Tree.string_tree_map(cr.new_tree2.tree_map))
print("")
print("POLISH NOTATION1")
notation = get_polish_notation(cr.new_tree1)
notation_str = notation_to_str(notation)
print(notation_str)
print("")
print("POLISH NOTATION2")
notation = get_polish_notation(cr.new_tree2)
notation_str = notation_to_str(notation)
print(notation_str)
print("")
print(calculate_polish_notation(notation, {'x': 2, 'y': 3, 'z': 4}))