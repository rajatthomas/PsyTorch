import numpy as np

def create_mri_patch(img, patch_dim=32):


    img_dim = np.array(img.shape)
    if np.any( img_dim < patch_dim):
        raise ValueError("Dimension of patch should be less than image")

    # Choose a random top corner
    corner_low  = np.array([0,0,0])
    corner_high = img_dim - patch_dim

    cx, cy, cz = [ np.random.random_integers(low=corner_low[i], high=corner_high[i] for i in [0,1,2])]

    return img[cx:patch_dim, cy:patch_dim, cz:patch_dim]