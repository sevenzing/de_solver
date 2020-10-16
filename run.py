import tkinter as tk
from tkinter import ttk

import constants
from frames import SettingsArea, GraphArea

import logging

class Root(tk.Tk):
    '''
    Main class of tkinter
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    root = Root()
    root.mainloop()


