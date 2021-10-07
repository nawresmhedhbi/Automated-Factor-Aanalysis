from tkinter.ttk import Label, Entry, Button, Frame

from tkinter import filedialog, StringVar, DISABLED, NORMAL, messagebox,Menu, IntVar, Menubutton , OptionMenu



import pandas as pd
from sklearn.pipeline import Pipeline
from preprocessors import Pipeline



class AutoMLmain(Frame):
    def __init__(self, master, data,next,pipeline):
        super().__init__(master)
        self.pipeline = pipeline
        self.data = data
        self.next = next







    def printValues(self):
        for name, var in self.choices.items():
            print("%s: %s" % (name, var.get()))

    def start(self):
        self.conf = Label(self,text="Some configurations before starting Predictions           ",font = ("bold",11))
        self.conf.grid(row=0, column=0)
        self.menubutton = Menubutton(self, text="Categorical Features",
                                   indicatoron=True, borderwidth=1, relief="raised")
        self.menu = Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.menu)

        self.label_menu2 = Label(self,
                                text="Select Categorical Features")
        self.label_menu2.grid(row=1, column=0, padx=20, pady=20)

        self.menubutton.grid(row=1, column=1, padx=20, pady=20)
        self.choices = {}

        for choice in self.data.columns.tolist():

            self.choices[choice] = IntVar(value=0)
            self.menu.add_checkbutton(label=choice, variable=self.choices[choice],
                             onvalue=1, offvalue=0,
                             command=self.printValues)
        self.menubutton2 = Menubutton(self, text="Numerical Features",
                                     indicatoron=True, borderwidth=1, relief="raised")
        self.menu2 = Menu(self.menubutton2, tearoff=False)
        self.menubutton2.configure(menu=self.menu2)
        self.label_menu3 = Label(self,
                                 text="Select Numerical Features")

        self.label_menu3.grid(row=2, column=0, padx=20, pady=20)
        self.menubutton2.grid(row=2, column=1, padx=20, pady=20)
        self.choices2 = {}

        for choice in self.data.columns.tolist():
            self.choices2[choice] = IntVar(value=0)
            self.menu2.add_checkbutton(label=choice, variable=self.choices2[choice],
                                      onvalue=1, offvalue=0,
                                      command=self.printValues)


        self.label_menu = Label(self,
                                 text="Enter max runtime seconds")
        self.label_menu.grid(row=3, column=0, padx=20, pady=20)

        self.maxruntimesecs = Entry(self)

        self.maxruntimesecs.grid(row=3, column=1, padx=20, pady=20)
        self.pack(padx=20, pady=20)
        self.submit_button = Button(self,
                                         text="Submit",
                                         command=self.submit)
        self.submit_button.grid(row=4, column=1, padx=30, pady=30)
    def get_list(self,choices):
        return [name for name,var in choices.items() if var.get() > 0]
    def submit(self):
        self.pipeline.set_categorical_variables_to_inpute(self.get_list(self.choices))
        self.pipeline.set_numerical_variables_to_inpute(self.get_list((self.choices2)))
        self.pipeline.set_max_runtime_secs(self.maxruntimesecs.get())


        self.next(self.pipeline)






