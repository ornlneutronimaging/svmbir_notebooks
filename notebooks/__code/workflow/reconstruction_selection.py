import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML
from ipywidgets import interactive
import logging
import numpy as np

from __code.parent import Parent
from __code import DEFAULT_RECONSTRUCTION_ALGORITHM
from __code.utilities.configuration_file import ReconstructionAlgorithm


class ReconstructionSelection(Parent):

    def select(self):   
        self.reconstruction_selection_ui = widgets.ToggleButtons(options=[ReconstructionAlgorithm.fbp, 
                                                                          ReconstructionAlgorithm.svmbir],
                                           value=DEFAULT_RECONSTRUCTION_ALGORITHM)
        display(self.reconstruction_selection_ui)

        self.reconstruction_selection_ui.observe(self.on_change, names='value')

    def on_change(self, change):
        selected_reconstruction_algorithm = change['new']
        self.parent.configuration.reconstruction_algorithm = selected_reconstruction_algorithm
        logging.info(f"selected reconstruction algorithm: {selected_reconstruction_algorithm}")
        