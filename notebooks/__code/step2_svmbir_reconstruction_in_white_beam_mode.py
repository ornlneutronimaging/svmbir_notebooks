import os
import logging

from __code import DEBUG, debug_folder, OperatingMode, DataType
from __code.utilities.configuration_file import Configuration, select_file
from __code.utilities.logging import setup_logging


class Step2SvmbirReconstructionInWhiteBeamMode:

    def __init__(self, system=None):

        self.configuration = Configuration()
        self.working_dir = system.System.get_working_dir()
        if DEBUG:
            self.working_dir = debug_folder[OperatingMode.white_beam][DataType.extra]

        self.instrument = system.System.get_instrument_selected()

        setup_logging(basename_of_log_file=os.path.basename(__file__).replace('.py', ''))      
        logging.info(f"working_dir: {self.working_dir}")
        logging.info(f"instrument: {self.instrument}")
        if DEBUG:
            logging.info(f"WARNING!!!! we are running using DEBUG mode!")

    def select_config_file(self):
        select_file(top_folder=self.working_dir,
                    next_function=self.load_config_file)

    def load_config_file(self, config_file_path):
        logging.info(f"configuration file loaded: {config_file_path}")
