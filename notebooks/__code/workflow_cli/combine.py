import logging

from __code import OperatingMode


def combine_tof_data(config_model, master_data):
    
    operating_mode = config_model.operating_mode
    if operating_mode == OperatingMode.white_beam:
        logging.info(f"white mode, all TOF data have already been combined!")
        return master_data
    
    return master_data
    