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

def plot(x_name, y_name, output_filename = "output.txt", fig = None, ax = None):
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

    #print("data in plot function : ", data)

    x = data[1:,findSciantixVariablePosition(data, x_name)].astype(float)
    y = data[1:,findSciantixVariablePosition(data, y_name)].astype(float)

    print("x : ", x)
    print("y : ", y)

    if fig == None and ax == None:
        fig, ax = plt.subplots()

    ax.plot(x, y, color = 'blue', label=y_name)

    # ax.set_title(y_name)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    # ax.legend()

    plt.show()

    return fig, ax



def sciantix_v2(file):

    """ WELCOME """
    print(f"This file (sciantix.py) is a python module made to handle the sciantix (standalone) postprocessing, and plot the quantities in the output.txt file.")
    print(f"Type help(sciantix) to get useful information.")

    """

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
            getDictionary(file)










    os.chdir('..')"""
    print(os.getcwd())
    print("dictionnary of", file, " : \n")
    output_tags = getDictionary(file)
    print("output_tags : ", output_tags)

    #plot(output_tags[0], output_tags[2], file)
    for tag in output_tags :
        print("current output : ", tag)
        plot(output_tags[0], tag, file)




def main():
    sciantix_v2()




# If the script is being run as the main program, call the 'main' function.
if __name__ == "__main__":
    main()