import argparse
import logging

from __code.utilities.logging import setup_logging
from __code.workflow_cli.svmbir_white_beam import  SvmbirCliHandler


setup_logging("svmbir_white_beam_cli")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the full svmbir in white beam mode")
    parser.add_argument('config_json_file', type=str, nargs=1, help="JSON config file created by notebook in pre-reduction step")
    # parser.add_argument('input_folder', type=str, nargs=1, help='location of pre-reconstructed projections')
    # parser.add_argument('output_folder', type=str, nargs=1, help='output folder')
    args = parser.parse_args()

    config_json_file = args.config_json_file[0]

    logging.info(f"about to call SvmbirCliHandler.run_reconstruction_from_pre_data_mode:")
    logging.info(f"\t{config_json_file = }")

    SvmbirCliHandler.run_reconstruction_from_pre_data_mode(config_json_file=config_json_file)

    print("svmbir reconstruction is done and report can be found in /SNS/VENUS/shared/log/svmbir_white_beam_cli.log!")
    logging.info(f"full reconstruction is done!")
    