import logging
import os
from tqdm import tqdm
import numpy as np

from __code.parent import Parent
from __code import DataType
from __code.utilities.load import load_data_using_multithreading
from __code.utilities.files import retrieve_list_of_tif


class Combine(Parent):
    
    final_list_of_runs = {DataType.sample: [],
                          DataType.ob: [],
    }

    def run(self):
        self.removing_rejected_runs()
        # self.combining_runs()

    def removing_rejected_runs(self):
        logging.info(f"removing rejected runs:")
        list_of_sample_runs_to_reject = self.parent.list_of_sample_runs_to_reject_ui.value
        list_of_ob_runs_to_reject = self.parent.list_of_ob_runs_to_reject_ui.value
        logging.info(f"\tlist of sample runs to reject: {list_of_sample_runs_to_reject}")
        logging.info(f"\tlist of ob runs to reject: {list_of_ob_runs_to_reject}")

        list_of_runs = self.parent.list_of_runs
        
        for _run in list_of_runs[DataType.sample]:
            logging.info(f"\t\tcheckint {_run =}")
            if _run in list_of_sample_runs_to_reject:
                logging.info(f"\t\t\t yes, in the list of files to reject!")
                continue
            else:
                logging.info(f"\t\t\t not in the list of files to reject, let's keep it!")
                self.final_list_of_runs[DataType.sample].append(_run)

        for _run in list_of_runs[DataType.ob]:
            if _run in list_of_ob_runs_to_reject:
                continue
            else:
                self.final_list_of_runs[DataType.ob].append(_run)

        self.parent.list_of_runs = self.final_list_of_runs

    def combining_runs(self):
        logging.info(f"combining runs:")

        list_sample_runs = self.parent.list_of_runs[DataType.sample]
        logging.info(f"\t{list_sample_runs = }")
        sample_folder = self.parent.working_dir[DataType.sample]
        logging.info(f"\t{sample_folder = }")

        list_ob_runs = self.parent.list_of_runs[DataType.ob]
        logging.info(f"\t{list_ob_runs = }")
        ob_folder = self.parent.working_dir[DataType.ob]
        logging.info(f"\t{ob_folder = }")

        full_path_sample_runs = [os.path.join(sample_folder, _run) for _run in list_sample_runs]
        full_path_ob_runs = [os.path.join(ob_folder, _run) for _run in list_ob_runs]

        logging.info(f"\tworking with obs:")
        _master_data = []
        for _full_path_run in tqdm(full_path_ob_runs):
            logging.info(f"\t\tloading {os.path.basename(_full_path_run)} ...")
            list_tif = retrieve_list_of_tif(_full_path_run)
            _master_data.append(load_data_using_multithreading(list_tif))
            logging.info(f"\t\t loading done!")
        self.parent.master_3d_data_array[DataType.ob] = _master_data

        logging.info(f"\tworking with sample:")
        _master_data = []
        for _full_path_run in tqdm(full_path_sample_runs):
            logging.info(f"\t\tloading {os.path.basename(_full_path_run)} ...")
            list_tif = retrieve_list_of_tif(_full_path_run)
            _master_data.append(load_data_using_multithreading(list_tif))
            logging.info(f"\t\t loading done!")
        self.parent.master_3d_data_array[DataType.sample] = _master_data
