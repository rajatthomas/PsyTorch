import numpy as np
import os
import os.path as pth

from glob import glob
import nibabel as nib


def create_mri_patch(img_file, patch_dim=64, num_patches=100):
    """
    Function to return a patch extracted from an MRI image
    :param img_file: nii file containing image
    :param patch_dim: dimension of patch to extract
    :param num_patches: number of patches to be extracted from file
    :return: patch of size patch_dim^3
    """

    img = read_mri(img_file)
    img_dim = np.array(img.shape)
    if np.any(img_dim < patch_dim):
        raise ValueError("Dimension of patch should be less than image")

    # Choose a random top corner
    corner_low = np.array([0, 0, 0])
    corner_high = img_dim - patch_dim

    all_patches = np.zeros((num_patches, patch_dim, patch_dim, patch_dim))

    for patch_i in range(num_patches):
        cx, cy, cz = [np.random.random_integers(low=corner_low[i], high=corner_high[i]) for i in [0, 1, 2]]
        all_patches[patch_i] = img[cx:patch_dim, cy:patch_dim, cz:patch_dim]

    return all_patches

def read_mri(img_file):
    """
    Reads MRI nifti files using Nibabel
    :param img_file: nii or nii.gz file
    :return:3D numpy ndarray
    """
    return nib.load(img_file).get_data()


def create_patch_files(root_dir, anat_sub_dir='anat', anat_file='anat.nii.gz', patch_dim=64, num_patches=100):
    """
    Create a directory within root_dir containing ASD and CON subdirectories.
    These subdirectories will contain image patches of size patch_dim
    :param root_dir: directory containing all original subject data
    :param anat_sub_dir: directory name containing the MRI image
    :param anat_file: name of MRI file
    :param patch_dim: dimension of the patch to be extracted.
    :param num_patches: number of patches to be extracted
    :return: num files created
    """

    # Create directory
    dir_name = pth.join(root_dir, 'ABIDE_patch' + str(patch_dim))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    dirs = os.listdir(root_dir)
    for d in dirs:
        img_file = pth.join(d, anat_sub_dir, anat_file)
        all_patches = create_mri_patch(img_file, patch_dim=patch_dim, num_patches=num_patches)

        if not os.path.exists(pth.join(dir_name, d)):
            os.makedirs(pth.join(dir_name, d))

        for patch_i in range(num_patches):
            patch_file = pth.join(dir_name, d, 'patch_'+str(patch_i)+'.npy')
            np.save(patch_file, all_patches[patch_i])
