# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:49:41 2021

@author: Thibaut


This script aims at extracting the data from the dataset zip file (which 
is too big to upload on github) and dispatch the training data and test data according
to VAL_RATIO (for a VAL_RATIO = 0.1 the 1 in 10 images will go in the test dataset) 
"""

import os
from shutil import copy, rmtree
import random
import zipfile
ZIP_DATASET_PATH = "E:\\repo_tensorflow\\tensorflow_projet\\humansandcats.zip"
DEST_EXTRACTED_FILE = "E:\\repo_tensorflow\\\\tensorflow_projet\\dataset"
VAL_RATIO = 0.1
CLASSES = ["cats", "humans"]
DATASET_HOME = 'E:\\repo_tensorflow\\tensorflow_projet\\dataset_cats_vs_humans\\'


def prepare_data():
    dataset_home = DATASET_HOME
    subdirs = ['train/', 'test/']
    for subdir in subdirs:
        # create label subdirectories
        for labldir in CLASSES:
            newdir = dataset_home + subdir + labldir
            os.umask(0)
            os.makedirs(newdir, mode=0o777, exist_ok=True)

    random.seed(1)
    # define ratio of pictures to use for validation
    # copy training dataset images into subdirectories
    src_directory = DEST_EXTRACTED_FILE + "\\Images"

    for directory in os.listdir(src_directory):
        src = src_directory + '\\' + directory

        for file in os.listdir(src):
            dst_dir = 'train/'
            if is_test_data():
                dst_dir = 'test\\'
            dst = dataset_home + dst_dir + directory.lower()  # + file
            copy(src + "\\" + file, dst)

    delete_unzip_directory()


def extract_data():
    with zipfile.ZipFile(ZIP_DATASET_PATH, 'r') as zip_ref:
        zip_ref.extractall(DEST_EXTRACTED_FILE)


def delete_unzip_directory():
    rmtree(DEST_EXTRACTED_FILE)


def is_test_data():
    if random.random() < VAL_RATIO:
        return True
    return False


if __name__ == "__main__":
    extract_data()
    prepare_data()
