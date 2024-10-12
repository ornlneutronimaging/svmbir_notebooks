import numpy as np
from IPython.display import display
import ipywidgets as widgets
from IPython.core.display import HTML
import matplotlib.pyplot as plt
from ipywidgets import interactive
import logging

import svmbir

from __code.parent import Parent
from __code.config import NUM_THREADS


class SvmbirHandler(Parent):

    def set_settings(self):

        corrected_array = self.parent.corrected_images
        nbr_images = len(corrected_array)
        height, _ = np.shape(corrected_array[0])        

        display(widgets.HTML("<font size=5>Select range of slices to reconstruct</font"))

        def plot_range(image_index, top_slice, bottom_slice):

            fig, axs = plt.subplots(nrows=1, ncols=1)
            axs.imshow(corrected_array[image_index], vmin=0, vmax=1)
            axs.axhspan(top_slice, bottom_slice, color='blue', alpha=0.3)
            axs.axhline(top_slice, color='red', linestyle='--')
            axs.axhline(bottom_slice, color='red', linestyle='--')

            plt.tight_layout()
            plt.show()

            return top_slice, bottom_slice

        self.display_corrected_range = interactive(plot_range,
                                                    image_index = widgets.IntSlider(min=0,
                                                                                    max=nbr_images-1,
                                                                                    value=0),
                                                   top_slice = widgets.IntSlider(min=0,
                                                                                 max=height-1,
                                                                                 value=0),
                                                    bottom_slice = widgets.IntSlider(min=0,
                                                                                     max=height-1,
                                                                                     value=height-1),
                                                    )
        display(self.display_corrected_range)

        display(widgets.HTML("<hr>"))

        display(widgets.HTML("<font size=5>Define reconstruction settings</font"))

        self.sharpness_ui = widgets.FloatSlider(min=0,
                                           max=1,
                                           value=0,
                                           description="sharpness")
        self.snr_db_ui = widgets.FloatSlider(min=0,
                                        max=100,
                                        value=30.0,
                                        description="snr db")
        self.positivity_ui = widgets.Checkbox(value=True,
                                         description="positivity")
        self.max_iterations_ui = widgets.IntSlider(value=200,
                                              min=10,
                                              max=500,
                                              description="max itera.")
        self.verbose_ui = widgets.Checkbox(value=False,
                                      description='verbose')
        
        vertical_widgets = widgets.VBox([self.sharpness_ui,
                                         self.snr_db_ui,
                                         self.positivity_ui,
                                         self.max_iterations_ui,
                                         self.verbose_ui])
        display(vertical_widgets)

    def display_projections(self):

        corrected_array = self.parent.corrected_images
        nbr_images = len(corrected_array)
        height, _ = np.shape(corrected_array[0])        

        def display_sinograms(slice_index):

            fig, axs = plt.subplots(nrows=1, ncols=1)
            axs.imshow(corrected_array[:, slice_index, :])
            plt.tight_layout()
            plt.show()

        display_sinogram = interactive(display_sinograms,
                                       slice_index = widgets.IntSlider(min=0,
                                                                       max=height-1,
                                                                       value=0),
                                        )
        display(display_sinogram)


    def run_reconstruction(self):

        logging.info(f"Running reconstruction:")
        top_slice, bottom_slice = self.display_corrected_range.result
        sharpness = self.sharpness_ui.value
        snr_db = self.snr_db_ui.value
        positivity = self.positivity_ui.value
        max_iterations = self.max_iterations_ui.value
        verbose = 1 if self.verbose_ui.value else 0

        corrected_array = self.parent.corrected_images
        height, width = np.shape(corrected_array[0])      
        list_of_angles = np.array(self.parent.list_of_angles_to_use_sorted)

        logging.info(f"\t{top_slice = }")
        logging.info(f"\t{bottom_slice = }")
        logging.info(f"\t{sharpness = }")
        logging.info(f"\t{snr_db = }")
        logging.info(f"\t{positivity = }")
        logging.info(f"\t{max_iterations = }")
        logging.info(f"\t{verbose = }")
        logging.info(f"\t{list_of_angles = }")
        logging.info(f"\t{width = }")
        logging.info(f"\t{height = }")

        logging.info(f"\t launching reconstruction ...")

        self.parent.reconstruction_array = svmbir.recon(sino=corrected_array[:, top_slice: bottom_slice+1, :],
                                                        angles=list_of_angles,
                                                        num_rows = height,
                                                        num_cols = width,
                                                        center_offset = 0,
                                                        sharpness = sharpness,
                                                        snr_db = snr_db,
                                                        positivity = positivity,
                                                        max_iterations = max_iterations,
                                                        num_threads = NUM_THREADS,
                                                        verbose = verbose,
                                                        svmbir_lib_path = "/tmp/"
                                                        )
        logging.info(f"\t Done !")
