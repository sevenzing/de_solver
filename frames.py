import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from functools import partial
import logging

from function import Function
from typing import List, Tuple

class PlotTab(tk.Frame):
    '''
    Respresents a tab (вкладка) 
    '''
    def __init__(self, parent: tk.Frame, label: str, callback_functions: List[Function], legend: Tuple[str]=None):
        super().__init__(parent, width=750, height=400)
        self.label = label
        self.funcs = callback_functions
        self.legend = legend

        fig = Figure(figsize=(5, 5), dpi=100)

        self.graph = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update()
        
    def update(self):
        logging.info(f'Updating graph on {self.__repr__()}')
        self.graph.clear()
        
        for i, func in enumerate(self.funcs):
            X = func.X
            Y = func.Y
            self.graph.plot(X, Y)

        self.graph.set_xlabel("x")
        self.graph.set_ylabel("y")
        if self.legend:
            self.graph.legend(self.legend)

        self.canvas.draw()
        self.toolbar.update()

    def __repr__(self):
        return f"Tab({self.label})"


class SettingsArea(tk.Frame):
    def __init__(self, parent, tabs):
        logging.info('Connecting settings')
        super().__init__(parent)
        self.tabs = tabs
        
        # ---
        btn = ttk.Button(
            self, 
            text="Plot", 
            padding="10",
            command=partial(lambda tabs: list(map(lambda x: x.update(), tabs)), self.tabs),
            )

        btn.grid(column=0, columnspan=2, row=5, pady="25")


class GraphArea(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        logging.info('Connecting graph area')    
        
        self.notebook = ttk.Notebook(self, padding="15", width=750, height=550)
        self.notebook.pack(fill='both', expand='yes')
        
        logging.info('Created Notebook')
        
        x_2 = Function(start=1, stop=5, num=100, func=lambda x: x**2)
        x_3 = Function(start=1, stop=5, num=100, func=lambda x: x**3)

        self.tabs = [
            PlotTab(self, 'label1', [x_2, x_3], legend=('x^2', 'x^3')), 
            PlotTab(self, 'label2', [x_3])
            ]
        
        logging.info('Created tabs')
        
        for tab in self.tabs:
            self.notebook.add(tab, text=tab.label)

        logging.info('Added tabs to notebook')
    
    @property
    def tabs_list(self):
        return self.tabs
