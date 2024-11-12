import numpy as np
import logging
from neutompy.preproc.preproc import correction_COR
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets
from matplotlib.patches import Rectangle

from __code.parent import Parent
from __code import crop_roi as default_roi
from __code import OperatingMode


class Crop(Parent):

    def set_region(self):

        width = self.parent.image_size['width']
        height = self.parent.image_size['height']

        default_left = default_roi[OperatingMode.white_beam]['left']
        default_right = default_roi[OperatingMode.white_beam]['right']
        default_top = default_roi[OperatingMode.white_beam]['top']
        default_bottom = default_roi[OperatingMode.white_beam]['bottom'] 

        normalized_data = self.parent.corrected_images
        integrated = np.min(normalized_data, axis=0)

        max_value = np.max(integrated)

        def plot_crop(left, right, top, bottom, vmin, vmax):

            fig, axs = plt.subplots(figsize=(7,7))

            axs.imshow(integrated, vmin=vmin, vmax=vmax)

            width = right - left + 1
            height = bottom - top + 1

            axs.add_patch(Rectangle((left, top), width, height,
                                            edgecolor='yellow',
                                            facecolor='green',
                                            fill=True,
                                            lw=2,
                                            alpha=0.3,
                                            ),
                )     

            return left, right, top, bottom    
        
        self.display_roi = interactive(plot_crop,
                                       left=widgets.IntSlider(min=0,
                                                              max=width-1,
                                                              value=default_left),
                                        right=widgets.IntSlider(min=0,
                                                                max=width-1,
                                                                value=default_right),                      
                                        top=widgets.IntSlider(min=0,
                                                              max=height-1,
                                                              value=default_top),
                                        bottom=widgets.IntSlider(min=0,
                                                                 max=height-1,
                                                                 value=default_bottom),
                                        vmin=widgets.FloatSlider(min=0,
                                                                 max=max_value,
                                                                 value=0),
                                        vmax=widgets.FloatSlider(min=0,
                                                                 max=max_value,
                                                                 value=max_value),
                                        )
        display(self.display_roi)

    def run(self):
        left, right, top, bottom = self.display_roi.result
        self.parent.corrected_images = np.array([image[top: bottom+1, left: right+1] 
                                                 for image in self.parent.corrected_images])
        