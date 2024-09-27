from skimage.io import imread
import numpy as np
import multiprocessing as mp 

from NeuNorm.normalization import Normalization

from __code.utilities.files import retrieve_list_of_tif


def _worker(fl):
    return (imread(fl).astype(np.float32)).swapaxes(0,1)

def load_data_using_multithreading(list_tif):
    with mp.Pool(processes=10) as pool:
        data = pool.map(_worker, list_tif)

    return np.array(data).sum(axis=0)

def load_data(folder):
    list_tif = retrieve_list_of_tif(folder)
    o_norm = Normalization()
    o_norm.load(list_tif)
    return o_norm.data['sample']['data']

def load_data_using_imread(folder):
    list_tif = retrieve_list_of_tif(folder)
    data = []
    for _file in list_tif:
        data.append(_hype_loader_sum)
        data.append((imread(_file).astype(np.float32)))
    return data
