import numpy as np
import os
import glob
import logging
import svmbir

from __code.workflow.export import Export
from __code.utilities.logging import setup_logging
from __code.utilities.files import make_or_reset_folder, make_folder
from __code.config import NUM_THREADS, SVMBIR_LIB_PATH
from __code.utilities.json import load_json_string
from __code.utilities.load import load_data_using_multithreading
from __code.utilities.time import get_current_time_in_special_file_name_format


class SvmbirCliHandler:


    @staticmethod
    def merge_reconstructed_slices(output_data_folder=None, top_slice=0, list_of_output_folders=None, list_of_slices_to_reconstruct=None):
        
        final_output_folder = output_data_folder

        logging.info(f"merge reconstructed slices ...")
        logging.info(f"\t{output_data_folder = }")
        logging.info(f"\t{top_slice = }")
        logging.info(f"\t{list_of_output_folders = }")
        logging.info(f"\t{list_of_slices_to_reconstruct = }")

        list_folder_tiff = {}
        for _index, _folder in enumerate(list_of_output_folders):
            _list_tiff = glob.glob(os.path.join(_folder, '*.tiff'))
            if len(_list_tiff) == 0:
                raise ValueError(f"no tiff files found in {_folder}")
            
            _list_tiff.sort()
            list_folder_tiff[_index] = _list_tiff

        list_slices_already_processed = []
        for _index, [top_slice_index, bottom_slice_index] in enumerate(list_of_slices_to_reconstruct):
            logging.info(f"working with folder: {os.path.dirname(list_folder_tiff[_index][0])}")
            logging.info(f"\tfrom slice #{top_slice_index} to slice #{bottom_slice_index}")

            list_slices = np.arange(top_slice_index, bottom_slice_index)
            for _tiff_index, _slice_index in enumerate(list_slices):
                if _slice_index in list_slices_already_processed:
                    continue

                else:
                    list_slices_already_processed.append(_slice_index)
                    logging.info(f"moving slice #{_slice_index} ({os.path.basename(list_folder_tiff[_index][_tiff_index])}) -> #image_{_slice_index + top_slice:03d}.tiff ... ")
                    _new_tiff_file = os.path.join(final_output_folder, f"image_{_slice_index + top_slice:03d}.tiff")
                    os.rename(list_folder_tiff[_index][_tiff_index], _new_tiff_file)
                    
            # remove the input folder
            logging.info(f"removing folder {list_of_output_folders[_index]}!")
            os.rmdir(list_of_output_folders[_index])


    @staticmethod
    def run_reconstruction_from_pre_data_mode(config_json_file):

        config = load_json_string(config_json_file)
        logging.info(f"config = {config}")

        input_data_folder = config["projections_pre_processing_folder"]
        base_output_folder = config['output_folder']

        list_tiff = glob.glob(os.path.join(input_data_folder, '*.tiff'))
        list_tiff.sort()
        print(f"loading {len(list_tiff)} images ... ", end="")
        logging.info(f"loading {len(list_tiff)} images ... ")
        corrected_array_log = load_data_using_multithreading(list_tiff)
        print(f"done!")
        logging.info(f"loading {len(list_tiff)} images ... done")
      
        list_of_angles_rad = np.array(config['list_of_angles'])
        # height = config['image_size']['height']
        # width = config['image_size']['width']
        # center_offset = config['center_offset']
        center_offset = 0

        sharpness = config['svmbir_config']['sharpness']
        snr_db = config['svmbir_config']['snr_db']
        positivity = config['svmbir_config']['positivity']
        max_iterations = config['svmbir_config']['max_iterations']
        verbose = config['svmbir_config']['verbose']
        svmbir_lib_path = SVMBIR_LIB_PATH
        max_resolutions = config['svmbir_config']['max_resolutions']
        list_of_slices_to_reconstruct = config['list_of_slices_to_reconstruct']
        top_slice = config['crop_region']['top']

        logging.info(f"Before switching y and x coordinates:")
        logging.info(f"{np.shape(corrected_array_log) = }")
        corrected_array_log = np.swapaxes(corrected_array_log, 1, 2)
        logging.info(f"After switching y and x coordinates:")
        logging.info(f"{np.shape(corrected_array_log) = }")

        logging.info(f"{list_of_angles_rad = }")
        # logging.info(f"{height = }")
        # logging.info(f"{width = }")
        logging.info(f"{center_offset = }")
        logging.info(f"{sharpness = }")
        logging.info(f"{snr_db = }")
        logging.info(f"{positivity = }")
        logging.info(f"{max_iterations = }")
        logging.info(f"{max_resolutions = }")
        logging.info(f"{verbose = }")
        logging.info(f"{svmbir_lib_path = }")
        logging.info(f"{input_data_folder = }")
        logging.info(f"{base_output_folder = }")
        logging.info(f"{list_of_slices_to_reconstruct = }")
        
        output_data_folder = os.path.join(base_output_folder, f"reconstructed_data_{get_current_time_in_special_file_name_format()}")
        logging.info(f"{output_data_folder = }")

        # make_or_reset_folder(output_data_folder)
        make_or_reset_folder(output_data_folder)

        list_of_output_folders = []
        if list_of_slices_to_reconstruct:

            for [index, [top_slice_index, bottom_slice_index]] in enumerate(list_of_slices_to_reconstruct):
                print(f"working with set of slices #{index}: from {top_slice} to {bottom_slice_index-1}. ", end="") 
                logging.info(f"working with set of slices #{index}: from {top_slice} to {bottom_slice_index-1}")
                print(f"launching svmbir #{index} ... ", end="")
                logging.info(f"launching svmbir #{index} ...")
        
                _sino = corrected_array_log[:, top_slice:bottom_slice_index, :]
        
                logging.info(f"\t{np.shape(_sino) = }")
                reconstruction_array = svmbir.recon(sino=_sino,
                                                    angles=list_of_angles_rad,
                                                    # num_rows = height,
                                                    # num_cols = width,
                                                    center_offset = center_offset,
                                                    max_resolutions = max_resolutions,
                                                    sharpness = sharpness,
                                                    snr_db = snr_db,
                                                    positivity = positivity,
                                                    max_iterations = max_iterations,
                                                    num_threads = NUM_THREADS,
                                                    verbose = verbose,
                                                    svmbir_lib_path = svmbir_lib_path,
                                                    )
                print(f"done! ")
                logging.info(f"done with #{index}!")
                _index = f"{index:03d}"
                print(f"exporting reconstructed slices set #{_index} ... ", end="")
                logging.info(f"\t{np.shape(reconstruction_array) = }")
                logging.info(f"exporting reconstructed data set #{_index} ...")

                _output_data_folder = os.path.join(output_data_folder, f"set_{_index}")
                logging.info(f"making or resetting folder {_output_data_folder}")
                list_of_output_folders.append(_output_data_folder)
                make_or_reset_folder(_output_data_folder)
                o_export = Export(image_3d=reconstruction_array,
                                  output_folder=_output_data_folder)
                o_export.run()
                print(f"done!")

            SvmbirCliHandler.merge_reconstructed_slices(output_data_folder=output_data_folder, 
                                                        top_slice=top_slice,
                                                        list_of_output_folders=list_of_output_folders,
                                                        list_of_slices_to_reconstruct=list_of_slices_to_reconstruct)

        else:

            print(f"launching svmbir with all slices ... ", end="")
            logging.info(f"launching svmbir with all slices ...")
       
            reconstruction_array = svmbir.recon(sino=corrected_array_log,
                                                angles=list_of_angles_rad,
                                                # num_rows = height,
                                                # num_cols = width,
                                                center_offset = center_offset,
                                                max_resolutions = max_resolutions,
                                                sharpness = sharpness,
                                                snr_db = snr_db,
                                                positivity = positivity,
                                                max_iterations = max_iterations,
                                                num_threads = NUM_THREADS,
                                                verbose = verbose,
                                                svmbir_lib_path = svmbir_lib_path,
                                                )
            print(f"done! ")
            logging.info(f"done with!")

            print(f"exporting reconstructed slices ... ", end="")
            logging.info(f"{np.shape(reconstruction_array) = }")
            logging.info(f"exporting reconstructed data ...")
            o_export = Export(image_3d=reconstruction_array,
                            output_folder=output_data_folder)
            o_export.run()
            print(f"done!")

        logging.info(f"exporting reconstructed data ... done!")
