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


DEBUG = False
debug_folder = {DataType.sample: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September20_2024_PurpleCar_GoldenRatio_CT_5_0_C_Cd_inBeam_Resonance",
                DataType.ob: "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/September26_2024_PurpleCar_OpenBean_5_0_C_Cd_inBeam_Resonance",
                DataType.cleaned_images: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.normalized: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.reconstructed: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
                DataType.extra: '/SNS/VENUS/IPTS-33699/shared/processed_data/jean_test',
}
roi = {'left': 0,
       'right': 74,
       'top': 0,
       'bottom': 49}


class Run:
    full_path = 'short run number'
    proton_charge_c = 'proton charge c'
    use_it = 'use it'
    angle = 'angle'
    frame_number = 'number of frames'
    nexus = ''
