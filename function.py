import numpy as np


class Function:

    def __init__(self, domain=None, values=None, func=None, start=None, stop=None, num=None):
        self.func = func
        self.domain = np.array(domain)
        self.values = np.array(values)
        self.start = start
        self.stop = stop
        self.num = num

        try:
            self.generate_X(start, stop, num)
        except TypeError:
            pass
            
    def generate_X(self, start, stop, num):
        self.start = start
        self.stop = stop
        self.num = num

        self.domain = np.linspace(start, stop, num) 
        return self.domain
    
    def generate_Y(self):
        self.values = self.func(self.domain)
        return self.values
    
    def append(self, x, y):
        self.domain = np.append(self.domain, [x])
        self.values = np.append(self.values, [y])

    @property
    def X(self):
        return self.domain
    
    @property
    def Y(self):
        return self.values
    
    def __str__(self):
        return 'Function (' + ','.join([self.X.__str__() , self.Y.__str__()]) + ')'

if __name__ == "__main__":
    f = Function(func=lambda x: x**2)
    f.generate_X(1, 20, 100)
    print(f.generate_Y())
