import logging
import os

def setup_logging(basename_of_log_file=""):

    log_file_name = f"/SNS/VENUS/shared/log/{basename_of_log_file}.log"
    logging.basicConfig(filename=log_file_name,
                        filemode='w',
                        format='[%(levelname)s] - %(asctime)s - %(message)s',
                        level=logging.INFO)
    logging.info(f"*** Starting a new script {basename_of_log_file} ***")
    