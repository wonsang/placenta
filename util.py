import constants
import nibabel as nib
import numpy as np


def read_vol(filename):
    vol = nib.load(filename).get_data()
    
    # need to add channel axis
    if vol.ndim == 3:
        vol = vol[..., np.newaxis]
    return vol


def save_vol(vol, filename, header=None, scale=False):
    if type(vol) is np.ndarray:
        if scale:
            vol *= constants.MAX_VALUE
        vol = np.rint(vol)
        vol = nib.Nifti1Image(vol.astype('int16'), np.diag([3, 3, 3, 1]), header=header)
    vol.to_filename(filename)


def shape(filename):
    return read_vol(filename).shape


def header(filename):
    return nib.load(filename).header


def get_weights(vols):
    if vols is None:
        return None
    w = np.sum(vols) / vols.size
    return (1 - w, w)
