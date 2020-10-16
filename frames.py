import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from functools import partial
import logging

from de_solver import DifferentialEq
from function import Function
from typing import List, Tuple

class PlotTab(tk.Frame):
    '''
    Respresents a tab (вкладка) 
    '''
    def __init__(self, parent: tk.Frame, label: str, functions: List[Function], legend: Tuple[str]=None):
        super().__init__(parent, width=750, height=400)
        self.label = label
        self.funcs = functions
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
    def __init__(self, parent, tabs: List[PlotTab]):
        logging.info('Connecting settings')
        super().__init__(parent)
        self.tabs = tabs
        self.diff_eq: DifferentialEq = parent.diff_eq
        
        ttk.Label(self, text="x_0")
        self.x_0 = ttk.Entry(self)
        
        ttk.Label(self, text="y_0")
        self.y_0 = ttk.Entry(self)
        
        ttk.Label(self, text="x_n")
        self.x_n = ttk.Entry(self)
        
        ttk.Label(self, text="Grid size")
        self.n = ttk.Entry(self)
        

        for i, child in enumerate(self.winfo_children()):
            child.grid_configure(padx=5, pady=5)

            if isinstance(child, ttk.Label):
                child.grid(column=0, row=i, sticky=(tk.W, tk.E))

            if isinstance(child, ttk.Entry):
                child.config(justify=tk.CENTER)
                child.grid(column=1, row=i - 1, sticky=(tk.W, tk.E))

        # ---
        update_button = ttk.Button(
            self, 
            text="Plot", 
            padding="10",
            command=self.update,
            )

        update_button.grid(column=0, columnspan=2, row=10, pady='25', padx='25')
    def update(self):
        '''
        Updates values of differential equation
        '''
        logging.info(f'Update differential eq with {self.x_0.get()}, {self.y_0.get()}, {self.x_n.get()}, {self.n.get()}')
        # TODO: обновлять функции, манагер или ссылки или че-нить
        try:
            self.diff_eq.x_0 = int(self.x_0.get())
            self.diff_eq.y_0 = int(self.y_0.get())
            self.diff_eq.x_n = int(self.x_n.get())
            self.diff_eq.n = int(self.n.get())
        except ValueError as e:
            logging.error(e)
        for tab in self.tabs:
            tab.update()

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
