from pydantic import BaseModel, Field
from typing import List

from __code.utilities.json import load_json_string
from __code import CleaningAlgorithm, NormalizationSettings, OperatingMode


class RemoveStripeFwWnameOptions:
    haar = 'haar'
    db5 = 'db5'
    sym5 = 'sym5'


class RemoveStripeDim:
    one = '1'
    two = '2'


class ImageSize(BaseModel):
    width: int = 512
    height: int = 512


class RemoveStripeFw(BaseModel):
    level: str = "None"
    wname: str = Field(default=RemoveStripeFwWnameOptions.haar)
    sigma: float = 2
    pad: bool = True


class RemoveStripeTi(BaseModel):
    nblock: int = 0
    alpha: float = 1.5


class RemoveStripeSf(BaseModel):
    size: int = 5


class RemoveStripeBasedSorting(BaseModel):
    size: str = "None"
    dim: str = Field(default=RemoveStripeDim.one)


class RemoveStripeBasedFiltering(BaseModel):
    sigma: float = 3
    size: str = "None"
    dim: str = Field(default=RemoveStripeDim.one)


class RemoveStripeBasedFitting(BaseModel):
    order: int = Field(default=3, ge=3, le=10)
    sigma: str = "5,20"


class RemoveLargeStripe(BaseModel):
    snr: float = 3
    size: int = 51
    drop_ratio: float = 0.1
    norm: bool = True


class RemoveDeadStripe(BaseModel):
    snr: float = 3
    size: int = 51
    norm: bool = True


class RemoveAllStripe(BaseModel):
    snr: float = 3
    la_size: int = 61
    sm_size: int = 21
    dim: str = Field(default=RemoveStripeDim.one)


class RemoveStripeBasedInterpolation(BaseModel):
    snr: float = 3
    size: int = 31
    drop_ratio: float = .1
    norm: bool = True


class HistogramCleaningSettings(BaseModel):
    nbr_bins: int = 10
    bins_to_exclude: int = 1


class TopFolder(BaseModel):
    sample: str = ""
    ob: str = ""


class NormalizationRoi(BaseModel):
    top: int = 0
    bottom: int = 1
    left: int = 0
    right: int = 1


class SvmbirConfig(BaseModel):
    sharpness: float = 0
    snr_db: float = 30.0
    positivity: bool = True
    max_iterations: int = 200
    verbose: bool = False
    top_slice: int = 0
    bottom_slice: int = 1


class Configuration(BaseModel):

    top_folder: TopFolder = Field(default=TopFolder())
    operating_mode: str = Field(default=OperatingMode.tof) 
    image_size: ImageSize = Field(default=ImageSize())

    list_of_angles: List[float] = Field(default=None)
    list_of_sample_runs: List[str] = Field(default=None)
    list_of_sample_frame_number: List[int] = Field(default=[])
    list_of_sample_pc: List[float] = Field(default=None)

    list_of_ob_runs: List[str] = Field(default=None)
    list_of_ob_frame_number: List[int] = Field(default=None)
    list_of_ob_pc: List[float] = Field(default=None)

    range_of_tof_to_combine: List[tuple[int, int]] = Field(default=[[0, -1]])
    
    list_clean_algorithm: List[str] = Field(default=[CleaningAlgorithm.histogram, CleaningAlgorithm.threshold])
    histogram_cleaning_settings: HistogramCleaningSettings = Field(default=HistogramCleaningSettings())
    list_normalization_settings: List[str] = Field(default=[NormalizationSettings.pc, 
                                              NormalizationSettings.frame_number,
                                              NormalizationSettings.roi])
    normalization_roi: NormalizationRoi = Field(default=NormalizationRoi())
    
    list_clean_stripes_algorithm: List[str] = Field(default=[])
    remove_stripe_fw_options: RemoveStripeFw = Field(default=RemoveStripeFw())
    remove_stripe_ti_options: RemoveStripeTi = Field(default=RemoveStripeTi())
    remove_stripe_sf_options: RemoveStripeSf = Field(default=RemoveStripeSf())
    remove_stripe_based_sorting_options: RemoveStripeBasedSorting = Field(default=RemoveStripeBasedFiltering())
    remove_stripe_based_filtering_options: RemoveStripeBasedFiltering = Field(default=RemoveStripeBasedFiltering())
    remove_stripe_based_fitting_options: RemoveStripeBasedFitting = Field(default=RemoveStripeBasedFitting())
    remove_large_stripe_options: RemoveLargeStripe = Field(default=RemoveLargeStripe())
    remove_dead_stripe_options: RemoveDeadStripe = Field(default=RemoveDeadStripe())
    remove_all_stripe_options: RemoveAllStripe = Field(default=RemoveAllStripe())
    remove_stripe_based_interpolation_options: RemoveStripeBasedInterpolation = Field(default=RemoveStripeBasedInterpolation())
    
    calculate_center_of_rotation: bool = Field(default=False)
    range_of_slices_for_center_of_rotation: list[int, int] = Field(default=[0, -1])
    
    svmbir_config: SvmbirConfig = Field(default=SvmbirConfig())
    output_folder: str = Field(default="")


def loading_config_file_into_model(config_file_path):
    config_dictionary = load_json_string(config_file_path)
    my_model = Configuration.parse_obj(config_dictionary)
    return my_model
