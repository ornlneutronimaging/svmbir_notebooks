import logging
import numpy as np

from __code.parent import Parent
from __code import Run, DataType


class Normalization(Parent):

    obs_combined = None
    mean_ob_proton_charge = None

    def run(self):
        self.combine_obs()
        self.normalize_runs()

    def combine_obs(self):
        
        list_obs = self.parent.master_3d_data_array_cleaned[DataType.ob]
        print(f"{np.shape(list_obs) =}")
        if len(list_obs) == 1:
            self.obs_combined = list_obs.copy()
        else:
            self.obs_combined = np.mean(list_obs, axis=0)
        print(f"{np.shape(self.obs_combined) =}")

        list_proton_charge = []
        for _run in self.parent.list_of_runs_used[DataType.ob]:
            list_proton_charge.append(self.parent.list_of_runs[DataType.ob][_run][Run.proton_charge_c])
        self.mean_ob_proton_charge = np.mean(list_proton_charge)
    
    def normalize_runs(self):
        master_3d_data = self.parent.master_3d_data_array_cleaned
        list_of_runs_used = self.parent.list_of_runs_used
        normalized_data = []


        list_proton_charge = {DataType.sample: [],
                              DataType.ob: [],
                             }

        logging.info(f"Normalization:")
        for _data_type in list_of_runs_used.keys():

            logging.info(f"\t{_data_type}:")
            for _index, _run in enumerate(list_of_runs_used[_data_type]):
                sample_proton_charge = self.parent.list_of_runs[_data_type][_run][Run.proton_charge_c]
                list_proton_charge[_data_type].append(_proton_charge)
                logging.info(f"\t\t{_run} has a proton charge of {_proton_charge}")

                norm_coeff = self.mean_ob_proton_charge / sample_proton_charge
                sample_data = master_3d_data[_index]

                normalized_sample = np.divide(sample_data, self.obs_combined) * norm_coeff
                normalized_data.append(normalized_sample) 

        self.parent.normalized_data = normalized_data

    def visualize_normalization(self):
        pass
    