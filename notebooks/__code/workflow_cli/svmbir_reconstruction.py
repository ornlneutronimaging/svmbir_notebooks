import numpy as np

from __code.config import NUM_THREADS, SVMBIR_LIB_PATH
from __code.utilities.general import retrieve_parameters


def svmbir_reconstruction(config_model, data_array):
    svmbir_config = config_model.svmbir_config
    dict_parameters = retrieve_parameters(svmbir_config)
    top_slice = dict_parameters['top_slice']
    del dict_parameters['top_slice']
    bottom_slice = dict_parameters['bottom_slice']
    del dict_parameters['bottom_slice']
    list_of_angles_deg = config_model.list_of_angles
    list_of_angles_rad = [np.deg2rad(_angle) for _angle in list_of_angles_deg]
    image_width = config_model.image_size.width
    image_height = config_model.image_size.height

    # make call
    