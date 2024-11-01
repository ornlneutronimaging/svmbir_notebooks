import os

from utilities.time import get_current_time_in_special_file_name_format
from __code.utilities.files import make_or_reset_folder


def export_slices(config_model, data_array):
    output_folder = config_model.ouptut_folder
    top_folder = os.path.basename(config_model.top_folder.sample)

    full_output_folder_name = os.path.join(output_folder, top_folder + 
                                          f"_reconstructed_on_{get_current_time_in_special_file_name_format()}")
    
    print(f"{full_output_folder_name = }")
    # make_or_reset_folder(full_output_folder_name)