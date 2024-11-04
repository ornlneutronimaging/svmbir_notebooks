import os
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
from tqdm import tqdm

from __code.utilities.file_folder_browser import FileFolderBrowser
from __code.utilities.configuration_file import Configuration
from __code import DataType
from __code.utilities.files import retrieve_list_of_runs, get_angle_value
from __code.utilities.nexus import get_proton_charge, get_frame_number

DEBUG = True


class CliConfigBuilder:

    data_type = DataType.sample
    top_folder = "./"
    full_ipts_folder = None
    
    at_least_one_run_with_no_pc_info = False

    def __init__(self):
        self.configuration = Configuration()

    def select_sample_folder(self, system=None):
        
        self.full_ipts_folder = system.System.get_working_dir()
        
        if DEBUG:
            top_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance"
        else:
             top_folder = system.System.get_working_dir()
        
        self.instrument = system.System.get_instrument_selected()


        self.data_type = DataType.sample
        self.top_folder = top_folder
        o_file_browser = FileFolderBrowser(working_dir=top_folder,
                                           next_function=self.data_selected)
        o_file_browser.select_input_folder(instruction=f"Select Top Folder of {self.data_type}",
                                           multiple_flag=False)

    def data_selected(self, top_folder):
        if self.data_type == DataType.sample:
            self.configuration.top_folder.sample = top_folder
        else:
            self.configuration.top_folder.ob = top_folder
        print(f"you selected for {self.data_type}: {top_folder} ")

    def select_ob_folder(self):
        if DEBUG:
            self.top_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September26_2024_PurpleCar_OpenBean_5_0_C_Cd_inBeam_Resonance"
        self.data_type = DataType.ob
        o_file_browser = FileFolderBrowser(working_dir=self.top_folder,
                                           next_function=self.data_selected)
        o_file_browser.select_input_folder(instruction=f"Select Top Folder of {self.data_type}",
                                           multiple_flag=False)

    def select_runs_to_remove(self):
        sample_list_of_runs = retrieve_list_of_runs(self.configuration.top_folder.sample)
        ob_list_list_of_runs = retrieve_list_of_runs(self.configuration.top_folder.ob)

        short_sample_list_of_runs = [os.path.basename(_run) for _run in sample_list_of_runs]
        short_ob_list_of_runs = [os.path.basename(_run) for _run in ob_list_list_of_runs]

        sample_runs = widgets.VBox([
            widgets.Label("Sample"),
            widgets.SelectMultiple(options=short_sample_list_of_runs,
                                    layout=widgets.Layout(height="100%",
                                                            width='100%',
                                                            )),                                                       
        ],
        layout=widgets.Layout(width='200px',
                                height='300px'))
        self.list_of_sample_runs_to_reject_ui = sample_runs.children[1]

        ob_runs = widgets.VBox([
            widgets.Label("OB"),
            widgets.SelectMultiple(options=short_ob_list_of_runs,
                                    layout=widgets.Layout(height="100%",
                                                            width='100%'))
        ],
        layout=widgets.Layout(width='200px',
                                height='300px'))
        self.list_of_ob_runs_to_reject_ui = ob_runs.children[1]

        hori_layout = widgets.HBox([sample_runs, ob_runs])
        display(hori_layout)

    def get_list_of_nexus(self, short_list_of_runs=None, top_folder=None):
        top_nexus_path = os.path.join(self.full_ipts_folder, 'nexus')
        list_of_nexus = []
        for _run in short_list_of_runs:
            _, number = os.path.basename(_run).split("_")
            nexus_path = os.path.join(top_nexus_path, f"{self.instrument}_{number}.nxs.h5")
            if not os.path.exists(nexus_path):
                nexus_path = None
            list_of_nexus.append(nexus_path)
        return list_of_nexus

    def retrieve_metadata(self):
        sample_list_of_runs = retrieve_list_of_runs(self.configuration.top_folder.sample)
        ob_list_list_of_runs = retrieve_list_of_runs(self.configuration.top_folder.ob)

        short_sample_list_of_runs = [os.path.basename(_run) for _run in sample_list_of_runs]
        short_ob_list_of_runs = [os.path.basename(_run) for _run in ob_list_list_of_runs]

        list_of_sample_runs_to_remove = self.list_of_sample_runs_to_reject_ui.value
        list_of_ob_runs_to_remove = self.list_of_ob_runs_to_reject_ui.value

        for _sample in list_of_sample_runs_to_remove:
            short_sample_list_of_runs.remove(_sample)
        self.configuration.list_of_sample_runs = short_sample_list_of_runs

        for _ob in list_of_ob_runs_to_remove:
            short_ob_list_of_runs.remove(_ob)
        self.configuration.list_of_ob_runs = short_ob_list_of_runs

        # build list of NeXus
        sample_list_of_nexus = self.get_list_of_nexus(short_sample_list_of_runs, 
                                                      self.configuration.top_folder.sample)
        ob_list_of_nexus = self.get_list_of_nexus(short_ob_list_of_runs,
                                                  self.configuration.top_folder.ob)

        # get proton charge
        sample_list_proton_charge = []
        for _nexus in tqdm(sample_list_of_nexus):
            sample_list_proton_charge.append(get_proton_charge(_nexus, units='c'))
        self.configuration.list_of_sample_pc = sample_list_proton_charge

        ob_list_proton_charge = []
        for _nexus in tqdm(ob_list_of_nexus):
            ob_list_proton_charge.append(get_proton_charge(_nexus, units='c'))
        self.configuration.list_of_ob_pc = ob_list_proton_charge

        # get frame number
        sample_list_frame_number = []
        for _nexus in tqdm(sample_list_of_nexus):
            sample_list_frame_number.append(get_frame_number(_nexus))
        self.configuration.list_of_sample_frame_number = sample_list_frame_number                                            

        ob_list_frame_number = []
        for _nexus in tqdm(ob_list_of_nexus):
            ob_list_frame_number.append(get_frame_number(_nexus))
        self.configuration.list_of_ob_frame_number = ob_list_frame_number

        # angle value
        sample_list_of_runs = retrieve_list_of_runs(self.configuration.top_folder.sample)
        sample_list_of_angles = []
        for _run in tqdm(sample_list_of_runs):
            sample_list_of_angles.append(get_angle_value(_run))
        self.configuration.list_of_angles = sample_list_of_angles

        # remove bad runs (no tiff, no nexus)
        list_sample_indexes_with_none_in_proton_charge = [i for i, pc in enumerate(sample_list_proton_charge) if pc is None]
        if len(list_sample_indexes_with_none_in_proton_charge):
            self.at_least_one_run_with_no_pc_info = True

        list_sample_indexes_with_none_in_angles = [i for i, angle in enumerate(sample_list_of_angles) if angle is None]

        size_before = len(sample_list_of_runs)
        if len(list_sample_indexes_with_none_in_angles) > 0:
            bad_list_of_runs = sample_list_of_runs[list_sample_indexes_with_none_in_angles]

        for index in list_sample_indexes_with_none_in_angles[::-1]:
            del sample_list_proton_charge[index]
            del sample_list_frame_number[index]
            del sample_list_of_angles[index]
            del sample_list_of_nexus[index]
            del sample_list_of_runs[index]
        size_after = len(sample_list_of_runs)

        if len(bad_list_of_runs) > 0:
            print(f"The program automatically removed {size_before - size_after} bad runs!")
            print(f"{bad_list_of_runs = }")
        else:
            print(f"All selected runs are good to go!")


