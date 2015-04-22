#-*- coding: utf-8 -*-
from random import randint
from functions import Function


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
        print("deleting ", deleting)
        for ver in deleting:
            del self.tree_del[ver]

        self.tree_del[self.index] = []
        self._count_vertexes_number()
        print(Tree.string_tree_map(self.tree_map))
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

    def mutate(self):
        position = randint(1, len(self.init_tree)-1)
