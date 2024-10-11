import numpy as np
from IPython.display import display
import ipywidgets as widgets
from IPython.core.display import HTML
from IPython.display import Javascript
from enum import Enum
from tomopy.prep import stripe
import logging
from tqdm import tqdm
import matplotlib.pyplot as plt
from ipywidgets import interactive


class ListAlgo:

    remove_stripe_fw = "remove_stripe_fw"
    remove_stripe_ti = "remove_stripe_ti"
    remove_stripe_sf = "remove_stripe_sf"
    remove_stripe_based_sorting = "remove_stripe_based_sorting"
    remove_stripe_based_filtering = "remove_stripe_based_filtering"
    remove_stripe_based_fitting = "remove_stripe_based_fitting"
    remove_large_stripe = "remove_large_stripe"
    remove_all_stripe = "remove_all_stripe"
    remove_dead_stripe = "remove_dead_stripe"
    remove_stripe_based_interpolation = "remove_stripe_based_interpolation"


class RemoveStrips:

    sinogram = None

    default_list_algo_to_use = [ListAlgo.remove_all_stripe]

    list_algo = {ListAlgo.remove_stripe_fw: {'help': 'Remove horizontal stripes from sinogram using the Fourier-Wavelet (FW) based method',
                                             'function': stripe.remove_stripe_fw,
                                             'settings': widgets.VBox([
                                                            widgets.Text(value="None",
                                                                            description="level"),
                                                            widgets.Dropdown(options=['haar', 'db5', 'sym5'],
                                                                description="wname"
                                                            ),
                                                            widgets.FloatText(value=2,
                                                                            description="sigma"),
                                                            widgets.Checkbox(value=True,
                                                                            description='pad')
                                                        ]),
                },
                 ListAlgo.remove_stripe_ti: {'help': "Remove horizontal stripes from sinogram using Titarenko's approach [B13]",
                                             'function': stripe.remove_stripe_ti,
                                              'settings': widgets.VBox([
                                                                        widgets.IntText(value=0,
                                                                            description="nblock"),
                                                                        widgets.FloatText(value=1.5,
                                                                            description="alpha"),
                                                        ]),
                 },
                 ListAlgo.remove_stripe_sf: {'help': "Normalize raw projection data using a smoothing filter approach.",
                                             'function': stripe.remove_stripe_sf,
                                              'settings': widgets.VBox([
                                                                        widgets.IntText(value=5,
                                                                            description="size"),
                                                        ]),
                 },
                 ListAlgo.remove_stripe_based_sorting: {'help': "Remove full and partial stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 3).",
                                                        'function': stripe.remove_stripe_based_sorting,
                                                         'settings': widgets.VBox([
                                                                        widgets.Text(value="None",
                                                                            description="size"),
                                                                        widgets.Dropdown(options=['1','2'],
                                                                            value='1',
                                                                            description="dim"),
                                                        ]),
                 },
                 ListAlgo.remove_stripe_based_filtering: {'help': "Remove stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 2).",
                                                          'function': stripe.remove_stripe_based_filtering,
                                                           'settings': widgets.VBox([
                                                            widgets.FloatSlider(value=3,
                                                                                min=3,
                                                                                max=10,
                                                                            description="sigma"),
                                                            widgets.Text(value="None",
                                                                            description="size"),
                                                            widgets.Dropdown(options=['1','2'],
                                                                            value='1',
                                                                            description="dim")
                                                        ]),
                 },
                 ListAlgo.remove_stripe_based_fitting: {'help': "Remove stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 1).",
                                                        'function': stripe.remove_stripe_based_fitting,
                                                         'settings': widgets.VBox([
                                                            widgets.IntSlider(value=3,
                                                                                min=1,
                                                                                max=5,
                                                                            description="order"),
                                                            widgets.Text(value="5,20",
                                                                            description="sigma"),
                                                        ]),
                 },
                 ListAlgo.remove_large_stripe: {'help': "Remove unresponsive and fluctuating stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 6).",
                                                'function': stripe.remove_large_stripe,
                                                'settings': widgets.VBox([
                                                            widgets.FloatText(value=3,
                                                                            description="snr"),
                                                            widgets.IntText(value=51,
                                                                            description="size"),
                                                            widgets.FloatSlider(value=0.1,
                                                                                min=0,
                                                                                max=1,
                                                                            description="drop_ratio"),
                                                            widgets.Checkbox(value=True,
                                                                             description='norm')
                                                        ]),
                 },
                ListAlgo.remove_dead_stripe: {'help': "Remove unresponsive and fluctuating stripe artifacts from sinogram using Nghia Vo's approach [B24] (algorithm 6).",
                                              'function': stripe.remove_dead_stripe,
                                              'settings': widgets.VBox([
                                                            widgets.FloatText(value=3,
                                                                            description="snr"),
                                                            widgets.IntText(value=51,
                                                                            description="size"),
                                                            widgets.Checkbox(value=True,
                                                                             description='norm'),
                                                        ]),
                },
                ListAlgo.remove_all_stripe: {'help': "Remove all types of stripe artifacts from sinogram using Nghia Vo's approach [B24] (combination of algorithm 3,4,5, and 6).",
                                              'function': stripe.remove_all_stripe,
                                              'settings': widgets.VBox([
                                                            widgets.FloatText(value=3,
                                                                            description="snr"),
                                                            widgets.IntText(value=61,
                                                                            description="la_size"),
                                                            widgets.IntText(value=21,
                                                                            description="sm_size"),
                                                            widgets.Dropdown(options=['1','2'],
                                                                            value='1',
                                                                            description='dim')
                                                        ]),
                 },
                 ListAlgo.remove_stripe_based_interpolation: {'help': "Remove most types of stripe artifacts from sinograms based on interpolation.",
                                                              'function': stripe.remove_stripe_based_interpolation,
                                                                'settings': widgets.VBox([
                                                                widgets.FloatText(value=3,
                                                                                description="snr"),
                                                                widgets.IntText(value=31,
                                                                                description="size"),
                                                                widgets.FloatText(value=.1,
                                                                                description="drop_ratio"),
                                                                widgets.Checkbox(value=True,
                                                                                description='norm')
                                                            ]),
                 },
                }
    
    list_options = list(list_algo.keys())
    list_options_widgets = None
    list_to_use_widgets = None

    nothing_to_display = True
    
    def __init__(self, parent=None):
        self.parent = parent
        self.define_default_lists()

    def define_default_lists(self):
        full_list_options = self.list_options
        default_list_algo_to_use = self.default_list_algo_to_use

        left_list_algo = []
        right_list_algo = default_list_algo_to_use
        for _algo in full_list_options:
            if _algo in default_list_algo_to_use:
                pass
            else:
                left_list_algo.append(_algo)

        self.default_left_list_algo = left_list_algo
        self.default_right_list_algo = right_list_algo

    def calculate_sinogram(self, data_3d):
        return np.moveaxis(data_3d, 1, 0)

    def select_algorithms(self):
        
        display(widgets.HTML("<font size=4><b>Select the algorithms to use (CTRL + CLICK to select more than one)</b></font>"))

        self.list_options = list(self.list_algo.keys())
        self.list_options_widget = widgets.SelectMultiple(
            options = self.default_left_list_algo,
            layout = widgets.Layout(height="200px")
        )
        left_text = widgets.HTML("<b>List of algorithms available</b>")
        left_widget = widgets.VBox([left_text, self.list_options_widget])
        
        button_add = widgets.Button(description=">>>")
        button_remove = widgets.Button(description="<<<")
        second_column = widgets.VBox([widgets.Label(""),
                                      button_add, button_remove])

        self.list_to_use_widget = widgets.SelectMultiple(options=self.default_right_list_algo,
                                                    layout = widgets.Layout(height="200px"))      
        right_text = widgets.HTML("<b>List of algorithms to use</b>")
        right_widget = widgets.VBox([right_text, self.list_to_use_widget])

        all_widget = widgets.HBox([left_widget,
                                   second_column,
                                   right_widget])
        display(all_widget)
        
        help_button = widgets.Button(description='Algorithms documentation ...',
                                     button_style='info',
                                     layout=widgets.Layout(width='max-content'))
        display(help_button)

        button_add.on_click(self.button_add_clicked)
        button_remove.on_click(self.button_remove_clicked)
        help_button.on_click(self.help_button_clicked)

    def define_settings(self):
        list_options_to_use = self.list_to_use_widget.options

        _children = []
        for _option in list_options_to_use:
            _children.append(self.list_algo[_option]['settings'])

        accordion = widgets.Accordion(children=_children,
                                      titles=list_options_to_use)
        display(accordion)

    def button_add_clicked(self, value):
        list_to_add = self.list_options_widget.value
        list_already_added = self.list_to_use_widget.options
        full_list = list_to_add + list_already_added
        list_to_show_on_the_right = []
        list_to_display_on_the_left = []
        for _option in self.list_options:
            if _option in full_list:
                list_to_show_on_the_right.append(_option)
            else:
                list_to_display_on_the_left.append(_option)
        self.list_to_use_widget.options = list_to_show_on_the_right
        self.list_options_widget.options = list_to_display_on_the_left

    def button_remove_clicked(self, value):
        right_list_to_remove = self.list_to_use_widget.value
        right_list = self.list_to_use_widget.options

        new_list_to_use = []
        for _option in right_list:
            if _option in right_list_to_remove:
                pass
            else:
                new_list_to_use.append(_option)
        self.list_to_use_widget.options = new_list_to_use

        full_list_options = self.list_options
        new_left_list = []
        for _option in full_list_options:
            if _option in new_list_to_use:
                pass
            else:
                new_left_list.append(_option)
        self.list_options_widget.options = new_left_list

    def help_button_clicked(self, value):
        self.window_open("https://tomopy.readthedocs.io/en/latest/api/tomopy.prep.stripe.html")

    def run(self):
        self.perform_cleaning()
        self.display_cleaning()

    def get_keyword_arguments(self, algorithm_name=None):
        list_widgets = self.list_algo[algorithm_name]['settings'].children
        list_arguments = {}
        for _widget in list_widgets:
            _arg_name = _widget.description
            _arg_value = _widget.value
            list_arguments[_arg_name] = _arg_value
        return list_arguments

    def perform_cleaning(self):
        list_algo_to_use = self.list_to_use_widget.options
        logging.info(f"Strip cleaning:")
        if list_algo_to_use:
            tomography_array = self.parent.corrected_images
            list_algo_that_failed = []
            list_algo_that_worked = []
            try:
                for _algo in tqdm(list_algo_to_use):
                    logging.info(f"\t{_algo} ... running")
                    kwargs = self.get_keyword_arguments(algorithm_name=_algo)
                    logging.info(f"\t\t{kwargs =}")
                    tomography_array = RemoveStrips.run_algo(self.list_algo[_algo]['function'], 
                                                            tomography_array, 
                                                            **kwargs)
                    logging.info(f"\t{_algo} done!")
                    list_algo_that_worked.append(_algo)
            except np.linalg.LinAlgError:
                list_algo_that_failed.append(_algo)

            self.nothing_to_display = False
            self.parent.strip_corrected_images = tomography_array
        else:
            logging.info(f"\tskipped!")

        if list_algo_that_failed:
            display(HTML("<font color=red><b>List of algo that failed:</b></font>"))
            for _algo in list_algo_that_failed:
                display(HTML(f"<font color=red> * {_algo}</font>"))
        if list_algo_that_worked:
            display(HTML("<font color=green><b>List of algos that worked:</b></font>"))
            for _algo in list_algo_that_worked:
                display(HTML(f"<font color=green> * {_algo}</font>"))

    def run_algo(name_of_algo, array, **kwargs):
        return name_of_algo(array, **kwargs)

    def display_cleaning(self):
        if self.nothing_to_display:
            return

        strip_corrected_images = self.parent.strip_corrected_images
        sinogram_before = self.calculate_sinogram(strip_corrected_images)

        corrected_images = self.parent.corrected_images
        sinogram_after = self.calculate_sinogram(corrected_images)

        nbr_projections, height, _ = np.shape(corrected_images)

        def plot_result(image_index, slice_index):

            fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))

            axs[0][0].imshow(corrected_images[image_index], vmin=0, vmax=1)
            axs[0][0].set_title("Before correction")
            axs[0][0].axhline(slice_index, color='red', linestyle='--')

            axs[0][1].imshow(strip_corrected_images[image_index], vmin=0, vmax=1)
            axs[0][1].set_title("After correction")
            axs[0][1].axhline(slice_index, color='red', linestyle='--')

            axs[1][0].imshow(sinogram_before[slice_index], vmin=0, vmax=1)
            axs[1][1].imshow(sinogram_after[slice_index], vmin=0, vmax=1)

            plt.tight_layout()
            plt.show()

        display_plot = interactive(plot_result,
                                   image_index=widgets.IntSlider(min=0,
                                                                 max=nbr_projections-1),
                                    slice_index=widgets.IntSlider(min=0,
                                                                  max=height-1),
                                    )
        display(display_plot)
    
    def window_open(self, url):
        display(Javascript('window.open("{url}");'.format(url=url)))
