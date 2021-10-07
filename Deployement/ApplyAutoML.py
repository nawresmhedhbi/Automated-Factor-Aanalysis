from tkinter.ttk import Label, Entry, Button, Frame
from tkinter import filedialog, StringVar, DISABLED, NORMAL, messagebox
import tkinter as tk

import pandas as pd


class ApplyAML(Frame):
    def __init__(self, master, pipeline, data):
        super().__init__(master)

        self.pipeline = pipeline
        self.data = data

    def runtraining(self):
        self.display(self.pipeline.run_model())

    def performancetraining(self):

        self.display(self.pipeline.model_performance_train_data())

    def runprediction(self):
        self.pipeline.predict()
        self.display(self.pipeline.model_performance_prediction())
    def performanceprediction(self):
        self.display(self.pipeline.model_performance_prediction())

    def start(self):
        self.pipeline.fit(self.data, 'contract_suspect')
        # print(self.pipeline.check_validity())
        self.title = Label(self,text="    Prediction Using Factor Analysis Results           ",font = ("bold",13))
        self.title.pack()

        self.BuildModelButton = Button(self,
                                           text="Build Model By AutoML and Visualise Leaderboard",
                                           command=self.runtraining)
        self.BuildModelButton.pack(padx=50, pady=50)


        self.Exploration = Button(self,
                               text="Model Exploration",
                               command=self.performancetraining)
        self.Exploration.pack(padx=50, pady=50)


        self.Prediction = Button(self,
                               text="RUN prediction and Explore Model Performance",
                               command=self.runprediction)
        self.Prediction.pack(padx=50, pady=50)


        self.pack(padx=20, pady=20)

    def display(self, quote):
        #self.pipeline.check_validity()
        root = tk.Tk()
        S = tk.Scrollbar(root)
        T = tk.Text(root, height=60, width=100)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(tk.END, quote)

        tk.mainloop()
