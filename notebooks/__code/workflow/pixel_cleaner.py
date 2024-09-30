import numpy as np
from tqdm import tqdm
import os
import dxchange
import matplotlib.pyplot as plt
import pandas as pd
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets

from __code import DataType
from __code.config import clean_paras
from __code.parent import Parent


class PixelCleaner(Parent): 

    """
    PixelCleaner Class: find the abnormal pixels (extremely low/high) and replaced by median value of the neighor matrix
    ===========
    to initiate cleaner: 
    data_cleaner = PixelCleaner(clean_paras, clean_path)
    [clean_paras]: parameters used for cleaning (dictionary)
    [clean_path]: the directory where save the cleaned data (if save) and logs (strings)
    ===========
    to clean a 2D image:
    cleaned_data = data_cleaner(orginal_im, save_file_name)
    [original_im]: the image need to be cleaned (M*M array)
    [save_file_name]: the cleaned tiff and its log will be saved in this name (strings)

    """
    low_gate = clean_paras['low_gate']
    high_gate = clean_paras['high_gate']
    r = clean_paras['correct_radius']
    CLEAN = clean_paras['if_clean']
    SAVE_CLEAN = clean_paras['if_save_clean']
    edge_nbr_pixels = clean_paras['edge_nbr_pixels']
        
    def preview_cleaning(self):
        sample_data = self.parent.master_3d_data_array[DataType.sample]
        ob_data = self.parent.master_3d_data_array[DataType.ob]

        sample_histogram = sample_data.sum(axis=0)[self.edge_nbr_pixels: -self.edge_nbr_pixels,
                                                   self.edge_nbr_pixels: -self.edge_nbr_pixels]
        ob_histogram = ob_data.sum(axis=0)[self.edge_nbr_pixels: -self.edge_nbr_pixels,
                                           self.edge_nbr_pixels: -self.edge_nbr_pixels]

        def plot_histogram(nbr_bins=10, nbr_exclude=1):
        
            fig, axs = plt.subplots(nrows=2, ncols=1)
            _, sample_bin_edges = np.histogram(sample_histogram.flatten(), bins=nbr_bins, density=False)
            axs[0].hist(sample_histogram.flatten(), bins=nbr_bins)
            axs[0].set_title('sample histogram')
            axs[0].set_yscale('log')
            axs[0].axvspan(sample_bin_edges[0], sample_bin_edges[nbr_exclude], facecolor='red', alpha=0.2)
            axs[0].axvspan(sample_bin_edges[-nbr_exclude-1], sample_bin_edges[-1], facecolor='red', alpha=0.2)
            
            _, ob_bin_edges = np.histogram(ob_histogram.flatten(), bins=nbr_bins, density=False)
            axs[1].hist(ob_histogram.flatten(), bins=nbr_bins)
            axs[1].set_title('ob histogram')
            axs[1].set_yscale('log')
            axs[1].axvspan(ob_bin_edges[0], ob_bin_edges[nbr_exclude], facecolor='red', alpha=0.2)
            axs[1].axvspan(ob_bin_edges[-nbr_exclude-1], ob_bin_edges[-1], facecolor='red', alpha=0.2)
            plt.tight_layout()
            plt.show()

        self.parent.display_histogram = interactive(plot_histogram,
                                                     nbr_bins = widgets.IntSlider(min=10,
                                                                                max=1000,
                                                                                value=10,
                                                                                description='Nbr bins',
                                                                                continuous_update=False),
                                                    nbr_exclude = widgets.IntSlider(min=1,
                                                                                    max=100,
                                                                                    value=1,
                                                                                    description='Bins to exclude',
                                                                                    continuous_update=False))
        display(self.parent.display_histogram)

    def run(self, im, fname):
        self.im = im
        self.row, self.col = self.im.shape
        self.corr_im = np.nan_to_num(self.im.copy(), nan=0, posinf=0, neginf=0)
        self.log = {}
        self.fname = fname

        if self.CLEAN:
            self.replace_pix()
            self.save_opt()

    def replace_pix(self):
        hist, bin_edges = np.histogram(self.corr_im.flatten(), density=False)
        thres_low = bin_edges[self.low_gate]
        thres_high = bin_edges[self.high_gate]
        x_coords, y_coords = np.nonzero(np.logical_or(self.corr_im <= thres_low, self.corr_im > thres_high))
        r = self.r

        org_val, cor_val = [], []
        for x, y in zip(x_coords, y_coords):
            X_, _X = max(0, x-r), min(self.corr_im.shape[0], x+r)
            Y_, _Y = max(0, y-r), min(self.corr_im.shape[1], y+r)
            org_val.append(self.corr_im[x, y])
            pat = self.im[X_ : _X+1, Y_: _Y+1]
            if np.nonzero(pat > thres_low)[0].size >=4:
                _elements = list(pat.flatten())
                _elements.pop(r*(1+2*r)+r)
                _corrected = np.median(_elements)#sum(_elements)/(pat.size-1)
                self.corr_im[x, y] = _corrected
                cor_val.append(_corrected)
            else:
                print('ERROR, too many zeros around pixel({},{})'.format(x, y))
                cor_val.append('-')
        
        self.log = {'fname': self.fname, 'X': x_coords, 'Y': y_coords, 
                    'original': org_val, 'corrected': cor_val}
        
    def save_opt(self):
        if self.SAVE_CLEAN:
            _fname = os.path.join(self.clean_path, f'ZeroRemove_{self.fname}')
            dxchange.writer.write_tiff(self.corr_im, fname=_fname, overwrite=True)

        log_fld = os.path.join(self.clean_path, 'logs')
        df = pd.DataFrame.from_dict(self.log, orient='columns')
        df.to_csv(os.path.join(log_fld, f'clean_log_{self.fname}.csv'))
        print(f"save log into {os.path.join(log_fld, f'clean_log_{self.fname}.csv')}")
