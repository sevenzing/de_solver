import numpy as np
from inspect import getmembers

import logging

class Function:
    def __init__(self, domain=None, values=None, func=None, start=None, stop=None, num=None, hide=False, name=None):
        self.func = func
        self.X = np.array(domain)
        self.Y = np.array(values)
        self.start = start
        self.stop = stop
        self.num = num
        self.hide = hide
        self.name = name

        try:
            self.generate_X(start, stop, num)
        except TypeError:
            pass
        if self.func:
            self.generate_Y()
            
    def generate_X(self, start, stop, num):
        self.start = start
        self.stop = stop
        self.num = num

        self.X = np.linspace(start, stop, num) 
        return self.X
    
    def generate_Y(self):
        self.Y = self.func(self.X)
        return self.Y
    
    def append(self, x, y):
        self.X = np.append(self.X, [x])
        self.Y = np.append(self.Y, [y])

    def assign(self, other_function):
        self.X = other_function.X
        self.Y = other_function.Y
        self.func = other_function.func
        self.start = other_function.start
        self.stop = other_function.stop
        self.num = other_function.num

    def __str__(self):
        return 'Function (' + ','.join([self.X.__str__() , self.Y.__str__()]) + ')'

if __name__ == "__main__":
    f = Function(func=lambda x: x**2)
    f.generate_X(1, 20, 100)
    print(f.generate_Y())
