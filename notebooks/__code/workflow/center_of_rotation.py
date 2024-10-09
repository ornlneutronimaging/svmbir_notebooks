import numpy as np
import logging
from neutompy.preproc.preproc import find_COR
import matplotlib.pyplot as plt
from ipywidgets import interactive
from IPython.display import display
import ipywidgets as widgets

# from imars3d.backend.diagnostics.rotation import find_rotation_center

from __code.parent import Parent
from __code import DataType, Run


class CenterOfRotation(Parent):

    image_0_degree = None
    image_180_degree = None
    height = None

    def _isolate_0_and_180_degrees_images(self):
        list_of_runs_used = self.parent.list_of_runs_used[DataType.sample]
        logging.info(f"\t{list_of_runs_used = }")
        list_of_angles = np.array([self.parent.list_of_runs[DataType.sample][_key][Run.angle] for _key in list_of_runs_used])

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

        display_plot = interactive(plot_range,
                                   y_top = widgets.IntSlider(min=0, 
                                                            max=self.height-1, 
                                                            value=0),
                                   y_bottom = widgets.IntSlider(min=0,
                                                            max=self.height-1, 
                                                            value=self.height-1)
        )

        display(display_plot)

    def run(self):
        self.calculate_using_neutompy()
        #self.calculate_using_imars3d()

    # def calculate_using_imars3d(self):
    #     corrected_images = self.parent.corrected_images
    #     list_of_runs_used = self.parent.list_of_runs_used[DataType.sample]
    #     list_of_angles = [self.parent.list_of_runs[DataType.sample][_key][Run.angle] for _key in list_of_runs_used]
    #     list_of_angles = np.array([float(_value) for _value in list_of_angles])
    #     mean_delta_angle = np.mean([y - x for (x, y) in zip(list_of_angles[:-1], list_of_angles[1:])])

    #     rotation_center = find_rotation_center(arrays=corrected_images,
    #                                            angles=list_of_angles,
    #                                            num_pairs=1,
    #                                            in_degrees=True,
    #                                            atol_deg=mean_delta_angle)
    #     logging.info(f"calculated rotation center: {rotation_center}")

    def calculate_using_neutompy(self):
        
        # retrieve index of 0 and 180degrees runs
        logging.info(f"calculate center of rotation:")

        list_of_runs_used = self.parent.list_of_runs_used[DataType.sample]
        logging.info(f"\t{list_of_runs_used = }")
        list_of_angles = np.array([self.parent.list_of_runs[DataType.sample][_key][Run.angle] for _key in list_of_runs_used])

        angles_minus_180 = [float(_value) - 180 for _value in list_of_angles]
        abs_angles_minus_180 = np.abs(angles_minus_180)
        minimum_value = np.min(abs_angles_minus_180)

        index_0_degree = 0
        index_180_degree = np.where(minimum_value == abs_angles_minus_180)[0][0]
        logging.info(f"\t{index_0_degree = }")
        logging.info(f"\t{index_180_degree = }")

        # retrieve data for those indexes
        image_0_degree = self.parent.corrected_images[index_0_degree]
        image_180_degree = self.parent.corrected_images[index_180_degree]

        # run neutompy
        # np.nan_to_num(image_0_degree, nan=0.0, posinf=1, neginf=0)
        # np.nan_to_num(image_180_degree, nan=0.0, posinf=1, neginf=0)    
        result = find_COR(image_0_degree, image_180_degree, nroi=5, ShowResults=False, rois=((0, 250), (251, 500)))
        logging.info(f"\t{result = }")
