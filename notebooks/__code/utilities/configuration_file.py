from pydantic import BaseModel, Field
from typing import List

from __code import CleaningAlgorithm, NormalizationSettings

class RemoveStripeFwWnameOptions:
    haar = 'haar'
    db5 = 'db5'
    sym5 = 'sym5'

class RemoveStripeDim:
    one = '1'
    two = '2'


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


class Configuration(BaseModel):
    list_of_sample_runs: List[str] = []
    list_of_angles: List[str] = []
    list_of_ob_runs: List[str] = []
    range_of_tof_to_combine:  List[tuple[int, int]] = [[-1, -1]]
    list_clean_algorithm: List[str] = [CleaningAlgorithm.histogram, CleaningAlgorithm.threshold]
    list_normalization_settings: List[str] = [NormalizationSettings.pc, 
                                              NormalizationSettings.frame_number,
                                              NormalizationSettings.roi]
    list_clean_stripes_algorithm: List[str] = []

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
    
    range_of_slices_for_center_of_rotation: list[int, int] = []
    svmbir_sharpness: float = 0
    svmbir_snr_db: float = 30.0
    svmbir_positivity: bool = True
    svmbir_max_iterations: int = 200
    svmbir_verbose: bool = False
    output_folder: str = ""
