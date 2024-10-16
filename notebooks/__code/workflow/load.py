import copy
import os
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive
import ipywidgets as widgets
from IPython.display import display
import random
import logging

from imars3d.backend.dataio.data import load_data

from __code import DataType
from __code import DEBUG, debug_folder
from __code.parent import Parent
from __code.utilities.file_folder_browser import FileFolderBrowser


class Load(Parent):

    def select_folder(self, data_type=DataType.sample, multiple_flag=False):

        self.parent.current_data_type = data_type
        self.data_type = data_type
        if data_type in [DataType.reconstructed, DataType.extra]:
            working_dir = self.parent.working_dir[DataType.processed]
        else:
            working_dir = self.parent.working_dir[DataType.top]

        if DEBUG:
            self.data_selected(debug_folder[data_type])
            return

        if not os.path.exists(working_dir):
            working_dir = os.path.abspath(os.path.expanduser("~"))

        o_file_browser = FileFolderBrowser(working_dir=working_dir,
                                           next_function=self.data_selected)
        o_file_browser.select_input_folder(instruction=f"Select Top Folder of {data_type}",
                                           multiple_flag=multiple_flag)

    def data_selected(self, top_folder):
        logging.info(f"{self.parent.current_data_type} top folder selected: {top_folder}")
        self.parent.working_dir[self.data_type] = top_folder
        print(f"Top {self.data_type} folder selected: {top_folder}")
