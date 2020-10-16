import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import constants
from frames import SettingsArea, GraphArea

from de_solver import DifferentialEq
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
        self.resizable(width=False, height=False)
        
        graph = GraphArea(self)
        graph.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        settings = SettingsArea(self, graph.tabs_list)
        settings.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=constants.LOG_FORMAT)
    logging.info('Start app')
    
    y_prime = lambda x,y: (y**2 +x*y - x**2) / x**2
    y = lambda x: x * (1 + x**2/3) / (1 - x**2/3)
    
    diff = DifferentialEq(y_prime, y, 1, 2, 1.5, 5, '')

    root = Root(diff)
    style = ThemedStyle(root)
    style.set_theme("breeze")
    root.mainloop()


