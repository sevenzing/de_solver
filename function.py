import numpy as np


class Function:

    def __init__(self, domain=None, values=None, func=None, start=None, stop=None, num=None):
        self.func = func
        self.domain = domain
        self.values = values
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
        return self.X
    
    def generate_Y(self):
        self.values = self.func(self.domain)
        return self.values
    @property
    def X(self):
        return self.domain
    
    @property
    def Y(self):
        return self.generate_Y()
    
if __name__ == "__main__":
    f = Function(func=lambda x: x**2)
    f.generate_X(1, 20, 100)
    print(f.generate_Y())
