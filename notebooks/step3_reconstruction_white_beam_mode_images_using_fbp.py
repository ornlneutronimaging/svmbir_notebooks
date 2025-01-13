import argparse
import logging
import os

from __code.utilities.logging import setup_logging
from __code.workflow_cli.fbp_white_beam import  FbpCliHandler

# this requires to activate first the hsnt conda environment
# ----------------------------------------------------------
# source /opt/anaconda/etc/profile.d/conda.sh
# conda activate hsnt
# ----------------------------------------------------------

file_name, ext = os.path.splitext(os.path.basename(__file__))
setup_logging(file_name)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the FBP in white beam mode")
    parser.add_argument('config_json_file', type=str, nargs=1, help="JSON config file created by notebook in pre-reduction step")
    # parser.add_argument('input_folder', type=str, nargs=1, help='location of pre-reconstructed projections')
    # parser.add_argument('output_folder', type=str, nargs=1, help='output folder')
    args = parser.parse_args()

    config_json_file = args.config_json_file[0]

    logging.info(f"about to call FbpCliHandler.run_reconstruction_from_pre_data_mode:")
    logging.info(f"\t{config_json_file = }")

    FbpCliHandler.run_reconstruction_from_pre_data_mode(config_json_file=config_json_file)

    print(f"FBP reconstruction is done and report can be found in /SNS/VENUS/shared/log/{file_name}.log!")
    logging.info(f"full reconstruction is done!")
    