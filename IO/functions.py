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
        if var2 == 0:
            var2 += 0.000001
        try:
            return eval(str(var1) + self.function_name + str(var2))
        except:
            print("function: ", self.function_name, var1, var2)


class OneVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2=None):
        try:
            result = eval(self.function_name+'('+str(var1)+')')
            return result
        except:
            print("function: ", self.function_name, var1)


def my_log(x):
    if x == 0:
        x += 0.000001
    return log(fabs(x))


def my_sqrt(x):
    return sqrt(fabs(x))


def my_exp(x):
    if x > 700:
        x = 700
    return exp(x)

