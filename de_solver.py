from typing import List, Tuple
from function import Function
import logging
from typing import Dict, List
from copy import deepcopy


class DifferentialEq:
    '''
    Represent first-order linear ordinary differential equation
    
    y'(x) = f(x, y(x)) 
    y(x_0) = y_0
    '''
    def __init__(self, f, f_solution, x_0, y_0, x_n, n, n_start, n_end, _repr: str):
        self.f = f
        self.f_solution = f_solution
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_n = x_n
        self.n_initital = n
        self.n = n
        self.n_start = n_start
        self.n_end = n_end
        self.repr = _repr

    @property
    def solution(self):
        return self.f_solution(self.x_0, self.y_0)

    @property
    def h(self):
        return (self.x_n - self.x_0) / self.n
        
    def __str__(self):
        return self.repr

class Method:
    def __init__(self, color=None):
        '''
        Represenst interface of iteration method
        '''
        self.color = color # color of functions of this method

    def get_next_value(self, f, x_i, y_i, h):
        raise NotImplementedError('you should implement it first')
    
    def solve(self, diff: DifferentialEq, precision=4) -> Tuple[Function]:
        '''
        Returns tuple of (method-derived function, LTE function, GTE function)
        '''
        # getting result function and lte
        result, lte, _ = self.__solve_de(
            diff.f, 
            diff.solution,
            diff.x_0,
            diff.y_0,
            diff.x_n,
            diff.n,
            precision=precision,
            )
        
        # calculate gte for all n from `n_start` to `n_end`
        gte = Function()
        for n in range(diff.n_start, diff.n_end):
            _, _, gte_values = self.__solve_de(
                diff.f, 
                diff.solution,
                diff.x_0,
                diff.y_0,
                diff.x_n,
                n,
                precision=precision,
            )
            gte.append(n, max(gte_values.Y))
        
        return result, lte, gte
        

    def __solve_de(self, f, y_solution_func, x_0, y_0, x_n, n, precision=4):
        h = (x_n - x_0) / n
        assert(h > 0, 'x_n should be greater than x_0')
        logging.debug(f"Solving eq with steps {h}")
        result_function = Function([], [])
        lte_function = Function([], [])
        gte_function = Function([], [])
        x_i = x_0
        y_i = y_0
        LTE = 0
        GTE = 0
        while x_i <= x_n:
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
            x_i  = round(x_i + h, precision)
            y_init = y_solution_func(x_i)
        return (result_function, lte_function, gte_function)


    def __str__(self):
        return self.__class__.__name__

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



class Manager:
    '''
    Class for managing changes of values of diff. eq
    '''
    def __init__(self, diff: DifferentialEq, methods: List[Method], solution_color='blue'):
        self.diff = diff
        self.methods = methods
        self.functions: Dict[List[Function]] = {
            str(method):[Function(name=str(method), color=method.color) for _ in range(len(methods))] 
                for method in methods 
            }
        self.solution = Function(name='Analytical solution', color=solution_color)
        self.update()

    def update(self, x_0=None, y_0=None, x_n=None, n=None, n_start=None, n_end=None):
        logging.info(f"Update differential eq with {x_0}, {y_0}, {x_n}, {n}, {n_start}, {n_end}")
        self.diff.x_0 = x_0 or self.diff.x_0
        self.diff.y_0 = y_0 or self.diff.y_0
        self.diff.x_n = x_n or self.diff.x_n
        self.diff.n = n or self.diff.n
        self.diff.n_start = n_start or self.diff.n_start
        self.diff.n_end = n_end or self.diff.n_end

        for method in self.methods:
            for func, new_func in zip(
                self.functions[method.__str__()],
                method.solve(self.diff)):

                #logging.debug(f"Function assign {func} {new_func}")
                func.assign(new_func)
        
        self.__update_solution()
        
    def __update_solution(self):
        new_solution = Function(func=self.diff.solution, start=self.diff.x_0, stop=self.diff.x_n, num=self.diff.n)
        self.solution.assign(new_solution)

    def hide_functions(self, methods: Dict[str, bool]):
        for method in methods:
            for func in self.functions[method]:
                func.hide = methods[method]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    y_prime = lambda x,y: 3 * y**(2/3)
    
    def f_solution(x_0, y_0):
        '''
        Since solution depends on constant C
        and constant depends on IVP, we need function 
        that returns function of solution
        '''
        def solution(x):
            '''
            Calculates the real solution according to IVP
            '''
            return (x + (y_0**(1/3) - x_0))**3
        
        return solution
    
    diff = DifferentialEq(y_prime, f_solution, 2, 27, 10, 10, '')
    x = 2
    print(diff.solution(x) == (x+1)**3)
    print(Manager(diff, [RungeKuttaMethod]).functions['RungeKuttaMethod'][0])
 