from tkinter.ttk import Label, Entry, Button, Frame
from tkinter import filedialog, StringVar, DISABLED, NORMAL, messagebox
import tkinter as tk

import pandas as pd
class EFA_Frame(Frame):
    def __init__(self, master, pipeline,data,nexxt):
        super().__init__(master)

        self.pipeline = pipeline
        self.data = data
        self.nexxt = nexxt



    def adequacychecksefa(self):

        self.display(self.pipeline.check_validity())

    def applyefa(self):
        self.pipeline.check_number_of_factors()
        self.display(self.pipeline.final_factors_and_names())
    def applyCFA(self):
        self.pipeline.create_model_dict()
        self.display(self.pipeline.apply_CFA())

    def display(self, quote):
        self.pipeline.check_validity()
        root = tk.Tk()
        S = tk.Scrollbar(root)
        T = tk.Text(root, height=40, width=100)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(tk.END, quote)
        tk.mainloop()

    def next(self):
        self.nexxt()
    def start(self):
        self.pipeline.Standarize_Data(self.data)
        #print(self.pipeline.check_validity())

        self.title = Label(self,text="      Applying Factor Analysis            ",font = ("bold",13))
        self.title.pack()

        self.AdequacyChecksButton = Button(self,
                                           text="1.Perform Adequacy Checks and get results   ",
                                           command=self.adequacychecksefa)
        self.AdequacyChecksButton.pack(padx=50, pady=50)


        self.ApplyEFA = Button(self,
                                           text="2.Apply Exploratory Factor Analysis and get results",
                                           command=self.applyefa)
        self.ApplyEFA.pack(padx=50, pady=50)

        self.ApplyCFA = Button(self,
                               text="3.Apply Confirmatory Factor Analysis and get results",
                               command=self.applyCFA)
        self.ApplyCFA.pack(padx=50, pady=50)

        self.next_button = Button(self,
                                  text="Next",
                                  command=self.next)
        self.next_button.pack(padx=30, pady=30)



        self.pack(padx=50, pady=50)




