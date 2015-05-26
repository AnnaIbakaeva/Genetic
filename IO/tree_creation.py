import random
from sets import function_set, variable_set, get_terminal
from functions import TwoVariableFunction, Function
from tree import Tree


class TreeCreator(object):

    def __init__(self, depth):
        self.depth = depth
        self._tree_struct = []
        self._tree_map = {}

    def create(self, full):
        self._tree_map[0] = random.choice(function_set)
        if full:
            self._full_tree()
        else:
            self._grow_tree()
        self.tree = Tree(self._tree_struct, self._tree_map)
        if not self.tree.check_var_existence():
            self._add_variable()

    def _full_tree(self, current_index=0, current_count=1):
        self._tree_struct.append([current_count])
        self._add_node(current_count)
        current_count += 1
        if isinstance(self._tree_map[current_index], TwoVariableFunction):
            self._tree_struct[len(self._tree_struct)-1].append(current_count)
            self._add_node(current_count)
            current_count += 1
        if self._get_current_depth() < self.depth:
            current_index += 1
            self._full_tree(current_index, current_count)

    def _grow_tree(self, current_index=0, current_count=1):
        if isinstance(self._tree_map[current_index], Function):
            self._tree_struct.append([current_count])
            self._add_node(current_count)
            current_count += 1
            if isinstance(self._tree_map[current_index], TwoVariableFunction):
                self._tree_struct[len(self._tree_struct)-1].append(current_count)
                self._add_node_in_grow(current_count)
                current_count += 1
            if self._get_current_depth() < self.depth:
                current_index += 1
                self._grow_tree(current_index, current_count)
        else:
            self._tree_struct.append([])
            current_index += 1
            if self._get_current_depth() < self.depth:
                self._grow_tree(current_index, current_count)

    def _get_max_depth(self):
        return Tree.get_depth(self._tree_struct, 0, 0, [], [])

    def _min_depth(self, current_depth, index, visited, depths):
        visited.append(index)
        try:
            for vertex in self._tree_struct[index]:
                if not (vertex in visited):
                    self._min_depth(current_depth+1, vertex, visited, depths)
            if len(depths) == 0:
                return 0
            return min(depths)
        except IndexError:
            depths.append(current_depth)
            return

    def _get_current_depth(self):
        return self._min_depth(0, 0, [], [])

    def _add_node(self, current_count):
        if self._get_max_depth() >= self.depth:
            self._tree_map[current_count] = get_terminal()
        else:
            self._tree_map[current_count] = random.choice(function_set)

    def _add_node_in_grow(self, current_count):
        if self._get_max_depth() >= self.depth or random.choice([0, 1]):
            self._tree_map[current_count] = get_terminal()
        else:
            self._tree_map[current_count] = random.choice(function_set)

    def _add_variable(self):
        terms = []
        for key in self._tree_map.keys():
            if not isinstance(self._tree_map[key], Function):
                terms.append(key)
        position = random.choice(terms)
        self._tree_map[position] = random.choice(variable_set)