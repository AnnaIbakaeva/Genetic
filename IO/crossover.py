#-*- coding: utf-8 -*-
from random import randint
from functions import TwoVariableFunction, OneVariableFunction
from tree import Tree
from copy import deepcopy


class Crossover(object):

    def __init__(self, tree1, tree2):
        self._parent1 = Tree(tree1.init_tree, tree1.tree_map)
        self._parent2 = Tree(tree2.init_tree, tree2.tree_map)
        self.new_tree1 = Tree([], {})
        self.new_tree2 = Tree([], {})
        self.max_recursion_depth = 10
        self.current_recursion_depth = 0

    def cross(self):
        try:
            if len(self._parent1.init_tree) <= 1 or len(self._parent2.init_tree) <= 1 \
                    or self.current_recursion_depth >= self.max_recursion_depth:
                return False
            index1 = self._get_index(list(self._parent1.init_tree))
            index2 = self._get_index(list(self._parent2.init_tree))
            is_arity_equal = False
            while not is_arity_equal and self.current_recursion_depth < self.max_recursion_depth:
                if (isinstance(self._parent1.tree_map[index1], TwoVariableFunction) and
                        isinstance(self._parent2.tree_map[index2], TwoVariableFunction)) or \
                        (isinstance(self._parent1.tree_map[index1], OneVariableFunction)
                         and isinstance(self._parent2.tree_map[index2], OneVariableFunction)):
                    is_arity_equal = True
                    self._parent1.index = index1
                    self._parent2.index = index2

                    self._parent1.find_children()
                    self._parent2.find_children()

                    self._parent1.delete_subtree()
                    self._parent2.delete_subtree()

                    self.new_tree1 = Tree.add_child_to_tree(self._parent1, self._parent2.children, self._parent2.children_map)
                    self.new_tree2 = Tree.add_child_to_tree(self._parent2, self._parent1.children, self._parent1.children_map)
                    return True
                else:
                    index2 = self._get_index(deepcopy(self._parent2.init_tree))
                self.current_recursion_depth += 1
                return False
        except:
            print("Cross except")
            print("parent1 ",self._parent1.init_tree)
            print(Tree.string_tree_map(self._parent1.tree_map))
            print("index1 ", index1)
            print("parent2 ", self._parent2.init_tree)
            print(Tree.string_tree_map(self._parent2.tree_map))
            print("index2 ", index2)

    def _get_index(self, tree_struct):
        index = 1
        if len(tree_struct) > 2:
            index = randint(1, len(tree_struct)-1)
        return index
