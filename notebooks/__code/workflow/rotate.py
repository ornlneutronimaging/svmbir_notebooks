import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML
from ipywidgets import interactive
from tqdm import tqdm
import numpy as np
from skimage import transform
import multiprocessing as mp 

from __code.parent import Parent


def _worker(_data, angle_value):
    data = transform.rotate(_data, angle_value)
    print(f"{np.shape(data) = }")
    print(f"{data = }")
    return data


class Rotate(Parent):

    def set_settings(self):

        title_ui = widgets.HTML("Select rotation angle (counter-clockwise)")
        self.angle_ui = widgets.RadioButtons(options=['-90 degrees', '0 degree', '+90 degrees'],
                                             value='-90 degrees',
                                            description='Angle')
        
        vbox = widgets.VBox([title_ui, self.angle_ui])
        display(vbox)

    def _worker(self, _data, angle_value):
        data = transform.rotate(_data, angle_value)
        print(f"{np.shape(data) = }")
        print(f"{data = }")
        return data

    def apply_rotation(self):

        str_angle_value = self.angle_ui.value
        if str_angle_value == '-90 degrees':
            angle_value = -90
        elif str_angle_value == '0 degree':
            angle_value = 0
        else:
            angle_value = +90
        
        # with mp.Pool(processes=5) as pool:
        #     self.parent.normalized_images = pool.map(_worker, list(self.parent.normalized_images), angle_value)
    
        new_array_rotated = []
        for _data in tqdm(self.parent.normalized_images):
            new_array_rotated.append(transform.rotate(_data, angle_value))

        self.parent.normalized_images = np.array(new_array_rotated)

    