from functions import OneVariableFunction, TwoVariableFunction
from random import randint, uniform, choice

function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt'),
                TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'), TwoVariableFunction('*')]

one_variable_function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                             OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt')]

two_variable_function_set = [TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'),
                             TwoVariableFunction('*')]

variable_set = ['x', 'y', 'z']

variable_values_set = [
    {'x': 0, 'y': 0, 'z': 2},
    {'x': 0, 'y': 1, 'z': 2},
    {'x': 1, 'y': 1, 'z': 3},
    {'x': 1, 'y': 0, 'z': 3}
]

target_values = [5.43656365691809, 12.611614377411055, 11.94586961052814, 5.14957709864671]


def get_terminal():
    var = randint(0, 1)
    if var == 1:
        return uniform(-100, 100)
    return choice(variable_set)


