from tqdm import tqdm
import os
import logging
import shutil

from __code.utilities.save import make_tiff
from __code.parent import Parent
from __code import DataType


class Export:

    base_image_name = "image"

    def __init__(self, image_3d=None, output_folder=None):
        self.image_3d = image_3d
        self.output_folder = output_folder

    def run(self):
       
        for _index, _data in tqdm(enumerate(self.image_3d)):
            short_file_name = f"{self.base_image_name}_{_index:04d}.tiff"
            full_file_name = os.path.join(self.output_folder, short_file_name)
            logging.info(f"\texporting {full_file_name}")
            make_tiff(data=_data, filename=full_file_name)


class ExportExtra(Parent):

    def run(self, base_log_file_name=None):
        print(f"Files exported:")
        log_file_name = f"/SNS/VENUS/shared/log/{base_log_file_name}.log"
        output_folder = self.parent.working_dir[DataType.extra]
        shutil.copy(log_file_name, output_folder)
        print(f"\tlog file from {log_file_name} to {output_folder}!")
