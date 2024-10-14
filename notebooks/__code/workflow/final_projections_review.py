import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets

from __code.parent import Parent
from __code import DataType


class FinalProjectionsReview(Parent):
    
    def run(self):
      
        corrected_array = self.parent.corrected_images
        nbr_images = len(corrected_array)

        list_angles = self.parent.final_list_of_angles
        list_runs = self.parent.list_of_runs_to_use[DataType.sample]

        nbr_cols = 5
        nbr_rows = int(np.ceil(nbr_images / nbr_cols))

        display(widgets.HTML("Scales kept between 0 and 1!"))

        fig, axs =  plt.subplots(nrows=nbr_rows, ncols=nbr_cols,
                                figsize=(nbr_cols*2,nbr_rows*2))

        _index = 0
        for _row in np.arange(nbr_rows):
            for _col in np.arange(nbr_cols):
                _index = _col + _row * nbr_cols
                if _index == (nbr_images):
                    break
                
                axs[_row][_col].set_title(f"{list_runs[_index]}, {list_angles[_index]}")
                axs[_row][_col].imshow(corrected_array[_index], vmin=0, vmax=1)

        for _row in np.arange(nbr_rows):
            for _col in np.arange(nbr_cols):
                axs[_row][_col].axis('off')

        plt.tight_layout()
        plt.show()
