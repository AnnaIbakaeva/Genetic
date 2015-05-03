from functions import Function, TwoVariableFunction
from sets import variable_set


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
    visited.append(current_vertex)
    notation.append(tree_map[current_vertex])
    if current_vertex < len(tree):
        for v in tree[current_vertex]:
            if not v in visited:
               notation = _create_polish_notation(tree, tree_map, v, visited, notation)
        return notation
    else:
        return notation


def get_value(term, var_values):
    if term in variable_set:
        return var_values[term]
    return term


def calculate_polish_notation(notation, var_values):
    operands = []
    i = len(notation) - 1
    while i >= 0:
        if isinstance(notation[i], Function):
            func = notation[i]
            if isinstance(func, TwoVariableFunction):
                o1 = get_value(operands.pop(), var_values)
                o2 = get_value(operands.pop(), var_values)
                operands.append(func.execute(o1, o2))
            else:
                result = func.execute(get_value(operands.pop(), var_values))
                operands.append(result)
        else:
            operands.append(notation[i])
        i -= 1
    return operands
