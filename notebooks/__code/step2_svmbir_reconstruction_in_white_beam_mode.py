import os
import logging
import glob
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
import numpy as np
from matplotlib.patches import Rectangle
  
from __code import DEBUG, debug_folder, OperatingMode, DataType
from __code.utilities.configuration_file import Configuration, select_file, loading_config_file_into_model
from __code.utilities.logging import setup_logging
from __code.utilities.files import retrieve_list_of_tif
from __code.utilities.load import load_data_using_multithreading


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
        logging.info(f"loading images done!")
        logging.info(f"self.data.shape: {self.data.shape}")

    def select_range_of_slices(self):
        
        _, width = np.shape(self.data[0])

        def plot_images(image_index, top_slice, bottom_slice, number_of_ranges):
            fig, ax = plt.subplots()
            ax.imshow(self.data[image_index], cmap='jet')
            
            range_size = int((top_slice - bottom_slice) / number_of_ranges)

            for _range_index in np.arange(number_of_ranges):
                _top_slice = top_slice + _range_index * range_size

                ax.add_patch(Rectangle((0, _top_slice), width, range_size,
                                    edgecolor='yellow',
                                    # facecolor='green',
                                    fill=True,
                                    lw=2,
                                    alpha=0.3,
                                    ),
                )     

            ax.ahvline(top_slice, color='red')
            ax.ahvline(_top_slice + number_of_ranges * range_size, color='red')
                  
            plt.show()

        display_plot_images = interactive(plot_images,
                                          image_index=widgets.IntSlider(min=0, max=self.data.shape[0]-1, step=1, value=0),
                                          top_slice=widgets.IntSlider(min=0, max=self.data.shape[1]-1, step=1, value=0),
                                          bottom_slice=widgets.IntSlider(min=0, max=self.data.shape[1]-1, step=1, value=0),
                                          number_of_ranges=widgets.IntSlider(min=1, max=10, step=1, value=1))
        display(display_plot_images)
