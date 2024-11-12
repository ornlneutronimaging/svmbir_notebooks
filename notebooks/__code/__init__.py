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


DEFAULT_OPERATING_MODE = OperatingMode.tof
NBR_TOF_RANGES = 3

DEBUG = True
debug_folder = {OperatingMode.tof: {DataType.sample: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance",
                                    DataType.ob: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September26_2024_PurpleCar_OpenBean_5_0_C_Cd_inBeam_Resonance",
                                    DataType.cleaned_images: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.normalized: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.reconstructed: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    DataType.extra: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                                    },
                OperatingMode.white_beam: {DataType.sample: "/HFIR/CG1D/IPTS-32720/raw/ct_scans/2024_10_30_anodefree/",
                                            DataType.ob: "/HFIR/CG1D/IPTS-32720/raw/ob/2024_10_30_anodefree/",
                                            DataType.dc: "",
                                            DataType.cleaned_images: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
                                            DataType.normalized: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
                                            DataType.reconstructed: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
                                            DataType.extra: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
                                            },
}

roi = {OperatingMode.tof: {'left': 0,
                            'right': 74,
                            'top': 0,
                            'bottom': 49},
        OperatingMode.white_beam: {'left': 750,
                                   'right': 5372,
                                   'top': 3798,
                                   'bottom': 5096},
                                   }
crop_roi = {OperatingMode.tof: {'left': 0,
                            'right': 74,
                            'top': 0,
                            'bottom': 49},
        OperatingMode.white_beam: {'left': 2549,
                                   'right': 5072,
                                   'top': 549,
                                   'bottom': 5496},
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
