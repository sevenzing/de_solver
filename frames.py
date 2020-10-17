import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from functools import partial
import logging

from de_solver import DifferentialEq, Manager
from function import Function
from typing import List, Tuple
import constants


class PlotTab(tk.Frame):
    '''
    Respresents a tab (вкладка) 
    '''
    def __init__(self, parent: tk.Frame, label: str, functions: List[Function]):
        super().__init__(parent, width=750, height=600)
        self.label = label
        self.funcs = functions

        fig = Figure(figsize=(5, 5), dpi=100)
        
        self.graph = fig.add_subplot(1, 1, 1)
        
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
        
        legend = []
        # show only non-hide functions
        for i, func in enumerate(filter(lambda f: not f.hide, self.funcs)):
            X = func.X
            Y = func.Y
            self.graph.plot(X, Y, color=func.color)
            if func.name:
                legend.append(func.name)

        self.graph.set_xlabel("x")
        self.graph.set_ylabel("y")
        
        self.graph.legend(legend)

        self.canvas.draw()
        self.toolbar.update()

    def __repr__(self):
        return f"Tab({self.label})"


class SettingsArea(tk.Frame):
    def __init__(self, parent, tabs: List[PlotTab], manager: Manager):
        logging.info('Connecting settings')
        super().__init__(parent)
        self.tabs = tabs
        self.diff_eq: DifferentialEq = manager.diff
        self.manager = manager

        title = ttk.Label(self, text=f"Solving {self.diff_eq.repr}", font=("Arial", 18))
        title.grid(column=0)

        ttk.Label(self, text="x_0")
        self.x_0 = ttk.Entry(self, )
        self.x_0.insert(tk.END, self.diff_eq.x_0)
        
        ttk.Label(self, text="y_0")
        self.y_0 = ttk.Entry(self)
        self.y_0.insert(tk.END, self.diff_eq.y_0)

        ttk.Label(self, text="x_n")
        self.x_n = ttk.Entry(self)
        self.x_n.insert(tk.END, self.diff_eq.x_n)

        ttk.Label(self, text="Grid size")
        self.n = ttk.Entry(self)
        self.n.insert(tk.END, self.diff_eq.n)
        
        ttk.Label(self, text="n_0 (for GTE)")
        self.n_start = ttk.Entry(self)
        self.n_start.insert(tk.END, self.diff_eq.n_start)

        ttk.Label(self, text="N (for GTE)")
        self.n_end = ttk.Entry(self)
        self.n_end.insert(tk.END, self.diff_eq.n_end)

        for i, child in enumerate(self.winfo_children()[1:]):
            child.grid_configure(padx=5, pady=5)

            if isinstance(child, ttk.Label):
                child.grid(column=0, row=i + 1, sticky=(tk.W, tk.E))

            if isinstance(child, ttk.Entry):
                child.config(justify=tk.CENTER)
                child.grid(column=1, row=i, sticky=(tk.W, tk.E))

        self.available_functions = {}
        for method in manager.methods:
            show_method = tk.BooleanVar(value=True)
            check_box = ttk.Checkbutton(self, text=str(method), command=self.hide_functions, variable=show_method)
            check_box.grid(column=0, row=len(self.winfo_children()), sticky=(tk.W, tk.E))
            self.available_functions[str(method)] = show_method

        
        update_button = ttk.Button(
            self, 
            text=constants.UPDATE_BUTTON_NAME, 
            padding="10",
            command=self.update,
            width='30',
            )

        update_button.grid(column=0, columnspan=2, row=len(self.winfo_children()), pady='25', padx='25')
    
    def __update_all_tabs(self):
        for tab in self.tabs:
            tab.update()

    def update(self):
        '''
        Updates values of differential equation with manager
        '''
        try:
            self.manager.update(
                float(self.x_0.get()),
                float(self.y_0.get()),
                float(self.x_n.get()),
                int(self.n.get()),
                int(self.n_start.get()),
                int(self.n_end.get()),
                )
        except ValueError as e:
            logging.error(e)
            raise e
        
        self.__update_all_tabs()

    def hide_functions(self):
        self.manager.hide_functions({m: not v.get() for m, v in self.available_functions.items()})
        self.__update_all_tabs()

class GraphArea(tk.Frame):
    def __init__(self, parent, manager: Manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        logging.info('Connecting graph area')    
        self.manager = manager
        self.notebook = ttk.Notebook(self, padding="15", width=750, height=550)
        self.notebook.pack(fill='both', expand='yes')
        
        logging.info('Created Notebook')
        anal_solution = manager.solution
        
        self.tabs = [
            PlotTab(self, 'Solutions', [anal_solution]), 
            PlotTab(self, 'LTE', []),
            PlotTab(self, 'GTE', []),
            ]
        for method in manager.functions:
            funcs = manager.functions[method]
            for i in range(len(funcs)):
                self.tabs[i].funcs.append(funcs[i])

        logging.info('Created tabs')
        
        for tab in self.tabs:
            self.notebook.add(tab, text=tab.label)
            tab.update()
        logging.info('Added tabs to notebook')
    
    @property
    def tabs_list(self):
        return self.tabs
