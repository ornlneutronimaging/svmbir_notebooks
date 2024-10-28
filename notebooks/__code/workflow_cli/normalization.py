import numpy as np
from scipy.ndimage import median_filter

from __code import NormalizationSettings, DataType


def update_normalize_coeff_by_pc(config_model, list_coeff, mean_ob_proton_charge):
    print(f"updating coeff by proton charge ...", end="")
    list_sample_pc = config_model.list_of_sample_pc
    for _index, _sample_pc in enumerate(list_sample_pc):
        list_coeff[_index] *= mean_ob_proton_charge / _sample_pc

    print(f" done!")
    return list_coeff


def update_normalize_coeff_by_frame_number(config_model, list_coeff, mean_ob_frame_number):
    print(f"updating coeff by frame number ...", end="")
    list_sample_frame = config_model.list_of_sample_frame
    for _index, _sample_frame in enumerate(list_sample_frame):
        list_coeff[_index] *= 

    print(f" done!")
    return list_coeff


def update_normalize_coeff_by_roi(config_model, list_coeff, data_array):
    print(f"update coeff by ROI ...", end="")
    _top = config_model.normalization_roi.top
    _bottom = config_model.normalization_roi.bottom
    _left = config_model.normalization_roi.left
    _right = config_model.normalization_roi.right


    print(f" done!")
    return list_coeff


def combine_obs(config_model=None, data_ob=None):
    print(f"Combining OBs ...", end="")
    if len(data_ob) == 1:
        obs_combined = np.array(data_ob[0])
    else:
        obs_combined = np.mean(data_ob, axis=0)
    
    temp_obs_combined = median_filter(obs_combined, size=2)
    index_of_zero = np.where(obs_combined == 0)
    obs_combined[index_of_zero] = temp_obs_combined[index_of_zero]

    mean_proton_charge = -1
    if NormalizationSettings.pc in config_model.list_normalization_settings:
        list_pc = config_model.list_of_ob_pc
        mean_proton_charge = np.mean(list_pc)

    mean_frame_number = -1
    if NormalizationSettings.frame_number in config_model.list_normalization_settings:
        list_frame_number = config_model.list_of_ob_frame_number
        mean_frame_number = np.mean(list_frame_number)

    print(f" done!")
    return obs_combined, mean_proton_charge, mean_frame_number


def normalize(config_model, data_array):
    
    data_array[DataType.ob], mean_ob_proton_charge, mean_ob_frame_number = combine_obs(config_model=config_model, 
                                                                                       data_ob=data_array[DataType.ob])

    list_normalization_settings_selected = config_model.list_normalization_settings

    list_coeff = np.ones(len(data_array[DataType.sample]))
    if NormalizationSettings.pc in list_normalization_settings_selected:
        list_coeff = update_normalize_coeff_by_pc(config_model, list_coeff, mean_ob_proton_charge)

    if NormalizationSettings.frame_number in list_normalization_settings_selected:
        list_coeff = 

    if NormalizationSettings.roi in list_normalization_settings_selected:
        pass

    return data_array