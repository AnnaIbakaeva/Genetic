#-*- coding: utf-8 -*-
from random import randint, choice, uniform
from functions import Function, OneVariableFunction, TwoVariableFunction
from sets import one_variable_function_set, two_variable_function_set, function_set
import tree_creation


class Tree(object):

    def __init__(self, tree_struct, tree_map):
        self.init_tree = tree_struct
        self.tree_map = tree_map
        self.tree_del = self.init_tree
        self.childs_counter = 1  #счетчик количества вершин у поддерева
        self.children = []
        self.children_map = {}
        self.vertex_counter = 0
        self.index = 0

    @staticmethod
    def string_tree_map(tree_map):
        string = ""
        for key in tree_map.keys():
            if isinstance(tree_map[key], Function):
                string += str(key) + ": " + tree_map[key].function_name
            else:
                string += str(key) + ": " + str(tree_map[key])
            string += "; "
        return string

    def find_children(self):
        self.children_map[0] = self.tree_map[self.index]
        self._find_children([self.index], [])

    def _find_children(self, queue, visited):
        if len(queue) == 0:
            return
        vertex = queue[0]
        del queue[0]
        if vertex < len(self.init_tree):
            self.children.append([])
            for v in self.init_tree[vertex]:
                if v not in visited:
                    queue.append(v)
                    visited.append(v)
                self.children[len(self.children)-1].append(self.childs_counter)
                self.children_map[self.childs_counter] = self.tree_map[v]
                self.childs_counter += 1
        self._find_children(queue, visited)

    def delete_subtree(self):
        deleting = []
        for v in self.init_tree[self.index]:
            if v < len(self.init_tree):
                deleting = self._count_delete_subtree(v, self.init_tree[v], deleting)
        deleting.sort(None, None, True)
        for ver in deleting:
            del self.tree_del[ver]

        self.tree_del[self.index] = []
        self._count_vertexes_number()
        self._delete_last_empty()

    def _count_delete_subtree(self, index, children, deleting):
        if index < len(self.init_tree) and index not in deleting:
            deleting.append(index)
        for v in children:
            if v < len(self.init_tree):
                self._count_delete_subtree(v, self.init_tree[v], deleting)
        return deleting

    def _count_vertexes_number(self):
        temp_map = dict(self.tree_map)
        self.tree_map = {0: temp_map[0]}
        count = 1
        i = 0
        while i < len(self.tree_del):
            j = 0
            while j < len(self.tree_del[i]):
                self.tree_map[count] = temp_map[self.tree_del[i][j]]
                self.tree_del[i][j] = count
                self.vertex_counter = count
                count += 1
                j += 1
            i += 1

    def _delete_last_empty(self):
        i = len(self.tree_del) - 1
        while i >= 0:
            if self.tree_del[i] == []:
                del self.tree_del[i]
            else:
                return
            i -= 1

    @staticmethod
    def add_child_to_tree(tree, children, children_map, new_tree):
        index = tree.index
        i = 0
        count = 0
        new_tree.tree_map[0] = tree.tree_map[0]
        while i < index:
            j = 0
            new_tree.init_tree.append([])
            while j < len(tree.tree_del[i]):
                new_tree.init_tree[len(new_tree.init_tree) - 1].append(tree.tree_del[i][j])
                new_tree.tree_map[tree.tree_del[i][j]] = tree.tree_map[tree.tree_del[i][j]]
                count = tree.tree_del[i][j]
                j += 1
            i += 1
        count += 1

        new_tree.tree_map[index] = children_map[0]

        save_counts = []
        save_counts2 = []
        last_m = 0
        new_vertex_counter = 0
        for vs in children:
            new_tree.init_tree.append([])
            if children.index(vs) > 0:
                new_vertex_counter += 1
            for v in vs:
                if len(new_tree.init_tree)-1 in save_counts2:
                    save_counts2.remove(len(new_tree.init_tree)-1)
                new_tree.init_tree[len(new_tree.init_tree)-1].append(count)
                new_tree.tree_map[count] = children_map[v]
                save_counts.append(count)
                count += 1
            if len(save_counts2) > 0:
                continue
            i = index + 1
            m = min(save_counts) - new_vertex_counter
            while i < m and i <= tree.vertex_counter:
                new_tree.init_tree.append([])
                if i < len(tree.tree_del):
                    for k in tree.tree_del[i]:
                        new_tree.init_tree[len(new_tree.init_tree) - 1].append(count)
                        new_tree.tree_map[count] = tree.tree_map[k]
                        count += 1
                i += 1
            index = m - 1
            last_m = min(save_counts)
            save_counts2 = save_counts
            save_counts = []
        while last_m < len(tree.tree_del):
            new_tree.init_tree.append([])
            if last_m in save_counts2:
                save_counts2.remove(last_m)
                continue
            for v in tree.tree_del[last_m]:
                new_tree.init_tree[len(new_tree.init_tree) - 1].append(count)
                new_tree.tree_map[count] = tree.tree_map[v]
                count += 1
            last_m += 1
        return new_tree

    def mutate_from_func_to_func(self):
        position = randint(0, len(self.init_tree)-1)
        if isinstance(self.tree_map[position], OneVariableFunction):
            self.tree_map[position] = choice(one_variable_function_set)
        else:
            self.tree_map[position] = choice(two_variable_function_set)

    def mutate_from_term_to_term(self):
        position = randint(2, len(self.tree_map.keys())-1)
        if isinstance(self.tree_map[position], Function):
            self.mutate_from_term_to_term()
        else:
            self.tree_map[position] = uniform(0.00001, 100)

    def mutate_from_func_to_term(self):
        position = randint(1, len(self.init_tree)-1)
        self.index = position
        self.delete_subtree()
        self.tree_map[position] = uniform(0.00001, 100)

    def mutate_from_term_to_func(self):
        position = randint(2, len(self.tree_map.keys())-1)
        if isinstance(self.tree_map[position], Function):
            self.mutate_from_term_to_func()
        else:
            creator = tree_creation.TreeCreator(4)
            creator.create(False)
            child = creator.tree
            self.tree_map[position] = child.tree_map[0]
            self.index = position
            self.tree_del = self.init_tree
            self.init_tree = Tree.add_child_to_tree(self, child.init_tree, child.tree_map, Tree([], {}))

