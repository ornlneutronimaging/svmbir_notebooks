import os
import logging
from collections import OrderedDict

from __code import DataType
from __code.utilities.logging import setup_logging

from __code.workflow.load import Load
from __code.workflow.checking_data import CheckingData
from __code.workflow.recap_data import RecapData
from __code.workflow.combine import Combine
from __code.workflow.images_cleaner import ImagesCleaner
from __code.workflow.normalization import Normalization


class WhiteBeam:

    working_dir = {
        DataType.sample: "",
        DataType.ob: "",
        DataType.nexus: "",
        DataType.cleaned_images: "",
        }
    
    # will record short_run_number and pc
    # will look like
    # {DataType.sample: {'Run_1234': {Run.full_path: "/SNS/VENUS/.../Run_1344",
    #                                 Run.proton_charge: 5.01,
    #                                 Ru.use_it: True,
    #                                },
    #                    ...,
    #                   },
    # DataType.ob: {...},
    # }
    list_of_runs = {DataType.sample: OrderedDict(),
                    DataType.ob: OrderedDict(),
                    }
    
    list_of_runs_checking_data = {DataType.sample: {},
                                   DataType.ob: {},
                                  }

    list_proton_charge_c = {DataType.sample: {},
                            DataType.ob: {},
                           }

    final_list_of_runs = {DataType.sample: {},
                          DataType.ob: {},
                          }

    master_3d_data_array = {DataType.sample: None,  # [angle, y, x]
                            DataType.ob: None}

    master_3d_data_array_cleaned = {DataType.sample: None,  # [angle, y, x]
                                    DataType.ob: None}

    normalized_data = None

    instrument = "VENUS"

    selection_of_pc = None   # plot that allows the user to select the pc for sample and ob and threshold

    list_of_sample_runs_to_reject_ui = None
    list_of_ob_runs_to_reject_ui = None
    minimum_requirements_met = False

    # created during the combine step to match data index with run number (for normalization)
    list_of_runs_used = {DataType.sample: [],
                         DataType.ob:[]}

    def __init__(self, system=None):

        top_sample_dir = system.System.get_working_dir()
        self.instrument = system.System.get_instrument_selected()

        setup_logging(basename_of_log_file="svmbir_white_beam")        
        self.working_dir[DataType.ipts] = os.path.basename(top_sample_dir)
        self.working_dir[DataType.top] = os.path.join(top_sample_dir, "shared", "autoreduce", "mcp")
        self.working_dir[DataType.nexus] = os.path.join(top_sample_dir, "nexus")
        logging.info(f"working_dir: {self.working_dir}")
        logging.info(f"instrument: {self.instrument}")

    # Selection of data
    def select_top_sample_folder(self):
        o_load = Load(parent=self)
        o_load.select_folder(data_type=DataType.sample)

    def select_top_ob_folder(self):
        o_load = Load(parent=self)
        o_load.select_folder(data_type=DataType.ob)

    # Checking data (proton charge, empty runs ...)
    def checking_data(self):
        try:
            o_checking = CheckingData(parent=self)
            o_checking.run()
        except ValueError:
            logging.info("Check the input folders provided !")

    def recap_data(self):
        o_recap = RecapData(parent=self)
        o_recap.run()

    def checkin_data_entries(self):
        o_check = CheckingData(parent=self)
        o_check.checking_minimum_requirements()

    # combine images
    def combine_images(self):
        o_check = CheckingData(parent=self)
        o_check.checking_minimum_requirements()
        if self.minimum_requirements_met:
            o_combine = Combine(parent=self)
            o_combine.run()
        else:
            o_check.minimum_requirement_not_met()

    # cleaning low/high pixels
    def clean_images_setup(self):
        o_clean = ImagesCleaner(parent=self)
        o_clean.cleaning_setup()

    def clean_images(self):
        o_clean = ImagesCleaner(parent=self)
        o_clean.cleaning()

    def select_export_folder(self):
        o_clean = ImagesCleaner(parent=self)
        o_clean.select_export_folder()

    def export_cleaned_images(self):
        o_clean = ImagesCleaner(parent=self)
        o_clean.export_clean_images()

    # normalization
    def normalization(self):
        o_norm = Normalization(parent=self)
        o_norm.run()
