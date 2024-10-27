from __code.parent import Parent
from __code.config import clean_paras
from __code.utilities.configuration_file import ImageCleaner


class Initialization(Parent):
    
    def configuration(self):

        low_gate = clean_paras['low_gate']
        high_gate = clean_paras['high_gate']
        correct_radius = clean_paras['correct_radius']
        if_clean = clean_paras['if_clean']
        save_clean = clean_paras['if_save_clean']
        edge_nbr_pixels = clean_paras['edge_nbr_pixels']
        nbr_bins = clean_paras['nbr_bins']        

        o_image_cleaner = ImageCleaner(low_gate=low_gate,
                                       high_gate=high_gate,
                                       correct_radius=correct_radius,
                                       if_clean=if_clean,
                                       save_clean=save_clean,
                                       edge_nbr_pixels=edge_nbr_pixels,
                                       nbr_bins=nbr_bins)

        self.parent.configuration.image_cleaner = o_image_cleaner
        