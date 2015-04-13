#-*- coding: utf-8 -*-
__author__ = 'Анна'
from tree_creation import TreeCreator
from functions import Function

tree_creator = TreeCreator(3)
tree_creator.create(True)

for key in tree_creator.tree_map.keys():
    print(str(key)+": ")
    if isinstance(tree_creator.tree_map[key], Function):
        print(tree_creator.tree_map[key].function_name)
    else:
        print(tree_creator.tree_map[key])

print(tree_creator.tree)