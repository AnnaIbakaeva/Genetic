#-*- coding: utf-8 -*-
from random import randint
from functions import TwoVariableFunction, OneVariableFunction
from tree import Tree


class Crossover(object):

    def __init__(self, tree1, tree2):
        self._parent1 = Tree(tree1.init_tree, tree1.tree_map)
        self._parent2 = Tree(tree2.init_tree, tree2.tree_map)
        self.new_tree1 = Tree([], {})
        self.new_tree2 = Tree([], {})

    def cross(self):
        if len(self._parent1.init_tree) <= 2:
            index1 = 1
        else:
            index1 = randint(1, len(self._parent1.init_tree)-1)
        if len(self._parent2.init_tree) <= 2:
            index2 = 1
        else:
            index2 = randint(1, len(self._parent2.init_tree)-1)
        if (isinstance(self._parent1.tree_map[index1], TwoVariableFunction) and
                isinstance(self._parent2.tree_map[index2], TwoVariableFunction)) or \
                (isinstance(self._parent1.tree_map[index1], OneVariableFunction)
                 and isinstance(self._parent2.tree_map[index2], OneVariableFunction)):
            self._parent1.index = index1
            self._parent2.index = index2
            print("parent1: ", self._parent1.init_tree)
            print(Tree.string_tree_map(self._parent1.tree_map))
            print("parent2: ", self._parent2.init_tree)
            print(Tree.string_tree_map(self._parent2.tree_map))
            print("index1: ", index1, " index2: ", index2)
            print("")

            self._parent1.find_children()
            print("child1: ", self._parent1.children)
            print(Tree.string_tree_map(self._parent1.children_map))
            self._parent2.find_children()
            print("child2: ", self._parent2.children)
            print(Tree.string_tree_map(self._parent2.children_map))

            self._parent1.delete_subtree()
            print("del1: ", self._parent1.tree_del)
            print(Tree.string_tree_map(self._parent1.tree_map))
            self._parent2.delete_subtree()
            print("del2: ", self._parent2.tree_del)
            print(Tree.string_tree_map(self._parent2.tree_map))

            self.new_tree1 = Tree.add_child_to_tree(self._parent1, self._parent2.children, self._parent2.children_map)
            self.new_tree2 = Tree.add_child_to_tree(self._parent2, self._parent1.children, self._parent1.children_map)
        else:
            self.cross()
