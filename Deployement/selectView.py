from tkinter.ttk import Label, Entry, Button, Frame
from tkinter import filedialog, StringVar, DISABLED, NORMAL, messagebox

import pandas as pd



class DirectorySelectFrame(Frame):
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
        self.text1 = Label(self, text="Please Select the file you want to Apply Factor Analysis on.")
        self.text1.grid(column=0,row=0)

        self.csvFileToParseLabel.grid(column=0, row=2, sticky='w')

        self.csvFileNameEntry.grid(column=1, row=2, ipadx=50, padx=20)

        self.browseButtonForcsv.grid(column=2, row=2, ipadx=20, pady=10, sticky='w')


        # start button
        self.startParsingButton.grid(column=2, row=4, sticky='s', ipadx=20, pady=50)
        self.text2 = Label(self, text="NB:Data should be preprocessed!                                           ")
        self.text2.grid(column=0,row=5)
        self.pack(padx=50, pady=50)

    def _csv_file_browse(self):
        fileName = filedialog.askopenfilename(title="Selecte a file",
                                              filetypes=[("Excel files", ".xlsx .xls")])
        self.csv_file_path.set(fileName)
        self._enable_start_button()


    def _enable_start_button(self):
        if len(self.csv_file_path.get()) > 0 :
            self.startParsingButton['state'] = NORMAL

    def _parse_data(self):
        # open the csv file
        self.csv_data = pd.read_excel(self.csv_file_path.get()
                                    )
        if len(self.csv_data.columns) > 50:
            messagebox.showerror("Error", "we don't support files with more then 49 columns")
            return
        # df = self.csv_data.select_dtypes(include=np.number)

        # pd.plotting.scatter_matrix(df, marker='.', hist_kwds={'bins': 10}, s=60, alpha=0.8)

        # plt.show()

        self.next_callback(self.csv_data)
