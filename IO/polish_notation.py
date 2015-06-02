from functions import Function, TwoVariableFunction
from constants import VARIABLE_SET
from math import isinf


def notation_to_str(notation):
    notation_str = ""
    for elem in notation:
        if isinstance(elem, Function):
            notation_str += elem.function_name + " "
        else:
            notation_str += str(elem) + " "
    return notation_str


def get_polish_notation(tree):
    tree_struct = tree.init_tree
    tree_map = tree.tree_map

    return _create_polish_notation(tree_struct, tree_map, 0, [],  [])


def _create_polish_notation(tree, tree_map, current_vertex, visited, notation):
    try:
        visited.append(current_vertex)
        notation.append(tree_map[current_vertex])
        if current_vertex < len(tree):
            for v in tree[current_vertex]:
                if not v in visited:
                    notation = _create_polish_notation(tree, tree_map, v, visited, notation)
            return notation
        else:
            return notation
    except KeyError:
        print("current_vertex ", current_vertex)
        print("tree_map ", tree_map)
        print("tree ", tree)


def _get_value(term, var_values):
    if term in VARIABLE_SET:
        return var_values[term]
    return term


def calculate_polish_notation(notation, var_values):
    operands = []
    i = len(notation) - 1
    while i >= 0:
        if isinstance(notation[i], Function):
            func = notation[i]
            try:
                if isinstance(func, TwoVariableFunction):
                    o1 = _get_value(operands.pop(), var_values)
                    o2 = _get_value(operands.pop(), var_values)
                    if isinf(o1) or isinf(o2):
                        return float('inf')
                    operands.append(func.execute(o1, o2))
                else:
                    o1 = _get_value(operands.pop(), var_values)
                    if isinf(o1):
                        return float('inf')
                    result = func.execute(o1)
                    operands.append(result)
            except:
                print('ERROR')
                print(func.function_name, o1)
                print(notation_to_str(notation))
                exit()
        else:
            operands.append(notation[i])
        i -= 1
    return _get_value(operands[0], var_values)
