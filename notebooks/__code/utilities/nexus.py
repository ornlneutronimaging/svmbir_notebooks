import h5py


def get_proton_charge(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        proton_charge = hdf5_data["entry"]["proton_charge"][0]
        return proton_charge
    

def get_frame_number(nexus):
    try:
        with h5py.File(nexus, 'r') as hdf5_data:
            frame_number = hdf5_data["entry"]['DASlogs']['BL10:Det:PIXELMAN:ACQ:NUM']['value'][:][-1]
            return frame_number
    except KeyError:
        return None
    