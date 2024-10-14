import logging
import numpy as np
import os
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
from scipy.ndimage import median_filter

from __code.parent import Parent
from __code import Run, DataType
from __code.workflow.load import Load
from __code.workflow.export import Export
from __code.utilities.files import make_or_reset_folder
from __code.utilities.logging import logging_3d_array_infos


class Normalization(Parent):

    obs_combined = None
    mean_ob_proton_charge = None

    def run(self):
        self.combine_obs()
        self.normalize_runs()

    def combine_obs(self):
        
        logging.info(f"Combine obs:")
        list_obs = self.parent.master_3d_data_array_cleaned[DataType.ob]
        if len(list_obs) == 1:
            self.obs_combined = np.array(list_obs[0])
            logging.info(f"\tonly 1 ob, nothing to combine!")
        else:
            self.obs_combined = np.mean(list_obs, axis=0)
            logging.info(f"\tcombining {len(list_obs)} obs.")
        
        temp_obs_combined = median_filter(self.obs_combined, size=2)
        index_of_zero = np.where(self.obs_combined == 0)
        self.obs_combined[index_of_zero] = temp_obs_combined[index_of_zero]

        logging_3d_array_infos(message="obs", array=self.obs_combined)

        list_proton_charge = []
        for _run in self.parent.list_of_runs_to_use[DataType.ob]:
            list_proton_charge.append(self.parent.list_of_runs[DataType.ob][_run][Run.proton_charge_c])

        self.mean_ob_proton_charge = np.mean(list_proton_charge)
        logging.info(f"\tcalculated combined ob proton charge: {self.mean_ob_proton_charge}")
    
    def normalize_runs(self):
        master_3d_data = self.parent.master_3d_data_array_cleaned
        list_of_runs_used = self.parent.list_of_runs_to_use
        normalized_data = []

        list_proton_charge = {DataType.sample: [],
                              DataType.ob: [],
                             }

        logging.info(f"Normalization:")
        logging_3d_array_infos(array=self.mean_ob_proton_charge, message="mean_ob_proton_charge")

        for _index, _run in enumerate(list_of_runs_used[DataType.sample]):
            sample_proton_charge = self.parent.list_of_runs[DataType.sample][_run][Run.proton_charge_c]
            angle = self.parent.list_of_runs[DataType.sample][_run][Run.angle]
            list_proton_charge[DataType.sample].append(sample_proton_charge)
            logging.info(f"\t{_run} has a proton charge of {sample_proton_charge} and angle of {angle}")
            
            norm_coeff = self.mean_ob_proton_charge / sample_proton_charge
            sample_data = np.array(master_3d_data[DataType.sample][_index])
            logging_3d_array_infos(message="sample_data", array=sample_data)

            normalized_sample = np.divide(sample_data, self.obs_combined) * norm_coeff
            logging_3d_array_infos(message="after normalization", array=normalized_sample)
            normalized_data.append(normalized_sample) 
            logging.info(f"\tnormalization of {_run} is done!")

        self.parent.normalized_images = normalized_data

    def visualize_normalization(self):
        
        normalized_data = self.parent.normalized_images
        list_of_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
        master_3d_sample_data = self.parent.master_3d_data_array_cleaned[DataType.sample]

        def plot_norm(image_index=0, vmin=0, vmax=1):

            fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

            _norm_data = normalized_data[image_index]
            _run_number = list_of_runs_to_use[image_index]
            _raw_data = master_3d_sample_data[image_index]

            im0 = axs[0].imshow(_raw_data)
            axs[0].set_title("Raw data")
            plt.colorbar(im0, ax=axs[0], shrink=0.5)

            im1 = axs[1].imshow(_norm_data, vmin=vmin, vmax=vmax)
            axs[1].set_title('Normalized')
            plt.colorbar(im1, ax=axs[1], shrink=0.5)
    
            # fig.set_title(f"{_run_number}")
            
            plt.tight_layout()
            plt.show()

        display_plot = interactive(plot_norm,
                                  image_index=widgets.IntSlider(min=0,
                                                                max=len(list_of_runs_to_use)-1,
                                                                value=0),
                                  vmin=widgets.IntSlider(min=0, max=10, value=0),
                                  vmax=widgets.IntSlider(min=0, max=10, value=1))
        display(display_plot)
    
    def export_images(self):
        
        logging.info(f"Exporting the normalized images")
        logging.info(f"\tfolder selected: {self.parent.working_dir[DataType.normalized]}")

        normalized_data = self.parent.normalized_images

        master_base_folder_name = f"{os.path.basename(self.parent.working_dir[DataType.sample])}_normalized"
        full_output_folder = os.path.join(self.parent.working_dir[DataType.normalized],
                                          master_base_folder_name)

        make_or_reset_folder(full_output_folder)

        o_export = Export(image_3d=normalized_data,
                          output_folder=full_output_folder)
        o_export.run()
        logging.info(f"\texporting normalized images ... Done!")
