import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import constants
from frames import SettingsArea, GraphArea

from de_solver import (
    DifferentialEq,  
    EulerMethod,
    ImprovedEulerMethod,
    RungeKuttaMethod,
    SampleMethod,
    )
from manager import Manager
import logging

class Root(tk.Tk):
    '''
    Main class of tkinter
    '''
    def __init__(self, diff_eq:DifferentialEq, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.diff_eq = diff_eq
        self.title(constants.APP_TITLE)
        self.geometry(constants.APP_SIZE)
        self.resizable(width=constants.RESIZE, height=constants.RESIZE)
        
        manager = self.get_manager()

        self.graph = GraphArea(self, manager)
        self.graph.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.settings = SettingsArea(self, self.graph.tabs_list, manager)
        self.settings.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), pady='25', padx='25')

    def get_manager(self) -> Manager:
        m = Manager(self.diff_eq, [
            EulerMethod(color='red'),
            ImprovedEulerMethod(color='orange'),
            RungeKuttaMethod(color='green'),
            SampleMethod(
                color='black', 
                title='My new method'
                ),
            ],
            solution_color='blue',
            )
        m.update()
        return m

if __name__ == "__main__":
    logging.basicConfig(level=constants.LOG_LEVEL, format=constants.LOG_FORMAT)
    logging.getLogger('matplotlib.font_manager').setLevel(logging.INFO)
    logging.info('Start app')
    
    diff = DifferentialEq(
        constants.f,
        constants.y_solution_getter,
        *constants.INITIAL_VALUES,
        )

    root = Root(diff)
    style = ThemedStyle(root)
    style.set_theme("breeze")
    
    root.mainloop()