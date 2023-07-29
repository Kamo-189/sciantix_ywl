# Import the necessary modules and libraries.
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

# Global variables
sciantix_v2_module = None  # A placeholder for the dynamically-loaded Sciantix v2 module.
selected_file = None  # A placeholder for the file selected by the user.
main = 0  # A flag to indicate whether the script is the main script.

def select_file(evt):
    # A function to handle listbox item selection events.

    global selected_file  # Use the global variable 'selected_file'.

    w = evt.widget  # Get the widget that triggered the event.
    index = int(w.curselection()[0])  # Get the index of the selected item.
    selected_file = w.get(index)  # Get the selected file name and store it in 'selected_file'.

def confirm_file():
    # A function to handle file confirmation.

    global selected_file  # Use the global variable 'selected_file'.
    global sciantix_v2_module  # Use the global variable 'sciantix_v2_module'.

    # If a file has been selected and the Sciantix v2 module is loaded,
    # call the 'sciantix_v2' function with the selected file name and the 'main' flag as arguments.
    if selected_file and sciantix_v2_module is not None:
        print("Selected file : ", selected_file)
        sciantix_v2_module.sciantix_v2(selected_file, main)

    elif not selected_file:  # If no file has been selected yet, print a message.
        print("No file selected yet.")
    else:  # If the Sciantix v2 module has not been loaded yet, print a message.
        print("sciantix_v2_module is not yet loaded.")

def save_output(wpath, folder_name):
    # A function to save the output files to a new directory.

    new_folder_path = '../regression/output_folder'  # Define the path of the new directory.

    # If the new directory does not exist, create it.
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    output_file_path = os.path.join(wpath, folder_name, 'output.txt')  # Construct the path to the output.txt file.

    # If the output.txt file exists, copy it to the new directory.
    if os.path.isfile(output_file_path):
        new_file_path = os.path.join(new_folder_path, f'{folder_name}_output.txt')
        shutil.copy(output_file_path, new_file_path)

        # Verify if the original output and the copied output are the same.
        if are_files_equal(output_file_path, new_file_path) == True:
            print(f"Copy verification for {folder_name} passed!\n")
        else:
            print(f"Copy verification for {folder_name} failed!\n")

def call_postProcessing(wpath):
    # A function to call the post-processing routine.

    def hide_window():
        # A function to handle the window close event.
        root.quit()  # Quit the mainloop and close all tkinter windows

    files_and_dirs = os.listdir(wpath)  # Get a list of all files and directories in the current working directory.
    sorted_files_and_dirs = sorted(files_and_dirs)  # Sort them by file name.

    # Iterate over the sorted list and save the output files of certain directories.
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

    folder_name = 'output_folder'  # The name of the output folder.
    outputs_path = os.path.join(wpath, folder_name)  # The path to the output folder.

    postP_path = '../utilities/postProcessing/sciantix_v2.py'  # The path to the sciantix_v2.py script.

    # Copy the Python script.
    dest_file_path = os.path.join(outputs_path, 'sciantix_v2.py')
    shutil.copy(postP_path, dest_file_path)

    # Import the module dynamically.
    global sciantix_v2_module  # Use the global variable 'sciantix_v2_module'.
    spec = importlib.util.spec_from_file_location("sciantix_v2", dest_file_path)
    sciantix_v2_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sciantix_v2_module)

    # Change the current working directory to the subfolder.
    subfolder_path = os.path.join(os.getcwd(), 'output_folder')
    os.chdir(subfolder_path)

    # Current working directory.
    wpath = os.getcwd()
    print("current folder before getDictionary : ", wpath)

    # Create a simple GUI window.
    root = tk.Tk()

    # Create a listbox and a scrollbar.
    file_listbox = tk.Listbox(root, width=50, height=30)  # Adjust the width and height as needed.
    file_listbox.bind('<<ListboxSelect>>', select_file)  # Bind the listbox selection event to the 'select_file' function.
    file_listbox.pack()  # Place the listbox in the window.
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=file_listbox.yview)  # Create a vertical scrollbar for the listbox.
    scrollbar.pack(side="right", fill="y")  # Place the scrollbar in the window.
    file_listbox.configure(yscrollcommand=scrollbar.set)  # Set the listbox to use the scrollbar.

    # Get a list of all output files.
    all_files = os.listdir(wpath)
    output_files = [filename for filename in all_files if filename.endswith('.txt')]

    # Sort the output files.
    sorted_output_files = sorted(output_files)

    # Add the output files to the listbox.
    for file in sorted_output_files:
        file_listbox.insert(tk.END, file)

    # Create a button that will confirm the selected file.
    confirm_button = tk.Button(root, text="Confirm selection", command=confirm_file)  # Bind the button click event to the 'confirm_file' function.
    confirm_button.pack()  # Place the button in the window.

    # Override the default window-closing behavior.
    root.protocol('WM_DELETE_WINDOW', hide_window)

    # Run the GUI event loop.
    root.mainloop()

    os.chdir('..')

    print("current folder after sciantix_v2 : ",os.getcwd())

    print("\t------------------ Are you done ? ------------------")
    are_done = int(input("\n Yes : 0 or No : 1 \n"))
    if are_done == 0:
        shutil.rmtree("output_folder")