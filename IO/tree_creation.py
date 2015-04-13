import random
from sets import function_set
from functions import TwoVariableFunction, Function


class TreeCreator(object):
    tree = []
    tree_map = {}
    depth = 0

    def __init__(self, depth):
        self.depth = depth

    def create(self, full):
        self.tree_map[0] = random.choice(function_set)
        if full:
            return self._full_tree(0, 1)
        else:
            return self._grow_tree(0, 1)

    def _full_tree(self, current_index, current_count):
        self.tree.append([current_count])
        self._add_node(current_count)
        current_count += 1
        if isinstance(self.tree_map[current_index], TwoVariableFunction):
            self.tree[len(self.tree)-1].append(current_count)
            self._add_node(current_count)
            current_count += 1
        if self._get_current_depth() >= self.depth:
            return self.tree
        current_index += 1
        return self._full_tree(current_index, current_count)

    def _grow_tree(self, current_index, current_count):
        if isinstance(self.tree_map[current_index], Function):
            self.tree.append([current_count])
            self._add_node(current_count)
            current_count += 1
            if isinstance(self.tree_map[current_index], TwoVariableFunction):
                self.tree[len(self.tree)-1].append(current_count)
                self._add_node_in_grow(current_count)
                current_count += 1
            if self._get_current_depth() >= self.depth:
                return self.tree
            current_index += 1
            return self._grow_tree(current_index, current_count)
        else:
            self.tree.append([])
            current_index += 1
            return self._grow_tree(current_index, current_count)

    def _max_depth(self, current_depth, index, visited, depths):
        visited.append(index)
        try:
            for vertex in self.tree[index]:
                if not (vertex in visited):
                    self._max_depth(current_depth+1, vertex, visited, depths)
            if len(depths) == 0:
                return 0
            return max(depths)
        except IndexError:
            depths.append(current_depth)
            return

    def _get_max_depth(self):
        return self._max_depth(0, 0, [], [])

    def _min_depth(self, current_depth, index, visited, depths):
        visited.append(index)
        try:
            for vertex in self.tree[index]:
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
            self.tree_map[current_count] = random.uniform(0.00001, 100)
        else:
            self.tree_map[current_count] = random.choice(function_set)

    def _add_node_in_grow(self, current_count):
        if self._get_max_depth() >= self.depth or random.choice([0, 1]):
            self.tree_map[current_count] = random.uniform(0.00001, 100)
        else:
            self.tree_map[current_count] = random.choice(function_set)

    # def check_end_ability(self, parent_index):
    #     if isinstance(self.tree_map[parent_index], TwoVariableFunction):
    #         pass