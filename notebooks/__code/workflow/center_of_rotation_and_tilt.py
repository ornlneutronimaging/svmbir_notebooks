import numpy as np
import logging
from neutompy.preproc.preproc import find_COR, correction_COR
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets

# from imars3d.backend.diagnostics.rotation import find_rotation_center

from __code.parent import Parent
from __code import DataType, Run
from __code.utilities.logging import logging_3d_array_infos


class CenterOfRotationAndTilt(Parent):

    image_0_degree = None
    image_180_degree = None
    height = None

    display_plot = None

    def _isolate_0_and_180_degrees_images(self):
        list_of_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
        logging.info(f"\t{list_of_runs_to_use = }")
        list_of_angles = np.array([self.parent.list_of_runs[DataType.sample][_key][Run.angle] for _key in list_of_runs_to_use])
        self.parent.final_list_of_angles = list_of_angles

        angles_minus_180 = [float(_value) - 180 for _value in list_of_angles]
        abs_angles_minus_180 = np.abs(angles_minus_180)
        minimum_value = np.min(abs_angles_minus_180)

        index_0_degree = 0
        index_180_degree = np.where(minimum_value == abs_angles_minus_180)[0][0]
        logging.info(f"\t{index_0_degree = }")
        logging.info(f"\t{index_180_degree = }")

        # retrieve data for those indexes
        self.image_0_degree = self.parent.corrected_images[index_0_degree]
        self.image_180_degree = self.parent.corrected_images[index_180_degree]

        self.height, _ = np.shape(self.image_0_degree)

    def select_range(self):
        self._isolate_0_and_180_degrees_images()

        def plot_range(y_top, y_bottom):
            _, axs = plt.subplots(nrows=1, ncols=2, figsize=(10,5))

            axs[0].imshow(self.image_0_degree, vmin=0, vmax=1)
            axs[0].set_title("0 degree")
            axs[0].axhspan(y_top, y_bottom, color='blue', alpha=0.2)

            axs[1].imshow(self.image_180_degree, vmin=0, vmax=1)
            axs[1].set_title("180 degree")
            axs[1].axhspan(y_top, y_bottom, color='blue', alpha=0.2)

            plt.tight_layout()
            plt.show()

            return y_top, y_bottom

        self.display_plot = interactive(plot_range,
                                   y_top = widgets.IntSlider(min=0, 
                                                            max=self.height-1, 
                                                            value=0),
                                   y_bottom = widgets.IntSlider(min=0,
                                                            max=self.height-1, 
                                                            value=self.height-1)
        )

        display(self.display_plot)

    def run(self):
        self.calculate_using_neutompy()

    def calculate_using_neutompy(self):
        
        # retrieve index of 0 and 180degrees runs
        logging.info(f"calculate center of rotation:")

        logging_3d_array_infos(message="before", array=self.parent.corrected_images)

        y_top, y_bottom = self.display_plot.result
        mid_point = int(np.mean([y_top, y_bottom]))
        rois = ((y_top, mid_point+1), (mid_point, y_bottom))

        corrected_images = correction_COR(self.parent.corrected_images,
                       self.image_0_degree,
                       self.image_180_degree,
                       rois=rois)
        logging.info(f"{np.shape(corrected_images) =}")
        self.parent.corrected_images = corrected_images

        logging_3d_array_infos(message="after", array=self.parent.corrected_images)
