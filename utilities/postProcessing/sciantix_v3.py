"""
sciantix.py is a python module made to handle the sciantix (standalone) postprocessing,
and plot the quantities in the output.txt file
the purposes are:
    - to plot variables, choosing both x- and y- axes.

@author: Giovanni Zullo

Instructions:
    Type help(sciantix) to get a summary of what the module provides
    To reload the module in the python shell, use importlib.reload(sciantix)

Example:
import sciantix
sciantix.getDictionary()
sciantix.plot("Time (h)", "Xe produced (at/m3)")

"""

import matplotlib.pyplot as plt
import numpy as np
import os
import importlib
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


canvas = None  # Declare canvas as a global variable


""" Defining useful functions"""
def is_output_here(filename):
    # is output.txt in the current folder?
    try:
        f = open(filename)
    except:
        print("ERROR: ", filename, " not found!")
        return False
    else:
        f.close()
        return True

def import_data(filename):
    """
    This function import a .txt file into an ndarray
    """

    if(is_output_here(filename) is False):
        return

    data = np.genfromtxt(filename, dtype= 'str', delimiter='\t')
    return data

def findSciantixVariablePosition(output, variable_name):
    """
    This function gets the output.txt file and the variable name,
    giving back its column index in the ndarray
    """

    i,j = np.where(output == variable_name)
    return int(j)

def working_dir(path):
    """
    This function receives the path of the folder that contains the sciantix file "output.txt".
    If output.txt is in the same folder of sciantix.py, it is not necessary to use this function.
    """
    os.chdir(path)
    return None

def getDictionary(file):
    """
    ----------------
    Input parameters
    ----------------

    output_filename : TYPE = str

        name of the output file (e.g. 'output.txt')
        the output file must be in the sciantix.py directory or
        the path must de defined by sciantix.working_dir(path).

        default name = 'output.txt'

    -------
    Returns
    -------
    The names of the sciantix quantities in output.txt that can be plotted
    and the corresponding values for the plot positions.
    """

    if(is_output_here(file) is False):
        return

    data = import_data(file)
    #print("data : ", data)
    output_tags = data[0,:-1]

    data_shape = data.shape
    # data_shape[0] = number of rows
    # data_shape[1] = number of columns

    # array with the index of the output file header
    tag_positions = np.linspace(0, data_shape[1] - 2, data_shape[1] - 1)

    print(f"An " + file + " file has been detected in the current folder.")
    print("The file ", file, "contains the following variables:")
    print("")

    for i in range(0, data_shape[1] - 1):
        print("Position #", tag_positions[i].astype(int), ", variable = ", output_tags[i])

    return output_tags

def plot(x_name, y_name, output_filename="output.txt", ax=None):
    """
    Parameters
    ----------
    output_filename : TYPE = str
        name of the output file (e.g. 'output.txt')
        the output file must be in the sciantix.py directory or
        the path must de defined by sciantix.working_dir(path)
    x_name :
        name of the sciantix variable
    y_name :
        name of the sciantix variable

    Returns
    -------
    Plot of x_name - y_name
    """

    # verify if output file exists
    if(is_output_here(output_filename) is False):
        return

    # Reading the output file and saving into data variable
    data = import_data(output_filename)

    x = data[1:,findSciantixVariablePosition(data, x_name)].astype(float)
    y = data[1:,findSciantixVariablePosition(data, y_name)].astype(float)

    if ax == None:
        fig, ax = plt.subplots()
    else:
        ax.clear()

    ax.plot(x, y, color = 'blue', label=y_name)

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)

    # No need to return anything as changes are made directly to the ax



def sciantix_v2(file):
    global canvas  # Indicate that we're using the global canvas variable

    output_filename = file
    output_tags = getDictionary(output_filename)

    root = tk.Tk()

    def plot_graph():
        if not listbox_x.curselection() or not listbox_y.curselection():
            messagebox.showwarning("Selection error", "Please select an item from both lists.")
            return
        x_index = listbox_x.curselection()[0]
        y_index = listbox_y.curselection()[0]
        x_name = output_tags[x_index]
        y_name = output_tags[y_index]

        # Here, create the fig and ax when you're about to plot
        fig, ax = plt.subplots(figsize=(5, 5))
        plot(x_name, y_name, output_filename, ax)

        global canvas  # Indicate that we're using the global canvas variable
        if canvas:
            # If a canvas already exists, remove it
            canvas.get_tk_widget().pack_forget()
        canvas = FigureCanvasTkAgg(fig, master=root)  # Create a new canvas with the new figure
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    listbox_x = tk.Listbox(root, exportselection=0, width=50)
    listbox_x.pack(side="left")

    listbox_y = tk.Listbox(root, exportselection=0, width=50)
    listbox_y.pack(side="right")

    for tag in output_tags:
        listbox_x.insert(tk.END, tag)
        listbox_y.insert(tk.END, tag)

    button = tk.Button(root, text="Plot graph", command=plot_graph)
    button.pack()

    root.mainloop()





def main():
    # Check if 'output.txt' exists in the current directory
    if 'output.txt' in os.listdir(os.getcwd()):
        sciantix_v2('output.txt')
    else:
        print('No file named "output.txt" found in the current directory')

if __name__ == "__main__":
    main()