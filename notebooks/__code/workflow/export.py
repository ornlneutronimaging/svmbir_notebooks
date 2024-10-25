from tqdm import tqdm
import os
import logging
import shutil

from __code.utilities.save import make_tiff
from __code.utilities.json import save_json
from __code.parent import Parent
from __code import DataType
from __code.utilities.time import get_current_time_in_special_file_name_format


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

        configuration = self.parent.configuration
        base_sample_folder = os.path.basename(self.parent.working_dir[DataType.sample])
        _time_ext = get_current_time_in_special_file_name_format()
        config_file_name = f"/SNS/VENUS/shared/log/{base_sample_folder}_{_time_ext}.json"
        config_json = configuration.model_dump_json()
        save_json(config_file_name, json_dictionary=config_json)
        print(f"\t\tconfig file {config_file_name}")
