from functions import OneVariableFunction, TwoVariableFunction

#terminal_set = ['x', random.uniform(0.00001, 100)]

function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('exp'),
                OneVariableFunction('log'), OneVariableFunction('abs'), OneVariableFunction('sqrt'),
                TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'), TwoVariableFunction('*')]

one_variable_function_set = [OneVariableFunction('sin'), OneVariableFunction('cos'), OneVariableFunction('exp'),
                             OneVariableFunction('log'), OneVariableFunction('abs'), OneVariableFunction('sqrt')]

two_variable_function_set = [TwoVariableFunction('+'), TwoVariableFunction('-'), TwoVariableFunction('/'),
                             TwoVariableFunction('*')]


