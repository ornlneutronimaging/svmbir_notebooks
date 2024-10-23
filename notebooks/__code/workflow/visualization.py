from IPython.display import display
import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interactive
import numpy as np

from __code.parent import Parent
from __code import DataType
from __code.workflow.final_projections_review import FinalProjectionsReview


class Visualization(Parent):

    def settings(self):
        self.display_ui = widgets.ToggleButtons(options=['1 image at a time',
                                                         'All images'],
                                                         description="How to plot?",
                                                         )
        display(self.display_ui)

    def visualize(self, data_before=None, data_after=None, label_before="", label_after="", turn_on_vrange=False):

        if self.display_ui.value == '1 image at a time':

            list_of_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
            
            if turn_on_vrange:

                vmin_before = np.min(data_before)
                vmax_before = np.max(data_before)
                vmin_after = np.min(data_after)
                vmax_after = np.max(data_after)

                def plot_norm(image_index=0, 
                              vmin_before=vmin_before, vmax_before=vmax_before, 
                              vmin_after=vmin_after, vmax_after=vmax_after):

                    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

                    _norm_data = data_after[image_index]
                    _run_number = list_of_runs_to_use[image_index]
                    _raw_data = data_before[image_index]

                    im0 = axs[0].imshow(_raw_data, vmin=vmin_before, vmax=vmax_before)
                    axs[0].set_title(label_before)
                    plt.colorbar(im0, ax=axs[0], shrink=0.5)

                    im1 = axs[1].imshow(_norm_data, vmin=vmin_after, vmax=vmax_after)
                    axs[1].set_title(label_after)
                    plt.colorbar(im1, ax=axs[1], shrink=0.5)
            
                    # fig.set_title(f"{_run_number}")
                    
                    plt.tight_layout()
                    plt.show()

                display_plot = interactive(plot_norm,
                                        image_index=widgets.IntSlider(min=0,
                                                                        max=len(list_of_runs_to_use)-1,
                                                                        value=0),
                                        vmin_before=widgets.IntSlider(min=vmin_before, max=vmax_before, value=vmin_before),
                                        vmax_before=widgets.IntSlider(min=vmin_before, max=vmax_before, value=vmax_before),
                                        vmin_after=widgets.IntSlider(min=vmin_after, max=vmax_after, value=vmin_after),
                                        vmax_after=widgets.IntSlider(min=vmin_after, max=vmax_after, value=vmax_after))

            else:

                def plot_norm(image_index=0):

                    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

                    _norm_data = data_after[image_index]
                    _run_number = list_of_runs_to_use[image_index]
                    _raw_data = data_before[image_index]

                    im0 = axs[0].imshow(_raw_data)
                    axs[0].set_title(label_before)
                    plt.colorbar(im0, ax=axs[0], shrink=0.5)

                    im1 = axs[1].imshow(_norm_data)
                    axs[1].set_title(label_after)
                    plt.colorbar(im1, ax=axs[1], shrink=0.5)
            
                    # fig.set_title(f"{_run_number}")
                    
                    plt.tight_layout()
                    plt.show()

                display_plot = interactive(plot_norm,
                                        image_index=widgets.IntSlider(min=0,
                                                                        max=len(list_of_runs_to_use)-1,
                                                                        value=0),
                )
                
            display(display_plot)


        else:
            o_review = FinalProjectionsReview(parent=self.parent)
            o_review.run(array=data_after)
