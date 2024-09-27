import numpy as np
from skimage.io import imread
from tqdm import tqdm
import glob, os
import multiprocessing as mp 

def worker(fl):
    return (imread(fl).astype(np.float32)).swapaxes(0,1)

def hype_loader_sum(fls_lst):
    with mp.Pool(processes=10) as pool:
        data = pool.map(worker, fls_lst)

    return np.array(data).sum(axis=0)

# load a data
fld_path = ('/SNS/VENUS/IPTS-33699/shared/processed_data/'
            'September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance')
flds = glob.glob(os.path.join(fld_path, 'Run*')) # find all projections
flds.sort()

print(flds)
flds = flds[0:5]

projs = []
for fld in tqdm(flds):
    print(f"working ")
    fls_lst = glob.glob(os.path.join(fld, '*.tif*'))
    fls_lst.sort()
    projs.append(hype_loader_sum(fls_lst))

print(np.shape(flds))