import logging
import os
from tqdm import tqdm
import numpy as np

from __code.parent import Parent
from __code import DataType, Run
from __code.utilities.load import load_data_using_multithreading
from __code.utilities.files import retrieve_list_of_tif


class Combine(Parent):
    
    list_of_runs_to_use = {DataType.sample: [],
                           DataType.ob: [],
    }

    def run(self):
        self.removing_rejected_runs()
        self.combining_runs()

    def removing_rejected_runs(self):
        logging.info(f"removing rejected runs:")
        list_of_sample_runs_to_reject = self.parent.list_of_sample_runs_to_reject_ui.value
        list_of_ob_runs_to_reject = self.parent.list_of_ob_runs_to_reject_ui.value
        logging.info(f"\tlist of sample runs to reject: {list_of_sample_runs_to_reject}")
        logging.info(f"\tlist of ob runs to reject: {list_of_ob_runs_to_reject}")

        for _run in self.parent.list_of_runs[DataType.sample].keys():
            if self.parent.list_of_runs[DataType.sample][_run][Run.use_it]:
                if _run in list_of_sample_runs_to_reject:
                    logging.info(f"\t\t rejecting sample run {_run}!")
                    self.parent.list_of_runs[DataType.sample][_run][Run.use_it] = False
                else:
                    self.parent.list_of_runs[DataType.sample][_run][Run.use_it] = True
                    self.list_of_runs_to_use[DataType.sample].append(_run)

        for _run in self.parent.list_of_runs[DataType.ob].keys():
            if self.parent.list_of_runs[DataType.ob][_run][Run.use_it]:
                if _run in list_of_ob_runs_to_reject:
                    self.parent.list_of_runs[DataType.ob][_run][Run.use_it] = False
                    logging.info(f"\t\t rejecting ob run {_run}!")
                else:
                    self.parent.list_of_runs[DataType.ob][_run][Run.use_it] = True
                    self.list_of_runs_to_use[DataType.ob].append(_run)

        self.parent.list_of_runs_to_use = self.list_of_runs_to_use

    def combining_runs(self):
        logging.info(f"combining runs:")

        list_of_angles = []
        list_of_runs = self.list_of_runs_to_use[DataType.sample]
        for _run in list_of_runs:
            list_of_angles.append(self.parent.list_of_runs[DataType.sample][_run][Run.angle])

        # sort the angles and sort the runs the same way
        index_sorted = sorted(range(len(list_of_angles)), key=lambda k: list_of_angles[k])
        list_of_runs_sorted = [list_of_runs[_index] for _index in index_sorted]
        list_of_angles_sorted = [list_of_angles[_index] for _index in index_sorted]

        logging.info(f"\t{list_of_runs_sorted = }")
        logging.info(f"\t{list_of_angles_sorted = }")

        self.parent.list_of_runs_to_use[DataType.sample] = list_of_runs_sorted
        self.parent.list_of_angles_to_use_sorted = list_of_angles_sorted

        for _data_type in self.parent.list_of_runs.keys():
            _master_data = []
            logging.info(f"\tworking with {_data_type}:")
            for _run in tqdm(self.parent.list_of_runs_to_use[_data_type]):
                _full_path_run = self.parent.list_of_runs[_data_type][_run][Run.full_path]
                logging.info(f"\t\tloading {os.path.basename(_full_path_run)} ...")
                list_tif = retrieve_list_of_tif(_full_path_run)
                _master_data.append(load_data_using_multithreading(list_tif))
                logging.info(f"\t\t loading done!")
            self.parent.master_3d_data_array[_data_type] = np.array(_master_data)

        height, width = np.shape(self.parent.master_3d_data_array[DataType.sample][0])
        self.parent.image_size = {'height': height,
                                  'width': width}
        