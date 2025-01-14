import logging
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ipywidgets import interactive
from IPython.display import display
from IPython.core.display import HTML
import ipywidgets as widgets
from scipy.ndimage import median_filter

from __code.parent import Parent
from __code import DEBUG, roi
from __code import Run, DataType, NormalizationSettings
from __code.workflow.load import Load
from __code.workflow.export import Export
from __code.utilities.files import make_or_reset_folder
from __code.utilities.logging import logging_3d_array_infos
from __code.workflow.final_projections_review import FinalProjectionsReview


class RectangleSelector:
   def __init__(self, ax):
      self.ax = ax
      self.start_point = None
      self.rect = None
      self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
      self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
      self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
   def on_press(self, event):
      if event.inaxes == self.ax:
         self.start_point = (event.xdata, event.ydata)
         self.rect = Rectangle(self.start_point, 0, 0, edgecolor='red', alpha=0.2)
         self.ax.add_patch(self.rect)
   def on_motion(self, event):
      if self.start_point is not None and event.inaxes == self.ax:
         width = event.xdata - self.start_point[0]
         height = event.ydata - self.start_point[1]
         self.rect.set_width(width)
         self.rect.set_height(height)
         self.ax.figure.canvas.draw()
   def on_release(self, event):
      if self.start_point is not None:
         # Determine the data points within the rectangle and perform actions as needed
         selected_data = self.get_data_within_rectangle()
         print("Selected Data:", selected_data)
         self.start_point = None
         self.rect.remove()
         self.ax.figure.canvas.draw()
   def get_data_within_rectangle(self):
      # Placeholder function to determine data points within the rectangle
      # Implement logic to identify data points based on the rectangle's coordinates
      return [(1, 2), (3, 4)]  # Example data points
   

class Normalization(Parent):

    obs_combined = None
    mean_ob_proton_charge = None
    mean_ob_frame_number = 1

    enable_frame_number = False

    def normalization_settings(self):

        self.use_proton_charge_ui = widgets.Checkbox(value=True,
                                                description='Use proton charge',
                                                disabled=True)
        self.use_frames_ui = widgets.Checkbox(value=False,
                                         description='Use frames',
                                         disabled=True,
                                         )
        self.use_roi_ui = widgets.Checkbox(value=True,
                                      description='Use ROI')
        vertical_layout = widgets.VBox([self.use_proton_charge_ui,
                                        self.use_frames_ui,
                                        self.use_roi_ui])
        display(vertical_layout)

    def select_roi(self):

        if not self.use_roi_ui.value:
            logging.info(f"User skipped normalization ROI selection.")
            return

        display(HTML("Note: This is an integrated view of the projections allowing you to see the contours of all the angles!"))

        # integrated_images = np.log(np.min(self.parent.master_3d_data_array[DataType.sample], axis=0))
        sample_images = self.parent.master_3d_data_array[DataType.sample]
        integrated_images = np.min(sample_images, axis=0)

        height = self.parent.image_size['height']
        width = self.parent.image_size['width']

        def plot_roi(left, right, top, bottom):

            height = np.abs(bottom - top) + 1
            width = np.abs(right - left) + 1

            fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
            im1 = axs.imshow(integrated_images)
            plt.colorbar(im1, ax=axs, shrink=0.8)

            axs.add_patch(Rectangle((left, top), width, height,
                                        edgecolor='yellow',
                                        facecolor='green',
                                        fill=True,
                                        lw=2,
                                        alpha=0.3,
                                        ),
            )     

            return left, right, top, bottom                       
    
        if DEBUG:
            default_left = roi[self.MODE]['left']
            default_right = roi[self.MODE]['right']
            default_top = roi[self.MODE]['top']
            defualt_bottom = roi[self.MODE]['bottom']
        else:
            default_left = default_top = 0
            default_right = defualt_bottom = 20

        self.display_roi = interactive(plot_roi,
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
                                                                 value=defualt_bottom),
                                        )
        display(self.display_roi)

    def run(self):
        self.normalize()

    # def combine_obs(self):
        
    #     logging.info(f"Combine obs:")
    #     list_obs = self.parent.master_3d_data_array_cleaned[DataType.ob]
    #     if len(list_obs) == 1:
    #         self.obs_combined = np.array(list_obs[0])
    #         logging.info(f"\tonly 1 ob, nothing to combine!")
    #     else:
    #         self.obs_combined = np.mean(list_obs, axis=0)
    #         logging.info(f"\tcombining {len(list_obs)} obs.")
        
    #     temp_obs_combined = median_filter(self.obs_combined, size=2)
    #     index_of_zero = np.where(self.obs_combined == 0)
    #     self.obs_combined[index_of_zero] = temp_obs_combined[index_of_zero]

    #     logging_3d_array_infos(message="obs", array=self.obs_combined)

    #     list_proton_charge = []
    #     for _run in self.parent.list_of_runs_to_use[DataType.ob]:
    #         list_proton_charge.append(self.parent.list_of_runs[DataType.ob][_run][Run.proton_charge_c])

    #     self.mean_ob_proton_charge = np.mean(list_proton_charge)
    #     logging.info(f"\tcalculated combined ob proton charge: {self.mean_ob_proton_charge}")

    #     use_frame = self.use_frames_ui.value
    #     if use_frame:
    #         list_frame = []
    #         for _run in self.parent.list_of_runs_to_use[DataType.ob]:
    #             frame_number = self.parent.list_of_runs[DataType.ob][_run][Run.frame_number]
    #             if frame_number:
    #                 list_frame.append(frame_number)
    #             else:
    #                 self.mean_ob_frame_number = 1
    #         mean_frame_number = np.mean(np.array(list_frame))
    #         self.mean_ob_frame_number = mean_frame_number
    
    def normalize(self):
        master_3d_data = self.parent.master_3d_data_array
        normalized_data = []

        list_proton_charge = {DataType.sample: [],
                              DataType.ob: [],
                             }

        logging.info(f"Normalization:")
        # logging_3d_array_infos(array=self.mean_ob_proton_charge, message="mean_ob_proton_charge")

        # use_proton_charge = self.use_proton_charge_ui.value
        # use_frame = self.use_frames_ui.value
        use_roi = self.use_roi_ui.value

        logging.info(f"\tnormalization settings:")
        # logging.info(f"\t\t- use proton charge: {use_proton_charge}")
        # logging.info(f"\t\t- use_frame: {use_frame}")
        logging.info(f"\t\t- use_roi: {use_roi}")

        if use_roi:
            left, right, top, bottom = self.display_roi.result
            self.parent.configuration.normalization_roi.top = top
            self.parent.configuration.normalization_roi.bottom = bottom
            self.parent.configuration.normalization_roi.left = left
            self.parent.configuration.normalization_roi.right = right

        # update configuration
        list_norm_settings = []
        # if use_proton_charge:
        #     list_norm_settings.append(NormalizationSettings.pc)
        # if use_frame:
        #     list_norm_settings.append(NormalizationSettings.frame_number)
        if use_roi:
            list_norm_settings.append(NormalizationSettings.roi)
        self.parent.configuration.list_normalization_settings = list_norm_settings

        ob_data_combined = self.parent.master_3d_data_array[DataType.ob]
        dc_data_combined = None if (self.parent.list_of_images[DataType.dc] is None) else self.parent.master_3d_data_array[DataType.dc]

        for _index, sample_data in enumerate(self.parent.master_3d_data_array[DataType.sample]):

            # sample_proton_charge = self.parent.list_of_runs[DataType.sample][_run][Run.proton_charge_c]
            # angle = self.parent.list_of_runs[DataType.sample][_run][Run.angle]
            # final_list_of_angles.append(angle)
            # list_proton_charge[DataType.sample].append(sample_proton_charge)
            # logging.info(f"\t{_run} has a proton charge of {sample_proton_charge} and angle of {angle}")
            
            sample_data = np.array(master_3d_data[DataType.sample][_index])

            coeff = 1
            # if use_proton_charge:
            #     coeff *= self.mean_ob_proton_charge / sample_proton_charge

            # if use_frame:
            #     _sample_frame = self.parent.list_of_runs[DataType.sample][_run][Run.frame_number]
            #     coeff *= self.mean_ob_frame_number / _sample_frame

            if use_roi:
                sample_roi_counts = np.sum(sample_data[top: bottom+1, left: right+1])
                ob_roi_counts = np.sum(ob_data_combined[top: bottom+1, left: right+1])
                coeff *= ob_roi_counts / sample_roi_counts

            logging_3d_array_infos(message="sample_data", array=sample_data)

            if not (dc_data_combined is None):
                num = np.subtract(sample_data, dc_data_combined)
                den = np.subtract(ob_data_combined, dc_data_combined)
                normalized_sample = np.divide(num, den) * coeff
            else:
                normalized_sample = np.divide(sample_data, ob_data_combined) * coeff

            logging_3d_array_infos(message="after normalization", array=normalized_sample)
            normalized_data.append(normalized_sample) 

        self.parent.normalized_images = normalized_data

    # def visualization_normalization_settings(self):
    #     self.display_ui = widgets.ToggleButtons(options=['1 image at a time',
    #                                                            'All images'],
    #                                                            description="How to plot?",
    #                                                            )
    #     display(self.display_ui)

    # def visualize_normalization(self):

    #     if self.display_ui.value == '1 image at a time':

    #         normalized_data = self.parent.normalized_images
    #         list_of_runs_to_use = self.parent.list_of_runs_to_use[DataType.sample]
    #         master_3d_sample_data = self.parent.master_3d_data_array_cleaned[DataType.sample]

    #         def plot_norm(image_index=0, vmin=0, vmax=1):

    #             fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    #             _norm_data = normalized_data[image_index]
    #             _run_number = list_of_runs_to_use[image_index]
    #             _raw_data = master_3d_sample_data[image_index]

    #             im0 = axs[0].imshow(_raw_data)
    #             axs[0].set_title("Raw data")
    #             plt.colorbar(im0, ax=axs[0], shrink=0.5)

    #             im1 = axs[1].imshow(_norm_data, vmin=vmin, vmax=vmax)
    #             axs[1].set_title('Normalized')
    #             plt.colorbar(im1, ax=axs[1], shrink=0.5)
        
    #             # fig.set_title(f"{_run_number}")
                
    #             plt.tight_layout()
    #             plt.show()

    #         display_plot = interactive(plot_norm,
    #                                 image_index=widgets.IntSlider(min=0,
    #                                                                 max=len(list_of_runs_to_use)-1,
    #                                                                 value=0),
    #                                 vmin=widgets.IntSlider(min=0, max=10, value=0),
    #                                 vmax=widgets.IntSlider(min=0, max=10, value=1))
    #         display(display_plot)

    #     else:
    #         o_review = FinalProjectionsReview(parent=self.parent)
    #         o_review.run(array=self.parent.normalized_images)

    def export_images(self):
        
        logging.info(f"Exporting the normalized images")
        logging.info(f"\tfolder selected: {self.parent.working_dir[DataType.normalized]}")

        normalized_data = self.parent.normalized_images

        master_base_folder_name = f"{os.path.basename(self.parent.working_dir[DataType.sample])}_normalized"
        full_output_folder = os.path.join(self.parent.working_dir[DataType.normalized],
                                          master_base_folder_name)

        make_or_reset_folder(full_output_folder)

        o_export = Export(image_3d=normalized_data,
                          output_folder=full_output_folder)
        o_export.run()
        logging.info(f"\texporting normalized images ... Done!")
