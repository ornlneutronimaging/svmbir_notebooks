import glob
import os
import json
import shutil


def retrieve_list_of_files_from_folders(list_folders):
    list_files = []
    for _folder in list_folders:
        _tiff_files = glob.glob(os.path.join(_folder, "*.tif*"))
        list_files = [*list_files, *_tiff_files]

    list_files.sort()
    return list_files


def retrieve_list_of_runs(top_folder):
    list_runs = glob.glob(os.path.join(top_folder, "Run_*"))
    list_runs.sort()
    return list_runs


def retrieve_list_of_tif(folder):
    list_tif = glob.glob(os.path.join(folder, "*.tif*"))
    list_tif.sort()
    return list_tif


def load_json(json_file_name):
    if not os.path.exists(json_file_name):
        return None

    with open(json_file_name) as json_file:
        data = json.load(json_file)

    return data


def save_json(json_file_name, json_dictionary=None):
    with open(json_file_name, 'w') as outfile:
        json.dump(json_dictionary, outfile)


def make_or_reset_folder(folder_name):
    if os.path.exists(folder_name):
         shutil.rmtree(folder_name)
    os.makedirs(folder_name)
    