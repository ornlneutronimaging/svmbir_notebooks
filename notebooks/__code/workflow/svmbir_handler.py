import numpy as np
from IPython.display import display
import ipywidgets as widgets
from IPython.core.display import HTML
import matplotlib.pyplot as plt
from ipywidgets import interactive

from __code.parent import Parent


class SvmbirHandler(Parent):

    def set_settings(self):

        # corrected_array = self.parent.corrected_images
        # nbr_images = len(corrected_array)
        # height, _ = np.shape(corrected_array[0])        

        # display(widgets.HTML("<font size=5>Select range of slices to reconstruct</font"))

        # def plot_range(image_index, top_slice, bottom_slice):

        #     fig, axs = plt.subplots(nrows=1, ncols=1)
        #     axs[0].imshow(corrected_array[image_index], vmin=0, vmax=1)
        #     axs[0].axhspan(top_slice, bottom_slice, color='blue', alpha=0.3)
        #     axs[0].axhline(top_slice, color='red', linestyle='--')
        #     axs[0].axhline(bottom_slice, color='red', linestyle='--')

        #     plt.tight_layout()
        #     plt.show()

        # self.display_corrected_range = interactive(plot_range,
        #                                             image_index = widgets.IntSlider(min=0,
        #                                                                             max=nbr_images-1,
        #                                                                             value=0),
        #                                            top_slice = widgets.IntSlider(min=0,
        #                                                                          max=height-1,
        #                                                                          value=0),
        #                                             bottom_slice = widgets.IntSlider(min=0,
        #                                                                              max=height-1,
        #                                                                              value=height-1),
        #                                             )
        # display(self.display_corrected_range)

        sharpness_ui = widgets.FloatSlider(min=0,
                                           max=1,
                                           value=0,
                                           description="sharpness")
        snr_db_ui = widgets.FloatSlider(min=0,
                                        max=100,
                                        value=30.0,
                                        description="snr db")
        positivity_ui = widgets.Checkbox(value=True,
                                         description="positivity")
        max_iterations_ui = widgets.IntSlider(value=200,
                                              min=10,
                                              max=500,
                                              description="max itera.",
                                              layout=widgets.Layout(width="max-content"))
        verbose_ui = widgets.Checkbox(value=False,
                                      description='verbose')
        
        vertical_widgets = widgets.VBox([sharpness_ui,
                                         snr_db_ui,
                                         positivity_ui,
                                         max_iterations_ui,
                                         verbose_ui])
        display(vertical_widgets)
