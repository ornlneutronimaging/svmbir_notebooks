import numpy as np


class RemoveStrips:

    sinogram = None

    def __init__(self, parent=None):
        self.parent = parent
        self.calculate_sinogram()

    def calculate_sinogram(self, data_3d):
        self.sinogram = np.moveaxis(data_3d, 1, 0)

    def run(self):
        self.perform_cleaning()
        self.display_cleaning()

    def perform_cleaning(self):
        pass

    def display_cleaning(self):
        pass
    