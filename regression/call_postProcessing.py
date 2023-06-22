
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from regression_functions import *
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import importlib.util
import shutil
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Global variable to hold the module
sciantix_v2_module = None
selected_file = None

def select_file(evt):
    # Use the global variable
    global selected_file

    # Get selected file from the listbox
    w = evt.widget
    index = int(w.curselection()[0])
    selected_file = w.get(index)

def confirm_file():
    # Use the global variable
    global selected_file
    global sciantix_v2_module

    if selected_file and sciantix_v2_module is not None:
        print("Selected file : ", selected_file)
        sciantix_v2_module.sciantix_v2(selected_file)
    elif not selected_file:
        print("No file selected yet.")
    else:
        print("sciantix_v2_module is not yet loaded.")

"""def select_file():
    wpath = os.getcwd()
    # Use the global variable
    global sciantix_v2_module

    # Open a file dialog and let the user select a file
    filename = filedialog.askopenfilename(initialdir = wpath, title = "Select output file",
                                          filetypes = (("text files", "*.txt"), ("all files", "*.*")))

    if filename:
        print("current file : ", filename)
        if sciantix_v2_module is not None:
            print("sciantix_v2_module is loaded.")
            sciantix_v2_module.sciantix_v2(filename)
        else:
            print("sciantix_v2_module is not yet loaded.")"""

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


    print("current folder before sciantix_v2 : ", wpath)

    folder_name = 'output_folder'
    outputs_path = os.path.join(wpath, folder_name)

    postP_path = '../utilities/postProcessing/sciantix_v2.py'



    # Copy the Python script
    dest_file_path = os.path.join(outputs_path, 'sciantix_v2.py')
    shutil.copy(postP_path, dest_file_path)

    # Import the module dynamically
    global sciantix_v2_module  # This line is added
    spec = importlib.util.spec_from_file_location("sciantix_v2", dest_file_path)
    sciantix_v2_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sciantix_v2_module)

    # Change the current working directory to the subfolder
    subfolder_path = os.path.join(os.getcwd(), 'output_folder')
    os.chdir(subfolder_path)

    # Current working directory
    wpath = os.getcwd()
    print("current folder before getDictionary : ", wpath)

    # Create a simple GUI window
    root = tk.Tk()

    # Create a listbox and a scrollbar
    file_listbox = tk.Listbox(root, width=50, height=30)  # Adjust the width and height as needed
    file_listbox.bind('<<ListboxSelect>>', select_file)
    file_listbox.pack()
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=file_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    file_listbox.configure(yscrollcommand=scrollbar.set)

    # Get a list of all output files
    all_files = os.listdir(wpath)
    output_files = [filename for filename in all_files if filename.endswith('.txt')]

    # Sort the files
    sorted_output_files = sorted(output_files)

    # Add the files to the listbox
    for file in sorted_output_files:
        file_listbox.insert(tk.END, file)


    # Create a button that will confirm the selected file
    confirm_button = tk.Button(root, text="Confirm selection", command=confirm_file)
    confirm_button.pack()

    # Run the GUI event loop
    root.mainloop()



    """



    # Copy the Python script
    dest_file_path = os.path.join(outputs_path, 'sciantix_v2.py')
    shutil.copy(postP_path, dest_file_path)

    # Import the module dynamically
    spec = importlib.util.spec_from_file_location("sciantix_v2", dest_file_path)
    sciantix_v2_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sciantix_v2_module)

    print(os.getcwd())

    # Construct the full path to the subfolder
    subfolder_path = os.path.join(os.getcwd(), 'output_folder')

    # Change the current working directory to the subfolder
    os.chdir(subfolder_path)

    wpath = os.getcwd()

    print("current folder before getDictionary : ",os.getcwd())

    # Get list of all files and directories in wpath
    files_and_dirs = os.listdir(wpath)

    # Sort them by filename
    sorted_files_and_dirs = sorted(files_and_dirs)

    # Iterate over sorted list
    for file in sorted_files_and_dirs:
        if "output.txt" in file :
            print("current file : ", file)
            sciantix_v2_module.sciantix_v2(file)

    os.chdir('..')

    # sciantix_v2_module.your_function_name()  # Replace with the right function's name
    #sciantix_v2_module.sciantix_v2()

    print("current folder after sciantix_v2 : ",os.getcwd())



    print("\t------------------ Are you done ? ------------------")
    are_done = int(input("\n Yes : 0 or No : 1 \n"))
    if are_done == 0:
        shutil.rmtree("output_folder")"""


