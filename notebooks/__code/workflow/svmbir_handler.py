import numpy as np
import os
from IPython.display import display
import ipywidgets as widgets
from IPython.core.display import HTML
import matplotlib.pyplot as plt
from ipywidgets import interactive
import logging
import tomopy

import svmbir

from __code.workflow.export import Export
from __code.utilities.files import make_or_reset_folder
from __code.utilities.configuration_file import SvmbirConfig
from __code.parent import Parent
from __code import DataType, Run
from __code.config import NUM_THREADS, SVMBIR_LIB_PATH


class SvmbirHandler(Parent):

    def set_settings(self):

        corrected_array = self.parent.corrected_images
        nbr_images = len(corrected_array)
        height = self.parent.image_size['height']

        list_angles = self.parent.final_list_of_angles
        list_runs = self.parent.list_of_runs_to_use[DataType.sample]

        display(widgets.HTML("<font size=5>Select range of slices to reconstruct</font"))

        [default_top, default_bottom] = self.parent.configuration.range_of_slices_for_center_of_rotation

        def plot_range(image_index, top_slice, bottom_slice):

            fig, axs = plt.subplots(nrows=1, ncols=1)

            axs.set_title(f"{list_runs[image_index]}, angle: {list_angles[image_index]}")
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
                                                                                 value=default_top),
                                                    bottom_slice = widgets.IntSlider(min=0,
                                                                                     max=height-1,
                                                                                     value=default_bottom),
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

    def display_sinograms(self):

        corrected_array = self.parent.corrected_images
        height = self.parent.image_size['height']
        
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

    def _get_list_of_index_of_runs_to_exclude(self):
        """this return the index of the runs selected and that need to be rejected from final reconstruction"""
        try:
            list_options = self.parent.runs_to_exclude_ui.options
            list_value = self.parent.runs_to_exclude_ui.value
            list_index = []
            for _index, _option in enumerate(list_options):
                if _option in list_value:
                    list_index.append(_index)
            return list_index, list_value
        except AttributeError:
            return [], []

    def run_reconstruction(self):

        logging.info(f"Running reconstruction:")

        corrected_array = self.parent.corrected_images
        height = self.parent.image_size['height']
        width = self.parent.image_size['width']
        list_of_angles = np.array(self.parent.list_of_angles_to_use_sorted)
        list_of_angles_rad = np.array([np.deg2rad(float(_angle)) for _angle in list_of_angles])
        list_of_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
        list_of_sample_pc = self.parent.final_dict_of_pc[DataType.sample]
        list_of_sample_pc_to_use = list_of_sample_pc

        list_of_sample_frame_number = self.parent.final_dict_of_frame_number[DataType.sample]
        list_of_sample_frame_number_to_use = list_of_sample_frame_number
        
        # looking at list of runs to reject
        list_of_index_of_runs_to_exlude, list_runs_to_exclude = self._get_list_of_index_of_runs_to_exclude()
        if list_of_index_of_runs_to_exlude:
            logging.info(f"\tUser wants to reject the following runs: {list_runs_to_exclude}!")
            corrected_array = np.delete(corrected_array, list_of_index_of_runs_to_exlude, axis=0)
            list_of_angles_rad = np.delete(list_of_angles_rad, list_of_index_of_runs_to_exlude, axis=0)
            list_of_runs_to_use = np.delete(list_of_runs_to_use, list_of_index_of_runs_to_exlude)
            list_of_sample_pc_to_use = np.delete(list_of_sample_pc, list_of_index_of_runs_to_exlude)
            list_of_sample_frame_number_to_use = np.delete(list_of_sample_frame_number, list_of_index_of_runs_to_exlude)

            # updating configuration
            # self.parent.configuration.list_of_sample_index_to_reject = list_of_index_of_runs_to_exlude

        else:
            logging.info(f"\tNo runs rejected before final reconstruction!")

        # update configuration
        self.parent.configuration.list_of_sample_runs = list(list_of_runs_to_use)
        self.parent.configuration.list_of_angles = list(list_of_angles_rad)

        # save pc and frame number in configuration
        self.parent.configuration.list_of_sample_frame_number = list_of_sample_frame_number_to_use
        self.parent.configuration.list_of_sample_pc = list_of_sample_pc_to_use
        self.parent.configuration.list_of_ob_pc = self.parent.final_dict_of_pc[DataType.ob]
        self.parent.configuration.list_of_ob_frame_number = self.parent.final_dict_of_frame_number[DataType.ob]

        top_slice, bottom_slice = self.display_corrected_range.result
        sharpness = self.sharpness_ui.value
        snr_db = self.snr_db_ui.value
        positivity = self.positivity_ui.value
        max_iterations = self.max_iterations_ui.value
        verbose = 1 if self.verbose_ui.value else 0

        # update configuration
        svmbir_config = SvmbirConfig()
        svmbir_config.sharpness = sharpness
        svmbir_config.snr_db = snr_db
        svmbir_config.positivity = positivity
        svmbir_config.max_iterations = max_iterations
        svmbir_config.verbose = verbose
        svmbir_config.top_slice = top_slice
        svmbir_config.bottom_slice = bottom_slice
        self.parent.configuration.svmbir_config = svmbir_config

        logging.info(f"\t{top_slice = }")
        logging.info(f"\t{bottom_slice = }")
        logging.info(f"\t{sharpness = }")
        logging.info(f"\t{snr_db = }")
        logging.info(f"\t{positivity = }")
        logging.info(f"\t{max_iterations = }")
        logging.info(f"\t{verbose = }")
        logging.info(f"\t{list_of_angles_rad = }")
        logging.info(f"\t{width = }")
        logging.info(f"\t{height = }")
        logging.info(f"\t{type(corrected_array) = }")
        logging.info(f"\t{np.shape(corrected_array) = }")
        logging.info(f"\t launching reconstruction ...")

        corrected_array_log = tomopy.minus_log(corrected_array)

        where_nan = np.where(np.isnan(corrected_array_log))
        corrected_array_log[where_nan] = 0

        logging.info(f"\t{np.min(corrected_array_log) =}")
        logging.info(f"\t{np.max(corrected_array_log) =}")
        logging.info(f"\t{np.mean(corrected_array_log) =}")

        self.parent.reconstruction_array = svmbir.recon(sino=corrected_array_log[:, top_slice: bottom_slice+1, :],
                                                        angles=list_of_angles_rad,
                                                        num_rows = height,
                                                        num_cols = width,
                                                        center_offset = 0,
                                                        sharpness = sharpness,
                                                        snr_db = snr_db,
                                                        positivity = positivity,
                                                        max_iterations = max_iterations,
                                                        num_threads = NUM_THREADS,
                                                        verbose = verbose,
                                                        svmbir_lib_path = SVMBIR_LIB_PATH,
                                                        )
        logging.info(f"\t Done !")

    def display_slices(self):

        reconstruction_array = self.parent.reconstruction_array

        height = self.parent.image_size['height']
        
        def display_slices(slice_index):

            fig, axs = plt.subplots(nrows=1, ncols=1)
            im1 = axs.imshow(reconstruction_array[:, slice_index, :])
            plt.colorbar(im1, ax=axs, shrink=0.5)
            plt.tight_layout()
            plt.show()

        display_svmbir_slices = interactive(display_slices,
                                            slice_index = widgets.IntSlider(min=0,
                                                                            max=height-1,
                                                                            value=0),
                                                )
        display(display_svmbir_slices)

    def export_images(self):
        
        logging.info(f"Exporting the reconstructed slices")
        logging.info(f"\tfolder selected: {self.parent.working_dir[DataType.reconstructed]}")

        reconstructed_array = self.parent.reconstruction_array

        master_base_folder_name = f"{os.path.basename(self.parent.working_dir[DataType.sample])}_reconstructed"
        full_output_folder = os.path.join(self.parent.working_dir[DataType.reconstructed],
                                          master_base_folder_name)

        make_or_reset_folder(full_output_folder)

        o_export = Export(image_3d=reconstructed_array,
                          output_folder=full_output_folder)
        o_export.run()
        logging.info(f"\texporting reconstructed images ... Done!")

        # update configuration
        self.parent.configuration.output_folder = full_output_folder
