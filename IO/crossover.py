#-*- coding: utf-8 -*-
from random import randint
from functions import TwoVariableFunction, OneVariableFunction
from tree import Tree
from copy import deepcopy
from constants import MAX_RECURSION


class Crossover(object):

    def __init__(self, tree1, tree2):
        self._parent1 = Tree(tree1.init_tree, tree1.tree_map, tree1.id)
        self._parent2 = Tree(tree2.init_tree, tree2.tree_map. tree2.id)
        self.new_tree1 = Tree([], {})
        self.new_tree2 = Tree([], {})
        self.current_recursion_depth = 0

    def cross(self):
        try:
            if len(self._parent1.init_tree) <= 1 or len(self._parent2.init_tree) <= 1:
                return False
            index1 = self._get_index(list(self._parent1.init_tree))
            index2 = self._get_index(list(self._parent2.init_tree))
            while self.current_recursion_depth < MAX_RECURSION:
                if (isinstance(self._parent1.tree_map[index1], TwoVariableFunction) and
                        isinstance(self._parent2.tree_map[index2], TwoVariableFunction)) or \
                        (isinstance(self._parent1.tree_map[index1], OneVariableFunction)
                         and isinstance(self._parent2.tree_map[index2], OneVariableFunction)):
                    self._parent1.index = index1
                    self._parent2.index = index2

                    self._parent1.children = Tree([], {})
                    self._parent2.children = Tree([], {})

                    self._parent1.find_children()
                    self._parent2.find_children()

                    self._parent1.delete_subtree()
                    self._parent2.delete_subtree()

                    self.new_tree1 = self._parent1.add_child_to_tree()
                    self.new_tree2 = self._parent2.add_child_to_tree()
                    self.current_recursion_depth = 0
                    return True
                else:
                    index2 = self._get_index(deepcopy(self._parent2.init_tree))
                self.current_recursion_depth += 1
                return False
        except:
            print("Cross except")
            print("parent1 ",self._parent1.init_tree)
            print(Tree.tree_map_to_string(self._parent1.tree_map))
            print("index1 ", index1)
            print("parent2 ", self._parent2.init_tree)
            print(Tree.tree_map_to_string(self._parent2.tree_map))
            print("index2 ", index2)

    def _get_index(self, tree_struct):
        index = randint(0, len(tree_struct)-1)
        return index
