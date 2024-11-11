import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML
from ipywidgets import interactive
from tqdm import tqdm
from skimage import transform

from __code.parent import Parent


class Rotate(Parent):

    def set_settings(self):

        title_ui = widgets.HTML("Select rotation angle (counter-clockwise)")
        self.angle_ui = widgets.IntSlider(value=0,
                                     min=-90,
                                     max=90,
                                     step=90,
                                     description='Angle')
        
        vbox = widgets.VBox([title_ui, self.angle_ui])
        display(vbox)

    def apply_rotation(self):

        angle_value = self.angle_ui.value

        if angle_value == 0:
            return
        
        new_array_rotated = []
        for _data in tqdm(self.parent.normalized_images):
            new_array_rotated.append(transform.rotate(_data, angle_value))

        self.parent.normalized_images = new_array_rotated
