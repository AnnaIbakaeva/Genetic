#-*- coding: utf-8 -*-
from tree_creation import TreeCreator
from functions import Function
from crossover import Crossover
from tree import Tree


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


tree_creator = TreeCreator(5)
tree_creator.create(False)
grow_tree = tree_creator.tree

tree_creator2 = TreeCreator(5)
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