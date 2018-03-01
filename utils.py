import numpy as np
import os
import os.path as pth

import nibabel as nib


def create_mri_patch(img, patch_dim=64):
    """
    Function to return a patch extracted from an MRI image
    :param img: numpy nd-array
    :param patch_dim: dimension of patch to extract
    :return: patch of size patch_dim^3
    """
    img_dim = np.array(img.shape)
    if np.any(img_dim < patch_dim):
        raise ValueError("Dimension of patch should be less than image")

    # Choose a random top corner
    corner_low = np.array([0, 0, 0])
    corner_high = img_dim - patch_dim

    cx, cy, cz = [np.random.random_integers(low=corner_low[i], high=corner_high[i]) for i in [0, 1, 2]]

    return img[cx:patch_dim, cy:patch_dim, cz:patch_dim]


def read_mri(img_file):
    """
    Reads MRI nifti files using Nibabel
    :param img_file: nii or nii.gz file
    :return:3D numpy ndarray
    """
    return nib.load(img_file).get_data()


def create_patch_files(root_dir, anat_sub_dir='anat', patch_dim=64):
    """
    Create a directory within root_dir containing ASD and CON subdirectories.
    These subdirectories will contain image patches of size patch_dim
    :param root_dir: directory containing all subjects
    :param patch_dim:
    :return:
    """

    dirs = os.listdir(root_dir)
    for d in dirs:
        img_file = pth.join(root_dir,