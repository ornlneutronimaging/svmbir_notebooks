import os
import logging
import glob
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
import numpy as np
from matplotlib.patches import Rectangle
from IPython.core.display import HTML

from __code import DEBUG, debug_folder, OperatingMode, DataType
from __code.utilities.configuration_file import Configuration, select_file, loading_config_file_into_model
from __code.utilities.logging import setup_logging
from __code.utilities.files import retrieve_list_of_tif
from __code.utilities.load import load_data_using_multithreading
from __code.utilities.time import get_current_time_in_special_file_name_format
from __code.utilities.json import save_json


class Step2SvmbirReconstructionInWhiteBeamMode:

    def __init__(self, system=None):

        # self.configuration = Configuration()
        self.working_dir = system.System.get_working_dir()
        if DEBUG:
            self.working_dir = debug_folder[OperatingMode.white_beam][DataType.extra]

        self.instrument = system.System.get_instrument_selected()

        setup_logging(basename_of_log_file=os.path.basename(__file__).replace('.py', ''))      
        logging.info(f"working_dir: {self.working_dir}")
        logging.info(f"instrument: {self.instrument}")
        if DEBUG:
            logging.info(f"WARNING!!!! we are running using DEBUG mode!")

    def select_config_file(self):
        select_file(top_folder=self.working_dir,
                    next_function=self.load_config_file)

    def load_config_file(self, config_file_path):
        logging.info(f"configuration file loaded: {config_file_path}")
        self.configuration = loading_config_file_into_model(config_file_path)
        self.images_path = self.configuration.projections_pre_processing_folder

    def load_images(self):
        logging.info(f"images_path: {self.images_path}")
        list_tiff = retrieve_list_of_tif(self.images_path)
        logging.info(f"list_tiff: {list_tiff}")
        self.data = load_data_using_multithreading(list_tiff)
        self.data = np.moveaxis(self.data, 1, 2)
        logging.info(f"loading images done!")
        logging.info(f"self.data.shape: {self.data.shape}")

    def select_range_of_slices(self):
        
        _, width = np.shape(self.data[0])

        def plot_images(image_index, top_slice, bottom_slice, nbr_of_ranges):
            fig, ax = plt.subplots()
            ax.imshow(self.data[image_index], cmap='jet')
            
            range_size = int((np.abs(top_slice - bottom_slice)) / nbr_of_ranges)

            for _range_index in np.arange(nbr_of_ranges):
                _top_slice = top_slice + _range_index * range_size

                ax.add_patch(Rectangle((0, _top_slice), width, range_size,
                                    edgecolor='yellow',
                                    facecolor='green',
                                    fill=True,
                                    lw=2,
                                    alpha=0.3,
                                    ),
                )     

            ax.axhline(top_slice, color='red')
            ax.axhline(nbr_of_ranges * range_size, color='red')
                  
            plt.show()

            return top_slice, bottom_slice, nbr_of_ranges

        self.display_plot_images = interactive(plot_images,
                                          image_index=widgets.IntSlider(min=0, max=self.data.shape[0]-1, step=1, value=0),
                                          top_slice=widgets.IntSlider(min=0, max=self.data.shape[1]-1, step=1, value=0),
                                          bottom_slice=widgets.IntSlider(min=0, max=self.data.shape[1]-1, step=1, value=self.data.shape[1]-1),
                                          nbr_of_ranges=widgets.IntSlider(min=1, max=10, step=1, value=1))
        display(self.display_plot_images)

    def export_config_file(self):
        top_slice, bottom_slice, nbr_of_ranges = self.display_plot_images.result
        logging.info(f"Exporting config file:")
        logging.info(f"\ttop_slice: {top_slice}")
        logging.info(f"\tbottom_slice: {bottom_slice}")
        logging.info(f"\tnbr_of_ranges: {nbr_of_ranges}")

        range_size = int((np.abs(top_slice - bottom_slice)) / nbr_of_ranges)

        list_slices = []
        for _range_index in np.arange(nbr_of_ranges):
            _top_slice = top_slice + _range_index * range_size
            _bottom_slice = _top_slice + range_size
            list_slices.append((_top_slice, _bottom_slice))
            self.configuration.list_of_slices_to_reconstruct = list_slices
            
        working_dir = self.working_dir
        current_time = get_current_time_in_special_file_name_format()
        config_file_name = f"step2_svmbir_reconstruction_in_white_beam_mode_config_{current_time}.json"
        full_config_file_name = os.path.join(working_dir, config_file_name)
        config_json = self.configuration.model_dump_json()
        save_json(full_config_file_name, json_dictionary=config_json)
        logging.info(f"config file saved: {full_config_file_name}")

        display(HTML("Move to the next step by running the command <font color='blue'>python step3_svmbir_reconstruction_in_white_beam_mode.py</font> " +
                     f"<font color='blue'>{full_config_file_name}</font>"))
