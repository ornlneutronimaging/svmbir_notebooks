import h5py


def get_proton_charge(nexus):

    with h5py.File(nexus, 'r') as hdf5_data:
        proton_charge = hdf5_data["entry"]["proton_charge"][0]
        return proton_charge
    