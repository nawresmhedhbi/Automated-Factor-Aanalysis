# import tkinter elements
import tkinter as tk

# import directory select frame
from selectView import DirectorySelectFrame
from home_view import HomeViewFrame
from EFA import EFA_Frame
from AutoMLSelectview import AutoMLSelectFrame
from ApplyAutoML import ApplyAML
from AutoMLMain import AutoMLmain
#from frames.general_stats_frame import GeneralStatsFrame


# Main window
class MainWindowView(tk.Tk):
    # constructor
    def __init__(self):
        super().__init__()

        # set title
        self.title('Deployment')

        self.current_frame_active = False

    def _diplay_first_frame(self):
        self.current_frame = DirectorySelectFrame(self, self._go_to_home_View)
        self.current_frame.start()

    def _diplay_frame(self, frame):
        self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.start()

    def main(self):
        self._diplay_first_frame()
        self.mainloop()

    def _go_to_home_View(self, csv_data):
        self.csv_data = csv_data
        self.home_view = HomeViewFrame(self, csv_data,self._go_to_efa_view)
        self._diplay_frame(self.home_view)
    def _go_to_efa_view(self,pipeline):
        self.pipeline = pipeline
        self.efa_view = EFA_Frame(self,pipeline,self.csv_data,self._go_to_efa_AUTOMLview)
        self._diplay_frame(self.efa_view)



    def _go_to_efa_AUTOMLview(self):

        self.automl_view = AutoMLSelectFrame(self,self.gotoautomlmail)
        self._diplay_frame(self.automl_view)
    def gotoautomlmail(self,h2odata):
        self.h2odata = h2odata
        self.automl_main = AutoMLmain(self ,self.csv_data, self._gotoapplyautoml, self.pipeline)
        self._diplay_frame(self.automl_main)

    def _gotoapplyautoml(self,pipeline):
        self.pipeline = pipeline
        self.apply_view = ApplyAML(self,self.pipeline,self.h2odata)
        self._diplay_frame(self.apply_view)






