from typing import List, Tuple
from function import Function

class DifferentialEq:
    '''
    Represent first-order linear ordinary differential equation
    
    y'(x) = f(x, y(x)) 
    y(x_0) = y_0
    '''
    def __init__(self, f, solution, x_0, y_0, x_n, n, _repr: str):
        self.f = f
        self.solution = solution
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_n = x_n
        self.n = n
        self.h = (x_n - x_0) / n
        self.repr = _repr

    def __str__(self):
        return self.repr

class Method:
    def get_next_value(self, f, x_i, y_i, h):
        raise NotImplementedError('you should implement it first')
    
    def solve(self, diff_eq: DifferentialEq, presicion=4) -> List[Function]:
        '''
        Returns method-derived function, LTE function, GTE function
        '''
        result_function = Function([], [])
        lte_function = Function([], [])
        gte_function = Function([], [])
        f = diff_eq.f
        y_solution_func = diff_eq.solution
        x_i = diff_eq.x_0
        y_i = diff_eq.y_0
        y_init = diff_eq.y_0
        h = diff_eq.h
        LTE = 0
        GTE = 0
        while x_i <= diff_eq.x_n:
            # add values to result functions 
            result_function.append(x_i, y_i)
            lte_function.append(x_i, LTE)
            gte_function.append(x_i, GTE)
            
            # execute method
            y_i = self.get_next_value(f, x_i, y_i, h)
            # errors
            LTE = abs(y_solution_func(x_i + h) - self.get_next_value(f, x_i, y_solution_func(x_i), h))
            GTE = abs(y_solution_func(x_i + h) - y_i)
            # step 
            x_i  = round(x_i + h, presicion)
            y_init = y_solution_func(x_i)
        return (result_function, lte_function, gte_function)

class EulerMethod(Method):
    def get_next_value(self, f, x_i, y_i, h):
        # https://en.wikipedia.org/wiki/Euler_method
        return y_i + h * f(x_i, y_i)


class ImprovedEulerMethod(Method):
    def get_next_value(self, f, x_i, y_i, h):
        # https://en.wikipedia.org/wiki/Heun%27s_method
        k_1i = f(x_i, y_i)
        k_2i = f(x_i + h, y_i + h * f(x_i, y_i))
        y_i = y_i + h/2 * (k_1i + k_2i)
        return y_i

class RungeKuttaMethod(Method):
    def get_next_value(self, f, x_i, y_i, h):
        # https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
        k_1i = f(x_i, y_i)
        k_2i = f(x_i + h/2, y_i + h/2*k_1i)
        k_3i = f(x_i + h/2, y_i + h/2*k_2i)
        k_4i = f(x_i + h, y_i + h*k_3i)

        return y_i + h/6*(k_1i+2*k_2i+2*k_3i+k_4i)


if __name__ == "__main__":
    y_prime = lambda x,y: (y**2 +x*y - x**2) / x**2
    y = lambda x: x * (1 + x**2/3) / (1 - x**2/3)
    
    diff = DifferentialEq(y_prime, y, 1, 2, 1.5, 5, '')
    print(RungeKuttaMethod().solve(diff,3)[2].Y)
