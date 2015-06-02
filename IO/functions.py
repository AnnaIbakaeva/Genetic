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
        if var2 == 0 and self.function_name == '/':
            return 1
        try:
            return eval(str(var1) + self.function_name + str(var2))
        except OverflowError:
            print("function: ", self.function_name, var1, var2)


class OneVariableFunction(Function):
    def __init__(self, function_name):
        Function.__init__(self, function_name)

    def execute(self, var1, var2=None):
        try:
            result = eval(self.function_name+'('+str(var1)+')')
            return result
        except OverflowError:
            print("function: ", self.function_name, var1)


def my_log(x):
    try:
        if x == 0:
            x += 0.000001
        return log(fabs(x))
    except:
        print("log except x ", x)
        exit()


def my_sqrt(x):
    try:
        return sqrt(fabs(x))
    except:
        print("sqrt except x ", x)
        exit()


def my_exp(x):
    try:
        if x > 700:
            x = 700
        result = exp(x)
        return result
    except:
        print("exp except, x: ", x)
        exit()
