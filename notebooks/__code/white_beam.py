import os
import logging

from __code import DataType
from __code.workflow.load import Load
from __code.utilities.logging import setup_logging


class WhiteBeam:

    working_dir = {
        DataType.sample: "",
        DataType.ob: "",
        }

    def __init__(self, top_sample_dir="./"):
        setup_logging(basename_of_log_file="svmbir_white_beam")        
        self.working_dir[DataType.ipts] = os.path.basename(top_sample_dir)
        self.working_dir[DataType.top] = os.path.join(top_sample_dir, "shared", "autoreduce", "mcp")
        logging.info(f"{self.working_dir =}")

    def select_top_sample_folder(self):
        o_load = Load(parent=self)
        o_load.select_folder(data_type=DataType.sample)

    def select_top_ob_folder(self):
        o_load = Load(parent=self)
        o_load.select_folder(data_type=DataType.ob)
