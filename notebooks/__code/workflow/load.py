import glob
import os
import numpy as np
import logging
from tqdm import tqdm

from __code import DataType, Run, OperatingMode
from __code import DEBUG, debug_folder
from __code.parent import Parent
from __code.utilities.file_folder_browser import FileFolderBrowser
from __code.utilities.load import load_data_using_multithreading, load_list_of_tif, load_tiff
from __code.utilities.files import retrieve_list_of_tif


class Load(Parent):

    list_of_runs_to_use = {DataType.sample: [],
                           DataType.ob: [],
    }

    def select_folder(self, data_type=DataType.sample, multiple_flag=False):

        self.parent.current_data_type = data_type
        self.data_type = data_type
        if data_type in [DataType.reconstructed, DataType.extra]:
            working_dir = self.parent.working_dir[DataType.processed]
        else:
            working_dir = self.parent.working_dir[DataType.top]

        if DEBUG:
            self.data_selected(debug_folder[self.parent.MODE][data_type])
            return

        if not os.path.exists(working_dir):
            working_dir = os.path.abspath(os.path.expanduser("~"))

        o_file_browser = FileFolderBrowser(working_dir=working_dir,
                                           next_function=self.data_selected)
        o_file_browser.select_input_folder(instruction=f"Select Top Folder of {data_type}",
                                           multiple_flag=multiple_flag)

    def select_images(self, data_type=DataType.ob):
        self.parent.current_data_type = data_type
        self.data_type = data_type
        if data_type in [DataType.reconstructed, DataType.extra]:
            working_dir = self.parent.working_dir[DataType.processed]
        else:
            working_dir = self.parent.working_dir[DataType.top]

        if DEBUG:
            working_dir = debug_folder[self.parent.MODE][data_type]
            if not os.path.exists(working_dir):
                return
            list_images = glob.glob(os.path.join(working_dir, "*_0045_*.tif*"))
            list_images.sort()
            self.images_selected(list_images=list_images)
            return

        o_file_browser = FileFolderBrowser(working_dir=working_dir,
                                           next_function=self.images_selected)
        o_file_browser.select_images_with_search(instruction="Select all images ...",
                                                 filters={"TIFF": "*.tif*"})
    
    def images_selected(self, list_images):
        if list_images:
            print(f"top {self.data_type} folder is: {os.path.dirname(list_images[0])}")
        else:
            print(f"no {self.data_type} selected !")
            return
        
        list_images.sort()
        logging.info(f"{len(list_images)} {self.data_type} images have been selected!")
        self.parent.list_of_images[self.data_type] = list_images

    def data_selected(self, top_folder):
        logging.info(f"{self.parent.current_data_type} top folder selected: {top_folder}")
        self.parent.working_dir[self.data_type] = top_folder
        print(f"Top {self.data_type} folder selected: {top_folder}")

        if self.parent.MODE == OperatingMode.white_beam:
            list_tiff = glob.glob(os.path.join(top_folder, "*.tif*"))

            if DEBUG:
                list_tiff = list_tiff[0:3]

            list_tiff.sort()
            self.parent.list_of_images[self.data_type] = list_tiff
            logging.info(f"{len(list_tiff)} {self.data_type} files will be loaded!")

        if self.data_type == DataType.sample:
            self.parent.configuration.top_folder.sample = top_folder
        elif self.data_type == DataType.ob:
            self.parent.configuration.top_folder.ob = top_folder

    def load_white_beam_data(self):
        """ from white beam notebook """
        list_of_images = self.parent.list_of_images
        logging.info(f"loading the data:")

        for _data_type in list_of_images.keys():
            logging.info(f"\t{_data_type} ... ")

            if not list_of_images[_data_type]:
                logging.info(f" no files selected!")
                continue
            
            self.parent.master_3d_data_array[_data_type] = load_data_using_multithreading(list_of_images[_data_type])
            # for _file in tqdm(list_of_images[_data_type]):
            #     _data = load_tiff(_file)
            #     logging.info(f"\t{_file}: {np.shape(_data)}")
            #     _list_data.append(_data)
                
            # self.parent.master_3d_data_array[_data_type] = _list_data
            logging.info(f"{np.shape(self.parent.master_3d_data_array[_data_type]) = }")
            logging.info(f"\t{_data_type} Done !")

    def load_data(self, combine=False):
        """combine is True when working with white beam (from tof notebook)"""
        
        logging.info(f"importing the data:")
       
        final_list_of_angles = []
        final_dict_of_pc = {}
        final_dict_of_frame_number = {}

        if combine:
            logging.info(f"\t combine mode is ON")
        else:
            logging.info(f"\t not combining the TOF images")

        list_of_runs_sorted = self.parent.list_of_runs_to_use
        self.parent.configuration.list_of_sample_runs = list_of_runs_sorted[DataType.sample]
        self.parent.configuration.list_of_ob_runs = list_of_runs_sorted[DataType.ob]

        for _data_type in self.parent.list_of_runs.keys():
            _master_data = []
            logging.info(f"\tworking with {_data_type}:")

            _final_list_of_pc = []
            _final_list_of_frame_number = []

            for _run in tqdm(list_of_runs_sorted[_data_type]):
                _full_path_run = self.parent.list_of_runs[_data_type][_run][Run.full_path]
                if _data_type == DataType.sample:
                    final_list_of_angles.append(self.parent.list_of_runs[_data_type][_run][Run.angle])

                logging.info(f"\t\tloading {os.path.basename(_full_path_run)} ...")
                list_tif = retrieve_list_of_tif(_full_path_run)
                _master_data.append(load_data_using_multithreading(list_tif,
                                                                   combine_tof=combine))
                _final_list_of_pc.append(self.parent.list_of_runs[_data_type][_run][Run.proton_charge_c])
                if self.parent.list_of_runs[_data_type][_run][Run.frame_number]:
                    _final_list_of_frame_number.append(self.parent.list_of_runs[_data_type][_run][Run.frame_number])
                logging.info(f"\t\t loading done!")
            self.parent.master_3d_data_array[_data_type] = np.array(_master_data)
            final_dict_of_pc[_data_type] = _final_list_of_pc
            final_dict_of_frame_number[_data_type] = _final_list_of_frame_number
        
        self.parent.final_list_of_angles = final_list_of_angles
        self.parent.configuration.list_of_angles = final_list_of_angles
        self.parent.final_dict_of_pc = final_dict_of_pc
        self.parent.final_dict_of_frame_number = final_dict_of_frame_number

        if combine:
            height, width = np.shape(self.parent.master_3d_data_array[DataType.sample][0])
            nbr_tof = 1
        else:
            nbr_tof, height, width = np.shape(self.parent.master_3d_data_array[DataType.sample][0])
        self.parent.image_size = {'height': height,
                                  'width': width,
                                  'nbr_tof': nbr_tof}
        
        logging.info(f"{self.parent.image_size} = ")

    def load_spectra_file(self):
        list_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
        first_run = list_runs_to_use[0]
        full_path_to_run = self.parent.list_of_runs[DataType.sample][first_run][Run.full_path]
        list_files = glob.glob(os.path.join(full_path_to_run, "*_Spectra.txt"))
        if list_files and os.path.exists(list_files[0]):
            time_spectra_file = list_files[0]
        else:
            time_spectra_file = ""
        self.parent.spectra_file_full_path = time_spectra_file
        