#-*- coding: utf-8 -*-
from random import randint
from functions import TwoVariableFunction, OneVariableFunction
from tree import Tree


class Crossover(object):

    def __init__(self, tree1, tree2):
        self._parent1 = tree1
        self._parent2 = tree2
        self.new_tree1 = Tree([], {})
        self.new_tree2 = Tree([], {})

    def cross(self):
        index1 = randint(1, len(self._parent1.init_tree)-1)
        index2 = randint(1, len(self._parent2.init_tree)-1)
        if (isinstance(self._parent1.tree_map[index1], TwoVariableFunction) and
                isinstance(self._parent2.tree_map[index2], TwoVariableFunction)) or \
                (isinstance(self._parent1.tree_map[index1], OneVariableFunction)
                 and isinstance(self._parent2.tree_map[index2], OneVariableFunction)):
            print("parent1, index1", self._parent1.init_tree, index1)
            print("parent2, index2", self._parent2.init_tree, index2)

            self._parent1.index = index1
            self._parent2.index = index2

            self._parent1.find_children()
            print("children1: ", self._parent1.children)
            print("children_map1: " + Tree.string_tree_map(self._parent1.children_map))
            self._parent2.find_children()
            print("children2: ", self._parent2.children)
            print("children_map2: " + Tree.string_tree_map(self._parent2.children_map))

            self._parent1.delete_subtree()
            print("tree_del1: ", self._parent1.tree_del)
            self._parent2.delete_subtree()
            print("tree_del2: ", self._parent2.tree_del)

            self.new_tree1 = Tree.add_child_to_tree(self._parent1, self._parent2.children, self._parent2.children_map,
                                                    self.new_tree1)
            self.new_tree2 = Tree.add_child_to_tree(self._parent2, self._parent1.children, self._parent1.children_map,
                                                    self.new_tree2)
        else:
            self.cross()
