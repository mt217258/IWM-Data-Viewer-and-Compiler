'''
Author  -    Matthew McLaughlin
Contact -    mt217258@dal.ca
'''

#### MODULE VERSION ####
CONST_SHARED_VERSION = "0.0.0" 

#### LIBRARIES ####
import tkinter as tk
from tkinter import ttk

import time

#### GLOBAL VARIABLES ####
pallette = {"c1": "#796F4B", "c2": "#70713B", "c3": "#5A5631", "c4": "#392C09", "c5": "#481E10"}

#### CLASSES ####
    #### Magic Methods
    #### Mangled Methods
    #### Muggle Methods

class ProgressBar():
    #### Magic Methods
    def __init__(self, message, numSteps):
        self.progress = 0
        self.progress_step = 100.0/float(numSteps)
        self.progress_var = tk.DoubleVar()
        self.message = message
        self.popup = tk.Toplevel()
        tk.Label(self.popup, text=self.message).grid(row=0,column=0)
        self.progress_bar = ttk.Progressbar(self.popup, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0)
        
    #### Mangled Methods
    #### Muggle Methods
    def update(self):
        self.popup.update()
        self.progress += self.progress_step
        self.progress_var.set(self.progress)
        if self.progress == 100.0:
            self.popup.destroy()
    
#### VULGER METHODS #### (They have no class)

#### MAIN ####
def main():  
    root = tk.Tk()

    test_bar = ProgressBar("Testing in progress", 10)

    tk.Button(root, text="Launch", command=test_bar.draw).pack()

    for i in range(0,10):
        time.sleep(1)
        test_bar.update()

    root.mainloop()
    
if __name__ == '__main__':
    main()