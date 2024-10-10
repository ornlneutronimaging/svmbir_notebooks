import numpy as np
from IPython.display import display
import ipywidgets as widgets
from enum import Enum


class ListAlgo:

    remove_stripe_fw = "remove_stripe_fw"
    remove_stripe_ti = "remove_stripe_ti"
    remove_stripe_sf = "remove_stripe_sf"
    remove_stripe_based_sorting = "remove_stripe_based_sorting"
    remove_stripe_based_filtering = "remove_stripe_based_filtering"
    remove_stripe_based_fitting = "remove_stripe_based_fitting"
    remove_large_stripe = "remove_large_stripe"
    remove_all_stripe = "remove_all_stripe"
    remove_stripe_based_interpolation = "remove_stripe_based_interpolation"


class RemoveStrips:

    sinogram = None

    list_algo = {ListAlgo.remove_stripe_fw: {'help': 'Remove horizontal stripes from sinogram using the Fourier-Wavelet (FW) based method',
                },
                 ListAlgo.remove_stripe_ti: {'help': "Remove horizontal stripes from sinogram using Titarenko's approach [B13]",
                 },
                 ListAlgo.remove_stripe_sf: {'help': "Normalize raw projection data using a smoothing filter approach.",
                 },
                 ListAlgo.remove_stripe_based_sorting: {'help': "Remove full and partial stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 3).",
                 },
                 ListAlgo.remove_stripe_based_filtering: {'help': "Remove stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 2).",
                 },
                 ListAlgo.remove_stripe_based_fitting: {'help': "Remove stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 1).",
                 },
                 ListAlgo.remove_large_stripe: {'help': "Remove unresponsive and fluctuating stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 6).",
                 },
                 ListAlgo.remove_all_stripe: {'help': "Remove all types of stripe artifacts from sinogram using Nghia Vo's approach [B24] (combination of algorithm 3,4,5, and 6).",
                 },
                 ListAlgo.remove_stripe_based_interpolation: {'help': "Remove most types of stripe artifacts from sinograms based on interpolation."
                 },
                }
    
    list_options = None
    list_options_widgets = None
    list_to_use_widgets = None
    
    def __init__(self, parent=None):
        self.parent = parent
        # self.calculate_sinogram()

    def calculate_sinogram(self, data_3d):
        self.sinogram = np.moveaxis(data_3d, 1, 0)

    def select_algorithms(self):
        
        display(widgets.HTML("<font size=4><b>Select the algorithms to use (CTRL + CLICK to select more than one)</b></font>"))

        self.list_options = list(self.list_algo.keys())
        self.list_options_widget = widgets.SelectMultiple(
            options = self.list_options,
            layout = widgets.Layout(height="200px")
        )
        left_text = widgets.HTML("<b>List of algorithms available</b>")
        left_widget = widgets.VBox([left_text, self.list_options_widget])
        
        button_add = widgets.Button(description=">>>")
        button_remove = widgets.Button(description="<<<")
        second_column = widgets.VBox([widgets.Label(""),
                                      button_add, button_remove])

        self.list_to_use_widget = widgets.SelectMultiple(options=[],
                                                    layout = widgets.Layout(height="200px"))      
        right_text = widgets.HTML("<b>List of algorithms to use</b>")
        right_widget = widgets.VBox([right_text, self.list_to_use_widget])

        all_widget = widgets.HBox([left_widget,
                                   second_column,
                                   right_widget])
        display(all_widget)

        button_add.on_click(self.button_add_clicked)
        button_remove.on_click(self.button_remove_clicked)

    def button_add_clicked(self, value):
        list_to_add = self.list_options_widget.value
        list_already_added = self.list_to_use_widget.options
        full_list = list_to_add + list_already_added
        list_to_show_on_the_right = []
        lsit_to_display_on_the_left = []
        for _option in self.list_options:
            if _option in full_list:
                list_to_show_on_the_right.append(_option)
            else:
                lsit_to_display_on_the_left.append(_option)
        self.list_to_use_widget.options = list_to_show_on_the_right
        self.list_options_widget.options = lsit_to_display_on_the_left

    def button_remove_clicked(self, value):
        print(f"{value =}")


    def run(self):
        self.perform_cleaning()
        self.display_cleaning()

    def perform_cleaning(self):
        pass

    def display_cleaning(self):
        pass
    