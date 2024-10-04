import logging
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets

from __code.parent import Parent
from __code import Run, DataType


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
            self.obs_combined = list_obs.copy()
            logging.info(f"\tonly 1 ob, nothing to combine!")
        else:
            self.obs_combined = np.mean(list_obs, axis=0)
            logging.info(f"\tcombining {len(list_obs)} obs.")

        list_proton_charge = []
        for _run in self.parent.list_of_runs_used[DataType.ob]:
            list_proton_charge.append(self.parent.list_of_runs[DataType.ob][_run][Run.proton_charge_c])
        self.mean_ob_proton_charge = np.mean(list_proton_charge)
        logging.info(f"\tcalculated combined ob proton charge: {self.mean_ob_proton_charge}")
    
    def normalize_runs(self):
        master_3d_data = self.parent.master_3d_data_array_cleaned
        list_of_runs_used = self.parent.list_of_runs_used
        normalized_data = []


        list_proton_charge = {DataType.sample: [],
                              DataType.ob: [],
                             }

        logging.info(f"Normalization:")

        for _index, _run in enumerate(list_of_runs_used[DataType.sample]):
            sample_proton_charge = self.parent.list_of_runs[DataType.sample][_run][Run.proton_charge_c]
            list_proton_charge[DataType.sample].append(sample_proton_charge)
            logging.info(f"\t{_run} has a proton charge of {sample_proton_charge}")

            norm_coeff = self.mean_ob_proton_charge / sample_proton_charge
            sample_data = master_3d_data[DataType.sample][_index]

            normalized_sample = np.divide(sample_data, self.obs_combined) * norm_coeff
            normalized_data.append(normalized_sample) 
            logging.info(f"\tnormalization of {_run} is done!")

        self.parent.normalized_data = normalized_data

    def visualize_normalization(self):
        
        normalized_data = self.parent.normalized_data
        list_of_runs_to_use = self.parent.list_of_runs_used[DataType.sample]
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
