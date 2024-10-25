import argparse
import json
import os
import logging

from __code.utilities.time import get_current_time_in_special_file_name_format
from __code import OperatingMode, DataType
from __code.utilities.logging import setup_logging
from __code.utilities.json import load_json_string
from __code.utilities.configuration_file import Configuration, loading_config_file_into_model
from __code.utilities.files import retrieve_list_of_tif
from __code.utilities.load import load_data_using_multithreading

setup_logging("svmbir_reconstruction_cli")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the full svmbir workflow using the provided config file")
    parser.add_argument('config_file', type=str, nargs=1, help="JSON config file created by notebook")
    args = parser.parse_args()

    config_file_name = args.config_file[0]
    config_model = loading_config_file_into_model(config_file_path=config_file_name)
    logging.info(f"loading config file name: {config_file_name}")

    operating_mode = config_model.operating_mode
    combine = operating_mode == OperatingMode.white_beam

    # load sample and ob
    list_sample_runs = config_model.list_of_sample_runs
    sample_base_folder_name = config_model.top_folder.sample
    logging.info(f"{list_sample_runs = }")
    logging.info(f"{sample_base_folder_name = }")

    list_ob_runs = config_model.list_of_ob_runs
    ob_base_folder_name = config_model.top_folder.ob
    logging.info(f"{list_ob_runs = }")
    logging.info(f"{ob_base_folder_name = }")

    list_of_runs = {DataType.sample: [os.path.join(sample_base_folder_name, _file) for _file in list_sample_runs],
                    DataType.ob: [os.path.join(ob_base_folder_name, _file) for _file in list_ob_runs]}

    master_3d_data_array = {DataType.sample: [],
                            DataType.ob: []}
    for _data_type in list_of_runs.keys():
        logging.info(f"loading {_data_type}:")
        for _full_path_run in list_of_runs[_data_type]:
            logging.info(f"\t{os.path.basename(_full_path_run)}")
            list_tif = retrieve_list_of_tif(_full_path_run)
            master_3d_data_array[_data_type].append(load_data_using_multithreading(list_tif,
                                                               combine_tof=combine))
