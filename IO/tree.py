#-*- coding: utf-8 -*-
from random import randint, choice
from functions import Function, OneVariableFunction, TwoVariableFunction
from sets import one_variable_function_set, two_variable_function_set, get_terminal
import tree_creation
from copy import deepcopy
from constants import MAX_DEPTH, VARIABLE_SET


class Tree(object):

    def __init__(self, tree_struct, tree_map, id):
        self.id = id
        self.init_tree = list(tree_struct)
        self.tree_map = dict(tree_map)
        self.tree_del = deepcopy(tree_struct)
        self.childs_counter = 1  #счетчик количества вершин у поддерева
        self.children = None
        self.vertex_counter = 0
        self.index = 0
        self.fitness = 100

    @staticmethod
    def tree_map_to_string(tree_map):
        string = ""
        for key in tree_map.keys():
            if isinstance(tree_map[key], Function):
                string += str(key) + ": " + tree_map[key].function_name
            else:
                string += str(key) + ": " + str(tree_map[key])
            string += "; "
        return string

    def check_var_existence(self):
        for key in self.tree_map.keys():
            if self.tree_map[key] in VARIABLE_SET:
                return True
        return False

    def find_children(self):
        self.children.tree_map[0] = self.tree_map[self.index]
        self._find_children([self.index], [])

    def _find_children(self, queue, visited):
        if len(queue) == 0:
            return
        vertex = queue[0]
        del queue[0]
        self.children.init_tree.append([])
        if vertex < len(self.init_tree):
            for v in self.init_tree[vertex]:
                if v not in visited:
                    queue.append(v)
                    visited.append(v)
                self.children.init_tree[len(self.children.init_tree)-1].append(self.childs_counter)
                self.children.tree_map[self.childs_counter] = self.tree_map[v]
                self.childs_counter += 1
        self._find_children(queue, visited)

    def delete_subtree(self):
        deleted_vertexes = []
        if self.index < len(self.init_tree):
            for v in self.init_tree[self.index]:
                if v < len(self.init_tree):
                    deleted_vertexes = self._calculate_deleted_vertexes(v, self.init_tree[v], deleted_vertexes)
            deleted_vertexes.sort(reverse=True)
            for ver in deleted_vertexes:
                del self.tree_del[ver]
            self.tree_del[self.index] = []
        self._recalculate_vertexes_number()
        self._delete_last_empty()

    def _calculate_deleted_vertexes(self, index, children, deleting):
        if index < len(self.init_tree) and index not in deleting:
            deleting.append(index)
        for v in children:
            if v < len(self.init_tree):
                self._calculate_deleted_vertexes(v, self.init_tree[v], deleting)
        return deleting

    def _recalculate_vertexes_number(self):
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
    def _get_last_vertex_number(tree):
        last_vertex_number = 0
        for vertex in tree.tree_map.keys():
            if vertex > last_vertex_number:
                last_vertex_number = vertex
        return last_vertex_number

    def _add_parent_residue(self, new_tree, current_position, saved_vertexes, next_vertex_number):
        while current_position < len(self.tree_del):
            new_tree.init_tree.append([])
            last_position = len(new_tree.init_tree)-1
            if last_position in saved_vertexes:
                saved_vertexes.remove(last_position)
                continue
            for v in self.tree_del[current_position]:
                new_tree.init_tree[len(new_tree.init_tree) - 1].append(next_vertex_number)
                new_tree.tree_map[next_vertex_number] = self.tree_map[v]
                next_vertex_number += 1
            current_position += 1
        return new_tree

    def _copy_constant_tree_part(self):
        new_tree = Tree([], {})
        new_tree.tree_map[0] = self.tree_map[0]
        n = self.index
        for i in range(0, n):
            new_tree.init_tree.append([])
            if i < len(self.tree_del):
                for j in range(0, len(self.tree_del[i])):
                    new_tree.init_tree[len(new_tree.init_tree) - 1].append(self.tree_del[i][j])
                    new_tree.tree_map[self.tree_del[i][j]] = self.tree_map[self.tree_del[i][j]]
        return new_tree

    def _add_child(self, new_tree, next_vertex_number):
        index = self.index
        saved_vertexes = [] #новые добавленные вершины текущего шага
        saved_vertexes2 = []
        last_adding_parent_vertex = len(self.tree_del)
        new_vertex_counter = 0
        for vs in self.children.init_tree:
            new_tree.init_tree.append([])
            if self.children.init_tree.index(vs) > 0:
                new_vertex_counter += 1
            if len(new_tree.init_tree)-1 in saved_vertexes2:
                saved_vertexes2.remove(len(new_tree.init_tree)-1)
            if len(vs) > 0:
                for v in vs:
                    new_tree.init_tree[len(new_tree.init_tree)-1].append(next_vertex_number)
                    new_tree.tree_map[next_vertex_number] = self.children.tree_map[v]
                    saved_vertexes.append(next_vertex_number)
                    next_vertex_number += 1
            if len(saved_vertexes2) > 0:
                if self.children.init_tree.index(vs) == len(self.children.init_tree)-1:
                    new_tree.init_tree.append([])
                    saved_vertexes2.remove(len(new_tree.init_tree)-1)
                    saved_vertexes2 = list(saved_vertexes)
                continue
            i = index + 1
            if len(saved_vertexes) == 0:
                m = i
            else:
                m = min(saved_vertexes) - new_vertex_counter
            while i < m and i <= self.vertex_counter:
                new_tree.init_tree.append([])
                if i < len(self.tree_del):
                    for k in self.tree_del[i]:
                        new_tree.init_tree[len(new_tree.init_tree) - 1].append(next_vertex_number)
                        new_tree.tree_map[next_vertex_number] = self.tree_map[k]
                        next_vertex_number += 1
                    last_adding_parent_vertex = i
                i += 1
            index = m - 1
            saved_vertexes2 = list(saved_vertexes)
            saved_vertexes = []
        last_adding_parent_vertex += 1
        new_tree = deepcopy(self._add_parent_residue(new_tree, last_adding_parent_vertex, saved_vertexes2, next_vertex_number))
        return new_tree

    def add_child_to_tree(self):
        """Добавляет дерево-потомок к текущему дереву-родителю.
        Корень дерева-потомка добавляется на заданный индекс текущего дерева.
        :return Новое дерево с присоединенным поддеревом"""
        index = self.index
        new_tree = deepcopy(self._copy_constant_tree_part())
        next_vertex_number = Tree._get_last_vertex_number(new_tree) + 1
        new_tree.tree_map[index] = self.children.tree_map[0]

        self._add_child(new_tree, next_vertex_number)

        if Tree.get_depth(new_tree.init_tree, 0, 0, [], []) > MAX_DEPTH:
            return Tree([], {})
        return new_tree

    def mutate_from_func_to_func(self):
        if len(self.init_tree) <= 1:
            return
        position = randint(0, len(self.init_tree)-1)
        if isinstance(self.tree_map[position], OneVariableFunction):
            self.tree_map[position] = choice(one_variable_function_set)
        elif isinstance(self.tree_map[position], TwoVariableFunction):
            self.tree_map[position] = choice(two_variable_function_set)
        else:
            self.mutate_from_func_to_func()

    def mutate_from_term_to_term(self):
        try:
            if len(self.init_tree) <= 1:
                return
            if len(self.tree_map.keys()) <= 2:
                position = 1
            else:
                position = randint(1, len(self.tree_map.keys())-1)
            if isinstance(self.tree_map[position], Function):
                self.mutate_from_term_to_term()
            else:
                self.tree_map[position] = get_terminal()
        except RuntimeError:
            return

    def mutate_from_func_to_term(self):
        if len(self.init_tree) <= 1:
            return
        else:
            position = randint(0, len(self.init_tree)-1)
        self.index = position
        self.tree_del = deepcopy(self.init_tree)
        self.delete_subtree()
        self.tree_map[position] = get_terminal()
        self.init_tree = self.tree_del

    def mutate_from_term_to_func(self):
        try:
            if len(self.tree_map.keys()) < 2:
                return
            if len(self.tree_map.keys()) < 3:
                position = 1
            else:
                position = randint(1, len(self.tree_map.keys())-1)
            if isinstance(self.tree_map[position], Function):
                self.mutate_from_term_to_func()
            else:
                depth = Tree.get_depth(self.init_tree, 0, 0, [], [])
                if depth < MAX_DEPTH:
                    creator = tree_creation.TreeCreator(3)
                    creator.create(False)
                    child = creator.tree
                    self.children = child

                    self.index = position
                    self.tree_del = deepcopy(self.init_tree)
                    self._recalculate_vertexes_number()

                    t = self.add_child_to_tree()
                    self.tree_del = deepcopy(t.tree_del)
                    self.init_tree = list(t.init_tree)
                    self.tree_map = t.tree_map
                else:
                    return
        except RuntimeError:
            return
        except:
            print("mutate_from_term_to_func EXCEPT")
            print(self.tree_map)
            print(position)
            exit()

    @staticmethod
    def get_depth(tree_struct, current_depth, index, visited, depths):
        visited.append(index)
        if index < len(tree_struct):
            for vertex in tree_struct[index]:
                if not (vertex in visited):
                    Tree.get_depth(tree_struct, current_depth+1, vertex, visited, depths)
            if len(depths) == 0:
                return 0
            return max(depths)
        else:
            depths.append(current_depth)
            return

    def get_coefficients(self):
        coefficients = []
        for keys in self.tree_map.keys():
            if not isinstance(self.tree_map[keys], Function):
                if not self.tree_map[keys] in VARIABLE_SET:
                    coefficients.append(self.tree_map[keys])
        return coefficients
