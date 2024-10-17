import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML
from ipywidgets import interactive
import logging

from __code.parent import Parent
from __code import OperatingMode

from __code.workflow.checking_data import CheckingData
from __code.workflow.remove_rejected_runs import RemoveRejectedRuns
from __code.workflow.sort_runs import SortRuns
from __code.workflow.load import Load


class ModeSelection(Parent):

    def select(self):   
        self.mode_selection_ui = widgets.ToggleButtons(options=[OperatingMode.white_beam, 
                                                                OperatingMode.tof],
                                           value=OperatingMode.tof)
        display(self.mode_selection_ui)
    
    def load(self):
        
        logging.info(f"Working in {self.mode_selection_ui.value} mode")
        o_check = CheckingData(parent=self.parent)
        o_check.checking_minimum_requirements()
        if self.parent.minimum_requirements_met:

            o_rejected = RemoveRejectedRuns(parent=self.parent)
            o_rejected.run()

            o_sort = SortRuns(parent=self.parent)
            o_sort.run()

            combine_mode = (self.mode_selection_ui.value == OperatingMode.white_beam)
            o_combine = Load(parent=self.parent)
            o_combine.load_data(combine=combine_mode)

            if not combine_mode:
                pass
                # load the data keep full 3D array

                # retrieve time spectra of first file

                # retrieve detector offset and distance source_detector (json created by autoreduction?)

                # display profile and sample (integrated) with region moving

                # 

        else:
            o_check.minimum_requirement_not_met()