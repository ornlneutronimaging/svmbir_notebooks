import numpy as np
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import logging
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
from scipy.ndimage import median_filter
from imars3d.backend.corrections.gamma_filter import gamma_filter
 
from __code import DataType, CleaningAlgorithm
from __code.config import clean_paras, NUM_THREADS, TOMOPY_REMOVE_OUTLIER_THRESHOLD_RATIO
from __code.parent import Parent
from __code.workflow.load import Load
from __code.workflow.export import Export
from __code.utilities.files import make_or_reset_folder
from __code.utilities.images import replace_pixels


class ImagesCleaner(Parent): 

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
    nbr_bins = clean_paras['nbr_bins']
            
    def settings(self):
        self.histo_ui = widgets.Checkbox(value=False,
                                         description="Histogram")
        self.tomo_ui = widgets.Checkbox(value=False,
                                        description="Threshold")
        v_box = widgets.VBox([self.histo_ui, self.tomo_ui])
        display(v_box)

    def cleaning_setup(self):

        # update configuration
        list_algo = []
        if self.histo_ui.value:
            list_algo.append(CleaningAlgorithm.histogram)
        if self.tomo_ui.value:
            list_algo.append(CleaningAlgorithm.threshold)
        self.parent.configuration.list_clean_algorithm = list_algo

        if self.histo_ui.value:
            sample_data = np.array(self.parent.master_3d_data_array[DataType.sample])
            ob_data = np.array(self.parent.master_3d_data_array[DataType.ob])
            dc_data = None
            if self.parent.master_3d_data_array[DataType.dc]:
                dc_data = self.parent.master_3d_data_array[DataType.dc]

            sample_histogram = sample_data.sum(axis=0)[self.edge_nbr_pixels: -self.edge_nbr_pixels,
                                                    self.edge_nbr_pixels: -self.edge_nbr_pixels]
            ob_histogram = ob_data.sum(axis=0)[self.edge_nbr_pixels: -self.edge_nbr_pixels,
                                            self.edge_nbr_pixels: -self.edge_nbr_pixels]

            if dc_data:
                dc_histogram = dc_data.sum(axis=0)[self.edge_nbr_pixels: -self.edge_nbr_pixels,
                                self.edge_nbr_pixels: -self.edge_nbr_pixels]

            nrows = 2 if dc_data is None else 3
            
            def plot_histogram(nbr_bins=10, nbr_exclude=1):
            
                fig, axs = plt.subplots(nrows=nrows, ncols=1)
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

                if dc_data:
                    _, dc_bin_edges = np.histogram(dc_histogram.flatten(), bins=nbr_bins, density=False)
                    axs[2].hist(dc_histogram.flatten(), bins=nbr_bins)
                    axs[2].set_title('dc histogram')
                    axs[2].set_yscale('log')
                    axs[2].axvspan(dc_bin_edges[0], dc_bin_edges[nbr_exclude], facecolor='red', alpha=0.2)
                    axs[2].axvspan(dc_bin_edges[-nbr_exclude-1], dc_bin_edges[-1], facecolor='red', alpha=0.2)
                    plt.tight_layout()
                    plt.show()

                return nbr_bins, nbr_exclude

            self.parent.display_histogram = interactive(plot_histogram,
                                                        nbr_bins = widgets.IntSlider(min=10,
                                                                                    max=1000,
                                                                                    value=10,
                                                                                    description='Nbr bins',
                                                                                    continuous_update=False),
                                                        nbr_exclude = widgets.IntSlider(min=0,
                                                                                        max=10,
                                                                                        value=1,
                                                                                        description='Bins to excl.',
                                                                                        continuous_update=False,
                                                                                        ),
                                                        )
            display(self.parent.display_histogram)

    def cleaning(self):

        # sample_data = self.parent.master_3d_data_array[DataType.sample]
        # ob_data = self.parent.master_3d_data_array[DataType.ob]
        # self.parent.master_3d_data_array = {DataType.sample: sample_data,
        #                                             DataType.ob: ob_data}

        self.cleaning_by_histogram()
        self.cleaning_by_imars3d()

    def cleaning_by_imars3d(self):
        
        if not self.tomo_ui.value:
            logging.info(f"cleaning using tomopy: OFF")
            return
    
        sample_data = np.array(self.parent.master_3d_data_array[DataType.sample])
        cleaned_sample = gamma_filter(arrays=sample_data)
        self.parent.master_3d_data_array[DataType.sample] = cleaned_sample
                
        ob_data = np.array(self.parent.master_3d_data_array[DataType.ob])
        cleaned_ob = gamma_filter(arrays=ob_data)
        self.parent.master_3d_data_array[DataType.ob] = cleaned_ob

        if self.parent.list_of_images[DataType.dc]:
            dc_data = np.array(self.parent.master_3d_data_array[DataType.dc])
            cleaned_dc = gamma_filter(arrays=dc_data)
            self.parent.master_3d_data_array[DataType.dc] = cleaned_dc
            
    def cleaning_by_histogram(self):

        if not self.histo_ui.value:
            logging.info(f"cleaning by histogram: OFF")
            return

        self.nbr_bins, nbr_bins_to_exclude = self.parent.display_histogram.result

        # update configuration
        self.parent.configuration.histogram_cleaning_settings.nbr_bins = self.nbr_bins
        self.parent.configuration.histogram_cleaning_settings.bins_to_exclude = nbr_bins_to_exclude

        sample_data = self.parent.master_3d_data_array[DataType.sample]
        ob_data = self.parent.master_3d_data_array[DataType.ob]
        dc_data = self.parent.master_3d_data_array[DataType.dc]

        if nbr_bins_to_exclude == 0:
            logging.info(f"0 bin selected, the raw data will be used!")

        else:         
            logging.info(f"user selected {nbr_bins_to_exclude} bins to exclude")
          
            logging.info(f"\t {np.shape(sample_data) = }")
            logging.info(f"\t {np.shape(ob_data) = }")

            logging.info(f"\tcleaning sample ...")
            cleaned_sample_data = []
            for _data in tqdm(sample_data):
                cleaned_im = replace_pixels(im=_data.copy(),
                                            nbr_bins=self.nbr_bins,
                                            low_gate=nbr_bins_to_exclude,
                                            high_gate=self.nbr_bins - nbr_bins_to_exclude,
                                            correct_radius=self.r)
                cleaned_sample_data.append(cleaned_im)          
            self.parent.master_3d_data_array[DataType.sample] = cleaned_sample_data
            logging.info(f"\tcleaned sample!")

            logging.info(f"\tcleaning ob ...")
            cleaned_ob_data = []
            for _data in tqdm(ob_data):
                cleaned_im = replace_pixels(im=_data.copy(),
                                            nbr_bins=self.nbr_bins,
                                            low_gate=nbr_bins_to_exclude,
                                            high_gate=self.nbr_bins - nbr_bins_to_exclude,
                                            correct_radius=self.r)
                cleaned_ob_data.append(cleaned_im)          
            self.parent.master_3d_data_array[DataType.ob] = cleaned_ob_data
            logging.info(f"\tcleaned ob!")

            if self.parent.list_of_images[DataType.dc]:
                logging.info(f"\tcleaning dc ...")
                cleaned_dc_data = []
                for _data in tqdm(dc_data):
                    cleaned_im = replace_pixels(im=_data.copy(),
                                                nbr_bins=self.nbr_bins,
                                                low_gate=nbr_bins_to_exclude,
                                                high_gate=self.nbr_bins - nbr_bins_to_exclude,
                                                correct_radius=self.r)
                    cleaned_dc_data.append(cleaned_im)          
                self.parent.master_3d_data_array[DataType.ob] = cleaned_dc_data
                logging.info(f"\tcleaned dc!")

    # def check_cleaned_pixels(self):
    #     sample_data = self.parent.master_3d_data_array[DataType.sample]  
    #     nbr_images = len(sample_data)     
    #     sample_data_cleaned = self.parent.master_3d_data_array[DataType.sample]

    #     def plot_cleaned_pixesl(image_index):
            
    #         fig, axs = plt.subplots(nrows=1, ncols=2)

    #         im1 = axs[0].imshow(sample_data[image_index])
    #         axs[0].set_title(f"Raw image #{image_index}")
    #         plt.colorbar(im1, ax=axs[0])
    #         im2 = axs[1].imshow(sample_data_cleaned[image_index])
    #         axs[1].set_title(f"Cleaned image #{image_index}")
    #         plt.colorbar(im2, ax=axs[1])

    #         plt.tight_layout()
    #         plt.show()

    #     display_comparison = interactive(plot_cleaned_pixesl,
    #                                      image_index = widgets.IntSlider(min=0,
    #                                                                      max=nbr_images-1,
    #                                                                      value=0))
    #     display(display_comparison)
        
    def select_export_folder(self):
        o_load = Load(parent=self.parent)
        o_load.select_folder(data_type=DataType.cleaned_images)
    
    def export_clean_images(self):
        
        logging.info(f"Exporting the cleaned images")
        logging.info(f"\tfolder selected: {self.parent.working_dir[DataType.cleaned_images]}")

        master_3d_data = self.parent.master_3d_data_array_cleaned

        master_base_folder_name = f"{os.path.basename(self.parent.working_dir[DataType.sample])}_cleaned"
        full_output_folder = os.path.join(self.parent.working_dir[DataType.cleaned_images],
                                          master_base_folder_name)

        # sample
        logging.info(f"working with sample:")
        sample_full_output_folder = os.path.join(full_output_folder, "sample")
        logging.info(f"\t {sample_full_output_folder =}")
        make_or_reset_folder(sample_full_output_folder)

        o_export = Export(image_3d=master_3d_data[DataType.sample],
                          output_folder=sample_full_output_folder)
        o_export.run()

        # ob
        logging.info(f"working with ob:")
        ob_full_output_folder = os.path.join(full_output_folder, 'ob')
        logging.info(f"\t {ob_full_output_folder =}")
        make_or_reset_folder(ob_full_output_folder)

        o_export = Export(image_3d=master_3d_data[DataType.ob],
                          output_folder=ob_full_output_folder)
        o_export.run()
        



        # self.export_cleaned_images(dict_of_images=self.parent.master_3d_data_array_cleaned,
        #                 output_folder=self.parent.working_dir[DataType.cleaned_images])

    


    # def save_opt(self):
    #     if self.SAVE_CLEAN:
    #         _fname = os.path.join(self.clean_path, f'ZeroRemove_{self.fname}')
    #         dxchange.writer.write_tiff(self.corr_im, fname=_fname, overwrite=True)

    #     log_fld = os.path.join(self.clean_path, 'logs')
    #     df = pd.DataFrame.from_dict(self.log, orient='columns')
    #     df.to_csv(os.path.join(log_fld, f'clean_log_{self.fname}.csv'))
    #     print(f"save log into {os.path.join(log_fld, f'clean_log_{self.fname}.csv')}")
