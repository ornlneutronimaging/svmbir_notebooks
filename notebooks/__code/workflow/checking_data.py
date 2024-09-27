import logging
import os
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
from IPython.core.display import HTML, display

from __code.parent import Parent
from __code.config import PROTON_CHARGE_TOLERANCE_C
from __code import DataType, Run
from __code.utilities.files import retrieve_list_of_runs, retrieve_list_of_tif
from __code.utilities.nexus import get_proton_charge
from __code.utilities.math import calculate_most_dominant_int_value_from_list


class CheckingData(Parent):

    list_of_runs = {DataType.sample: None,
                    DataType.ob: None}
    list_of_metadata = {}

    def run(self):

        # retrieve the full list of runs found in the top folder
        self.retrieve_runs()

        # check empty runs
        self.reject_empty_runs()

        # retrieve proton charge of runs
        self.retrieve_proton_charge()

    def retrieve_runs(self):
        """retrieve the full list of runs in the top folder of sample and ob"""

        logging.info(f"Retrieving runs:")
        for _data_type in self.list_of_runs.keys():
            list_of_runs = retrieve_list_of_runs(top_folder=self.parent.working_dir[_data_type])
            logging.info(f"\tfound {len(list_of_runs)} {_data_type} runs")
            
            for _run in list_of_runs:
                self.parent.list_of_runs[_data_type][os.path.basename(_run)] = {Run.full_path: _run,
                                                                                Run.proton_charge_c: None,
                                                                                Run.use_it: True}
          
    def reject_empty_runs(self):

        logging.info(f"Rejecting empty runs:")
        for _data_type in self.parent.list_of_runs.keys():
            list_of_runs = list(self.parent.list_of_runs[_data_type].keys())

            list_of_runs_to_keep = []
            list_of_runs_to_remove = []

            for _run in list_of_runs:

                _run_full_path = self.parent.list_of_runs[_data_type][_run][Run.full_path]
                list_tif = retrieve_list_of_tif(_run_full_path)
                if len(list_tif) > 0:
                    list_of_runs_to_keep.append(_run_full_path)
                    self.parent.list_of_runs[_data_type][_run][Run.use_it] = True
                else:
                    list_of_runs_to_remove.append(_run)
                    self.parent.list_of_runs[_data_type][_run][Run.use_it] = False

            logging.info(f"\trejected {len(list_of_runs_to_remove)} {_data_type} runs")
            logging.info(f"\t -> {[os.path.basename(_file) for _file in list_of_runs_to_remove]}")

    def retrieve_proton_charge(self):
        logging.info(f"Retrieving proton charge values:")
        top_nexus_path = self.parent.working_dir[DataType.nexus]
        list_proton_charge_c = {DataType.sample: [],
                                DataType.ob: []} 
        for _data_type in self.parent.list_of_runs.keys():
            _list_proton_charge = []
            for _run in self.parent.list_of_runs[_data_type]:
                _, number = os.path.basename(_run).split("_")
                nexus_path = os.path.join(top_nexus_path, f"{self.parent.instrument}_{number}.nxs.h5")
                proton_charge = get_proton_charge(nexus_path)
                _list_proton_charge.append(proton_charge)
                self.list_of_metadata[_run] = proton_charge
                self.parent.list_of_runs[_data_type][_run][Run.proton_charge_c] = proton_charge/1e12
            list_proton_charge_c[_data_type] = [_pc/1e12 for _pc in _list_proton_charge]
            logging.info(f"\t{_data_type}: {list_proton_charge_c[_data_type]}")

        default_sample_proton_charge = calculate_most_dominant_int_value_from_list(list_proton_charge_c[DataType.sample])
        default_ob_proton_charge = calculate_most_dominant_int_value_from_list(list_proton_charge_c[DataType.ob])

        def plot_proton_charges(sample_proton_charge_value, ob_proton_charge_value, proton_charge_threshold):        
            fig, axs = plt.subplots(nrows=1, ncols=1)
            axs.set_title("Proton charge (C) of selected runs")
            axs.plot(list_proton_charge_c[DataType.sample], 'g+', label=DataType.sample)
            axs.plot(list_proton_charge_c[DataType.ob], 'bo', label=DataType.ob)
            axs.set_xlabel("file index")
            axs.set_ylabel("proton charge (C)")
            axs.legend()
    
            axs.axhline(sample_proton_charge_value, linestyle='--', color='green')
            sample_proton_charge_range = [sample_proton_charge_value + proton_charge_threshold,
                                   sample_proton_charge_value - proton_charge_threshold]
            axs.axhspan(sample_proton_charge_range[0], 
                        sample_proton_charge_range[1], facecolor='green', alpha=0.2)

            axs.axhline(ob_proton_charge_value, linestyle='--', color='blue')
            ob_proton_charge_range = [ob_proton_charge_value + proton_charge_threshold,
                                      ob_proton_charge_value - proton_charge_threshold]
            axs.axhspan(ob_proton_charge_range[0], 
                        ob_proton_charge_range[1], facecolor='blue', alpha=0.2)

            plt.show()

            return sample_proton_charge_value, ob_proton_charge_value, proton_charge_threshold

        self.parent.selection_of_pc = interactive(plot_proton_charges,
                              sample_proton_charge_value = widgets.FloatSlider(min=0.01,
                                                                       max=50,
                                                                       value=default_sample_proton_charge,
                                                                       description='sample pc',
                                                                       continuous_update=True),
                              ob_proton_charge_value = widgets.FloatSlider(min=0.01,
                                                                       max=50,
                                                                       value=default_ob_proton_charge,
                                                                       description='ob pc',
                                                                       continuous_update=True),
                              proton_charge_threshold = widgets.FloatSlider(min=0.0001,
                                                                        max=1,
                                                                        description='threshold',
                                                                        value=PROTON_CHARGE_TOLERANCE_C,
                                                                        continuous_update=True),
                                                                        )
        display(self.parent.selection_of_pc)

        # display(HTML("Select the proton charge requested for <b>sample</b> and <b>ob</b>"))    

    def checking_minimum_requirements(self):
        """at least 1 OB and 3 samples selected"""
        logging.info(f"Checking minimum requirements:")
                
        list_ob = self.parent.list_of_ob_runs_to_reject_ui.options
        list_ob_selected = self.parent.list_of_ob_runs_to_reject_ui.value

        # at least 1 OB
        if len(list_ob) == 0:
            logging.info(f"\tno OB available. BAD!")
            self.parent.minimum_requirements_met = False
            return
        
        # at least 1 OB to keep
        if len(list_ob) == len(list_ob_selected):
            logging.info(f"\tnot keeping any OB. BAD!")
            self.parent.minimum_requirements_met = False
            return
        
        list_sample = self.parent.list_of_sample_runs_to_reject_ui.options
        list_sample_selected = self.parent.list_of_sample_runs_to_reject_ui.value
        
        # at least 3 projections
        if len(list_sample) < 3:
            logging.info(f"\tless than 3 sample runs available. BAD!")
            self.parent.minimum_requirements_met = False
            return
        
        if len(list_sample) == len(list_sample_selected):
            logging.info(f"\tnot keeping any sample run. BAD!")
            self.parent.minimum_requirements_met = False
            return
        
        logging.info(f"At least 1 OB and 3 sample runs. GOOD!")
        self.parent.minimum_requirements_met = True

    def minimum_requirement_not_met(self):
        display(HTML(f"<font color=red><b>STOP!</b> Make sure you have at least 3 sample and 1 OB selected!</font>"))

