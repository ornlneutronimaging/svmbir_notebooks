import numpy as np


class RemoveStrips:

    sinogram = None

    list_algo = {'remove_stripe_fw': 'Remove horizontal stripes from sinogram using the Fourier-Wavelet (FW) based method [B4]',
                 'remove_stripe_ti': "Remove horizontal stripes from sinogram using Titarenko's approach [B13]",
                 'remove_stripe_sf': "Normalize raw projection data using a smoothing filter approach.",
                 'remove_stripe_based_sorting': ""

}
    


    def __init__(self, parent=None):
        self.parent = parent
        self.calculate_sinogram()

    def calculate_sinogram(self, data_3d):
        self.sinogram = np.moveaxis(data_3d, 1, 0)

    def select_algorithms(self):
        pass





    def run(self):
        self.perform_cleaning()
        self.display_cleaning()

    def perform_cleaning(self):
        pass

    def display_cleaning(self):
        pass
    