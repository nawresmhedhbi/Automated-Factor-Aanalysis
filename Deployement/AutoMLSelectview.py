from tkinter.ttk import Label, Entry, Button, Frame
from tkinter import filedialog, StringVar, DISABLED, NORMAL, messagebox

import pandas as pd
import h2o
from h2o.automl import H2OAutoML


class AutoMLSelectFrame(Frame):
    def __init__(self, master, next_callback):
        super().__init__(master)

        self.next_callback = next_callback

        self.img_directory_path = StringVar()
        self.csv_file_path = StringVar()

        self.csvFileToParseLabel = Label(self,
                                         text="Enter the path of the csv file to parse : ")
        self.csvFileNameEntry = Entry(self,
                                      textvariable=self.csv_file_path)
        self.browseButtonForcsv = Button(self,
                                         text="Browse a file",
                                         command=self._csv_file_browse)



        self.startParsingButton = Button(self,
                                         text="Start Parsing",
                                         command=self._parse_data,
                                         state=DISABLED)

    def start(self):
        self.csvFileToParseLabel.grid(column=0, row=0, sticky='w')

        self.csvFileNameEntry.grid(column=1, row=0, ipadx=50, padx=20)

        self.browseButtonForcsv.grid(column=2, row=0, ipadx=20, pady=10, sticky='w')


        # start button
        self.startParsingButton.grid(column=2, row=3, sticky='s', ipadx=20, pady=50)

        self.pack(padx=50, pady=50)

    def _csv_file_browse(self):
        fileName = filedialog.askopenfilename(title="Selecte a file",
                                              filetypes=[("CSV files", ".csv")])
        self.csv_file_path.set(fileName)
        self._enable_start_button()


    def _enable_start_button(self):
        if len(self.csv_file_path.get()) > 0 :
            self.startParsingButton['state'] = NORMAL

    def _parse_data(self):
        # open the csv file
        self.csv_data = h2o.import_file(self.csv_file_path.get()
                                    )


        self.next_callback(self.csv_data)