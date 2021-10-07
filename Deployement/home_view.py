from tkinter.ttk import Label, Button, Frame

from tkinter import StringVar, Menu, IntVar, Menubutton , OptionMenu



import pandas as pd
from sklearn.pipeline import Pipeline
from preprocessors import Pipeline



class HomeViewFrame(Frame):
    def __init__(self, master, data,next):
        super().__init__(master)

        self.data = data
        self.next = next







    def printValues(self):
        for name, var in self.choices.items():
            print("%s: %s" % (name, var.get()))

    def start(self):
        self.conf = Label(self,text="Some configurations before starting Factor Analysis            ",font = ("bold",11))
        self.conf.grid(row=0, column=0)
        self.label_menu = Label(self,
                                text="Select variables to perfrom Factor Analysis On                                       ")
        self.label_menu.grid(row=1, column=0, padx=20, pady=20)

        self.menubutton = Menubutton(self, text="Variables",
                                   indicatoron=True, borderwidth=1, relief="raised")
        self.menu = Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.menu)
        self.menubutton.grid(row=1, column=1, padx=20, pady=20)
        self.choices = {}

        for choice in self.data.columns.tolist():

            self.choices[choice] = IntVar(value=0)
            self.menu.add_checkbutton(label=choice, variable=self.choices[choice],
                             onvalue=1, offvalue=0,
                             command=self.printValues)
        self.pack(padx=20, pady=20)

        self.label_menu_target = Label(self,
                                text="Select Target variable                                                                               ")
        self.label_menu_target.grid(row=2, column=0, padx=20, pady=20)

        self.selected_target = StringVar(self)
        # Set the default value of the variable
        self.selected_target.set("Target")
        self.target_menu = OptionMenu(self, self.selected_target,self.data.columns.tolist()[0],*self.data.columns.tolist())
        self.target_menu.grid(row=2, column=1, padx=20, pady=20)

        self.label_menu_rotation = Label(self,
                                       text="Select rotation type to be performed in Factor Analysis                 ")
        self.label_menu_rotation.grid(row=3, column=0, padx=20, pady=20)

        self.selected_rotation = StringVar(self)
        self.selected_rotation.set("Rotation")
        self.rotation_menu = OptionMenu(self, self.selected_rotation, "varimax",
                                      *["promax",  "oblimin", "oblimax", "quartimin",  "quartimax", "equamax" ])
        self.rotation_menu.grid(row=3, column=1, padx=20, pady=20)

        self.submit_button = Button(self,
                                         text="Submit",
                                         command=self.submit)
        self.submit_button.grid(row=4, column=1, padx=20, pady=20)
        self.warning = Label(self,
                                text="NB: Don not include correlated variables in the selection process!                 ")
        self.warning.grid(row=5, column=0, padx=20, pady=20)

    def get_list(self):
        return [name for name,var in self.choices.items() if var.get() > 0]
    def submit(self):
        #print(self.get_list())
        self.pipeline = Pipeline(
            target=self.selected_target.get(), features=self.get_list(), rotation=self.selected_rotation.get(),
            categorical_variables_to_inpute=[]
            , numerical_variables_to_inpute=[],
            max_runtime_secs= None
        )
        self.next(self.pipeline)






