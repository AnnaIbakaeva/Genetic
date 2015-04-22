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

            self._get_new_tree(self._parent1, self._parent2.children, self._parent2.children_map, self.new_tree1)
            self._get_new_tree(self._parent2, self._parent1.children, self._parent1.children_map, self.new_tree2)
        else:
            self.cross()

    def _get_new_tree(self, tree, children, children_map, new_tree):
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
