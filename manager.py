from function import Function
from typing import List, Dict
from de_solver import Method, DifferentialEq

import logging

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
