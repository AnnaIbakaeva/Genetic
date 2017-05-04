from functions import OneVariableFunction, TwoVariableFunction
from random import randint, uniform, choice
from constants import VARIABLE_SET

function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt'),
                TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'), TwoVariableFunction('*')]

one_variable_function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('my_exp'),
                             OneVariableFunction('my_log'), OneVariableFunction('fabs'), OneVariableFunction('my_sqrt')]

two_variable_function_set = [TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'),
                             TwoVariableFunction('*')]


def get_terminal():
    var = randint(0, 1)
    if var == 1:
        return uniform(-100, 100)
    return choice(VARIABLE_SET)


