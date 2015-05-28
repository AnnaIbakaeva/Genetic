from functions import OneVariableFunction, TwoVariableFunction
from random import randint, uniform, choice

function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt'),
                TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'), TwoVariableFunction('*')]

one_variable_function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                             OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt')]

two_variable_function_set = [TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'),
                             TwoVariableFunction('*')]

variable_set = ['x']

variable_values_set = [
    {'x': 1},
    {'x': 2},
    {'x': 3},
    {'x': 4},
    {'x': 5},
    {'x': 6},
    {'x': 7},
    {'x': 8},
    {'x': 9},
    {'x': 10}
]

target_values = [0.16301714400855244, 0.03151207168586773, 0.058874069320250945, -0.07665327400006214,
                 0.09289826287958812, -0.10728389239595373, 0.11952223407657944, -0.12936833742951767,
                 -0.12936833742951767, -0.14114737487040882]
#(sin(3x) + log(sqrt(exp(2/x)))/7


def get_terminal():
    var = randint(0, 1)
    if var == 1:
        return uniform(-100, 100)
    return choice(variable_set)


