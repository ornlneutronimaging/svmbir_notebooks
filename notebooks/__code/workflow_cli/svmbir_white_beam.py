import numpy as np
import os
import glob

import svmbir

from __code.workflow.export import Export
from __code.utilities.files import make_or_reset_folder
from __code.config import NUM_THREADS
from __code.utilities.json import load_json
from __code.utilities.load import load_data_using_multithreading


class SvmbirCliHandler:

    @staticmethod
    def run_reconstruction_from_pre_data_mode(config_json_file, input_data_folder, output_data_folder):
        config = load_json(config_json_file)
        list_tiff = glob.glob(os.path.join(input_data_folder, '*.tiff'))
        list_tiff.sort()
        print(f"loading {len(list_tiff)} images ... ", end="")
        corrected_array_log = load_data_using_multithreading(list_tiff)
        print(f"done!")

        list_of_angles_rad = np.array(config['list_of_angles_rad'])
        height = config['height']
        width = config['width']
        center_offset = config['center_offset']
        sharpness = config['sharpness']
        snr_db = config['snr_db']
        positivity = config['positivity']
        max_iterations = config['max_iterations']
        verbose = config['verbose']
        svmbir_lib_path = config['svmbir_lib_path']

        print(f"launching svmbir ... ", end="")
        reconstruction_array = svmbir.recon(sino=corrected_array_log,
                                            angles=list_of_angles_rad,
                                            num_rows = height,
                                            num_cols = width,
                                            center_offset = center_offset,
                                            sharpness = sharpness,
                                            snr_db = snr_db,
                                            positivity = positivity,
                                            max_iterations = max_iterations,
                                            num_threads = NUM_THREADS,
                                            verbose = verbose,
                                            svmbir_lib_path = svmbir_lib_path,
                                            )
        print(f"done! ", end="")

        print(f"exporting reconstructed slices ... ", end="")
        make_or_reset_folder(output_data_folder)
        o_export = Export(image_3d=reconstruction_array,
                          output_folder=output_data_folder)
        o_export.run()
        print(f"done!")
