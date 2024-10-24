class DataType:
    sample = 'sample'
    ob = 'ob'
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
debug_folder = {DataType.sample: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance",
                DataType.ob: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September26_2024_PurpleCar_OpenBean_5_0_C_Cd_inBeam_Resonance",
                DataType.cleaned_images: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.normalized: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.reconstructed: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.extra: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
}
# debug_folder = {DataType.sample: "/HFIR/CG1D/IPTS-32519/raw/ct_scans/2024_10_18_fossil_60s/",
#                 DataType.ob: "/HFIR/CG1D/IPTS-32519/raw/ob/2024_10_18_fossil_60s/",
#                 DataType.cleaned_images: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
#                 DataType.normalized: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
#                 DataType.reconstructed: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
#                 DataType.extra: '/HFIR/CG1D/IPTS-32519/shared/processed_data/jean_test',
# }


roi = {'left': 0,
       'right': 74,
       'top': 0,
       'bottom': 49}

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
