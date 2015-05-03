from math import cos, sin, fabs, exp, log, sqrt


class Function(object):
    def __init__(self, function_name):
        self.function_name = function_name

    def execute(self, var1, var2):
        pass


class TwoVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2):
        return eval(str(var1) + self.function_name + str(var2))


class OneVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2=None):
        return eval(self.function_name+'('+str(var1)+')')


def my_log(x):
    return log(fabs(x))


def my_sqrt(x):
    return sqrt(fabs(x))

