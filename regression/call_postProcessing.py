import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil
from regression_functions import *
import scipy.stats as stats
from sklearn.linear_model import LinearRegression

import shutil
import os

def save_output(wpath, folder_name):
    # Define the path of the new directory where you want to save the output files
    new_folder_path = '../regression/output_folder'

    # Ensure the new folder exists, if not create it
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # Construct the path to the output.txt file in the current directory
    output_file_path = os.path.join(wpath, folder_name, 'output.txt')

    # If the output.txt file exists, copy it to the new directory
    if os.path.isfile(output_file_path):
        # Copy the file to the new directory and rename it to include the folder name to prevent overwrites
        new_file_path = os.path.join(new_folder_path, f'{folder_name}_output.txt')
        shutil.copy(output_file_path, new_file_path)

        # Verify if the original output and the copied output are the same
        if are_files_equal(output_file_path, new_file_path) == True:
            print(f"Copy verification for {folder_name} passed!\n")
        else:
            print(f"Copy verification for {folder_name} failed!\n")

def call_postProcessing(wpath):

    # Get list of all files and directories in wpath
    files_and_dirs = os.listdir(wpath)

    # Sort them by filename
    sorted_files_and_dirs = sorted(files_and_dirs)

    # Iterate over sorted list
    for file in sorted_files_and_dirs:
        if "Baker" in file and os.path.isdir(os.path.join(wpath, file)) is True:
            save_output(wpath, file)
        if "White" in file and os.path.isdir(os.path.join(wpath, file)) is True:
            save_output(wpath, file)
        if "Talip" in file and os.path.isdir(os.path.join(wpath, file)) is True:
            save_output(wpath, file)
        if "CONTACT" in file and os.path.isdir(os.path.join(wpath, file)) is True:
            save_output(wpath, file)
        if "oxidation" in file and os.path.isdir(os.path.join(wpath, file)) is True:
            save_output(wpath, file)


    print(wpath)
    folder_name = 'output_folder'
    outputs_path = os.path.join(wpath, folder_name)

    postP_path = '../utilities/postProcessing/sciantix_v2.py'

    shutil.copy(postP_path, outputs_path)


    print("\t------------------ Are you done ? ------------------")
    are_done = int(input("\n Yes : 0 or No : 1"))
    if are_done == 0:
        shutil.rmtree("output_folder")

