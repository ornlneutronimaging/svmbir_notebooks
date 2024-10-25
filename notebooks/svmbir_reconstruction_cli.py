import argparse
import json
import os
import logging

from __code.utilities.time import get_current_time_in_special_file_name_format
from __code.utilities.logging import setup_logging
from __code.utilities.json import load_json_string
from __code.utilities.configuration_file import Configuration, loading_config_file_into_model

setup_logging("svmbir_reconstruction_cli")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the full svmbir workflow using the provided config file")
    parser.add_argument('config_file', type=str, nargs=1, help="JSON config file created by notebook")
    args = parser.parse_args()

    config_file_name = args.config_file[0]
    config_model = loading_config_file_into_model(config_file_path=config_file_name)
    logging.info(f"loading config file name: {config_file_name}")

    # load sample and ob
        