import numpy as np
import logging
from neutompy.preproc.preproc import find_COR

# from imars3d.backend.diagnostics.rotation import find_rotation_center

from __code.parent import Parent
from __code import DataType, Run


class CenterOfRotation(Parent):

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
        list_of_angles = [self.parent.list_of_runs[DataType][_key][Run.angle] for _key in list_of_runs_used]

        angles_minus_180 = list_of_angles - 180.0
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
        result = find_COR(image_0_degree, image_180_degree)
        logging.info(f"\t{result = }")
