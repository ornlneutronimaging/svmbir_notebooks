
import svmbir, tomopy



"""
Need variables:
sino (num_angles * rows * cols) : processed sinogram
center_offset (int): center offset fron rotation center
angle_rad (list): angle list
"""
sino = []
center_offset = []
angle_rad = []



# simply remove ring artifacts
_sino = tomopy.remove_stripe_fw(sino,level=6,ncore=10)

# launch svmbir
num_threads = 24
max_iterations = 200

T = 2.0
p = 1.2
sharpness = 0.0
snr_db = 30.0

_, num_rows, num_cols = sino.shape
startSlice, endSlice = 0, 50

recon = svmbir.recon(sino = sino[:, startSlice: startSlice:endSlice, ], angles=angle_rad,
                     num_rows = num_rows, num_cols = num_cols,
                     center_offset = center_offset, sharpness=sharpness,
                     snr_db = snr_db, positivity= True, 
                     max_iterations = max_iterations, num_threads= num_threads, 
                     verbose=0, svmbir_lib_path = '/storage',) # lib_path is a location to save intermedia computing data, need a larger space