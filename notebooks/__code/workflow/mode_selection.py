import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML
from ipywidgets import interactive
import logging

from __code.parent import Parent
from __code import OperatingMode

from __code.workflow.checking_data import CheckingData
from __code.workflow.combine import Combine


class ModeSelection(Parent):

    def select(self):   
        self.mode_selection_ui = widgets.ToggleButtons(options=[OperatingMode.white_beam, 
                                                                OperatingMode.tof],
                                           value=OperatingMode.tof)
        display(self.mode_selection_ui)
    
    def load(self):
        
        logging.info(f"Working in {self.mode_selection_ui.value} mode")
        if self.mode_selection_ui.value == OperatingMode.white_beam:
            o_check = CheckingData(parent=self.parent)
            o_check.checking_minimum_requirements()
            if self.minimum_requirements_met:
                o_combine = Combine(parent=self.parent)
                o_combine.run()
            else:
                o_check.minimum_requirement_not_met()
        
        else:
            pass
            # load the data keep full 3D array

            # retrieve time spectra of first file

            # retrieve detector offset and distance source_detector (json created by autoreduction?)

            # display profile and sample (integrated) with region moving

            # 