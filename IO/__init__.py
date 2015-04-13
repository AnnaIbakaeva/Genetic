#-*- coding: utf-8 -*-
__author__ = 'Анна'
from tree_creation import TreeCreator
from functions import Function

tree_creator = TreeCreator(5)
tree_creator.create(False)

for key in tree_creator.tree_map.keys():
    if isinstance(tree_creator.tree_map[key], Function):
        print(str(key)+": "+ tree_creator.tree_map[key].function_name)
    else:
        print(str(key)+": "+ str(tree_creator.tree_map[key]))

print(tree_creator.tree)