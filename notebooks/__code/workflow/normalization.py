import logging

from __code.parent import Parent
from __code import Run, DataType


class Normalization(Parent):

    def run(self):
        master_3d_data = self.parent.master_3d_data_array_cleaned
        list_of_runs_used = self.parent.list_of_runs_used

        list_proton_charge = {DataType.sample: [],
                              DataType.ob: [],
                             }

        logging.info(f"Normalization:")
        for _data_type in list_of_runs_used.keys():

            logging.info(f"\t{_data_type}:")
            for _run in list_of_runs_used[_data_type]:
                _proton_charge = self.parent.list_of_runs[_data_type][_run][Run.proton_charge_c]
                list_proton_charge[_data_type].append(_proton_charge)
                logging.info(f"\t\t{_run} has a proton charge of {_proton_charge}")

        logging.info(f"{list_proton_charge =}")
