class DataType:
    sample = 'sample'
    ob = 'ob'
    dc = 'dc'
    ipts = 'ipts'
    top = 'top'
    nexus = 'nexus'
    cleaned_images = 'cleaned images'
    normalized = 'normalized'
    reconstructed = 'reconstructed'
    extra = 'extra'
    processed = "processed"


class OperatingMode:
    tof = 'tof'
    white_beam = 'white_beam'


STEP3_SVMBIR_SCRIPTS = "/SNS/VENUS/shared/software/git/svmbir_notebooks/notebooks/step3_reconstruction_white_beam_mode_images_using_svmbir.py"
STEP3_FPB_SCRIPTS = "/SNS/VENUS/shared/software/git/svmbir_notebooks/notebooks/step3_reconstruction_white_beam_mode_images_using_fbp.py"


DEFAULT_OPERATING_MODE = OperatingMode.white_beam
DEFAULT_RECONSTRUCTION_ALGORITHM = "fbp"
NBR_TOF_RANGES = 3


DEBUG = False
debug_folder = {OperatingMode.tof: {DataType.sample: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance",
                                    DataType.ob: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September26_2024_PurpleCar_OpenBean_5_0_C_Cd_inBeam_Resonance",
                                    DataType.cleaned_images: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.normalized: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.reconstructed: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.extra: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    },
                OperatingMode.white_beam: {DataType.sample: "/SNS/VENUS/IPTS-33531/shared/processed_data/November8_2024_PlantE/",
                                            DataType.ob: "/SNS/VENUS/IPTS-33531/shared/processed_data/ob_PlantE/",
                                            DataType.dc: "",
                                            DataType.cleaned_images: '/SNS/VENUS/IPTS-33531/shared/processed_data/jean_test',
                                            DataType.normalized: '/SNS/VENUS/IPTS-33531/shared/processed_data/jean_test',
                                            DataType.reconstructed: '/SNS/VENUS/IPTS-33531/shared/processed_data/jean_test',
                                            DataType.extra: '/SNS/VENUS/IPTS-33531/shared/processed_data/jean_test',
                                            },
                # OperatingMode.white_beam: {DataType.sample: "/HFIR/CG1D/IPTS-25777/raw/ct_scans/iron_man",
                #                             DataType.ob: "/HFIR/CG1D/IPTS-25777/raw/ob/Oct29_2019",
                #                             DataType.dc: "/HFIR/CG1D/IPTS-25777/raw/dc/2023_05_24",
                #                             DataType.cleaned_images: '/HFIR/CG1D/IPTS-25777/shared/processed_data/jean_test',
                #                             DataType.normalized: '/HFIR/CG1D/IPTS-25777/shared/processed_data/jean_test',
                #                             DataType.reconstructed: '/HFIR/CG1D/IPTS-25777/shared/processed_data/jean_test',
                #                             DataType.extra: '/HFIR/CG1D/IPTS-25777/shared/processed_data/jean_test',
                #                             },
}

roi = {OperatingMode.tof: {'left': 0,
                            'right': 74,
                            'top': 0,
                            'bottom': 49},
        OperatingMode.white_beam: {'left': 0,
                                   'right': 549,
                                   'top': 131,
                                   'bottom': 8177},
                                   }
crop_roi = {OperatingMode.tof: {'left': 0,
                            'right': 74,
                            'top': 0,
                            'bottom': 49},
        OperatingMode.white_beam: {'left': 755,
                                   'right': 1306,
                                   'top': 881,
                                   'bottom': 1315},
                                   }

ANGSTROMS = u"\u212b"
LAMBDA = u"\u03bb"


class Run:
    full_path = 'full path'
    proton_charge_c = 'proton charge c'
    use_it = 'use it'
    angle = 'angle'
    frame_number = 'number of frames'
    nexus = 'nexus'


class CleaningAlgorithm:
    histogram = 'histogram'
    threshold = 'threshold'


class NormalizationSettings:
    pc = 'proton charge'
    frame_number = 'frame number'
    roi = 'roi'
    sample_roi = 'roi_sample'


class RemoveStripeAlgo:
    remove_stripe_fw = "remove_stripe_fw"
    remove_stripe_ti = "remove_stripe_ti"
    remove_stripe_sf = "remove_stripe_sf"
    remove_stripe_based_sorting = "remove_stripe_based_sorting"
    remove_stripe_based_filtering = "remove_stripe_based_filtering"
    remove_stripe_based_fitting = "remove_stripe_based_fitting"
    remove_large_stripe = "remove_large_stripe"
    remove_all_stripe = "remove_all_stripe"
    remove_dead_stripe = "remove_dead_stripe"
    remove_stripe_based_interpolation = "remove_stripe_based_interpolation"
