import os
import random
import csv
import subprocess
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from regression_functions import *
#from regression import regression

# Global dictionary to hold k_each values for each label
k_each_dict = {label: [] for label in ['resolution_rate', 'trapping_rate', 'nucleation_rate', 'diffusivity', 'temperature', 'fission_rate', 'screw_parameter', 'span_parameter', 'cent_parameter', 'helium_production_rate']}

def print_k_each(k_each, scale_value, swelling_value, i):

    if i == 0:
        return  # Do nothing if i is 0

    parameter_labels = ['resolution_rate', 'trapping_rate', 'nucleation_rate', 'diffusivity', 'temperature', 'fission_rate', 'screw_parameter', 'span_parameter', 'cent_parameter', 'helium_production_rate']

    # Determine the label based on i
    label_index = (i - 1) // 5
    label = parameter_labels[label_index] if label_index < len(parameter_labels) else 'Unknown'

    # Append k_each, scale_value and swelling_value to the corresponding label's list
    k_each_dict[label].append((k_each, scale_value, swelling_value))

    # If we have collected 5 k_each values for the label, print them
    if len(k_each_dict[label]) == 5:
        with open('k_each.txt', 'a+', newline='') as file:
            # Move read cursor to the beginning of file and read
            file.seek(0)
            first_line = file.readline()
            # If file is empty, write header
            if not first_line:
                header = "{:<25}".format("")
                for i in range(5):
                    header += "{:<25}".format('swelling_value_' + str(i+1)) + "{:<25}".format('scale_value_' + str(i+1)) + "{:<25}".format('k_each_' + str(i+1))
                header += "\n"
                file.write(header)

            row = "{:<25}".format(label)
            for value, scale, swelling in k_each_dict[label]:
                row += "{:<25}".format(swelling) + "{:<25}".format(scale) + "{:<25}".format(value)
            row += "\n"
            file.write(row)
            k_each_dict[label] = []  # Clear the list for the next set of values




def plot_one_k_graphs():
    # Read the file into a pandas DataFrame
    df = pd.read_csv('k_each.txt', delim_whitespace=True)

    # Only keep the first 6 rows
    df = df.iloc[:6]

    # Initialize a plot
    plt.figure(figsize=(10, 6))

    # Plot each row
    for i, row in df.iterrows():
        scale_values = [row[f'scale_value_{j+1}'] for j in range(5)]
        k_each_values = [row[f'k_each_{j+1}'] for j in range(5)]
        plt.plot(scale_values, k_each_values, 'o-', label=row.name)

    # Set the title and labels
    plt.title('k_each values by scale_value for each parameter')
    plt.xlabel('Scale Value')
    plt.ylabel('k_each Value')

    # Show the legend
    plt.legend()

    # Show the plot
    plt.show()



def plot_k_graphs():
    # Read the file into a pandas DataFrame
    df = pd.read_csv('k_each.txt', delim_whitespace=True)

    # Only keep the first 6 rows
    df = df.iloc[:6]

    # Determine the number of rows and columns for subplots
    n = len(df)
    ncols = 3
    nrows = n // ncols if n % ncols == 0 else n // ncols + 1

    # Initialize a figure with n subplots, arranged in nrows and ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))

    # Flatten the axes array, to make it easier to iterate over
    axs = axs.flatten()

    # Plot each row
    for i, row in enumerate(df.iterrows()):
        _, row = row
        scale_values = [row[f'scale_value_{j+1}'] for j in range(5)]
        k_each_values = [row[f'k_each_{j+1}'] for j in range(5)]

        # Plot on the i-th subplot
        axs[i].plot(scale_values, k_each_values,'o-')

        # Set the title and labels for i-th subplot
        axs[i].set_title(row.name)  # Using the parameter name as title
        axs[i].set_xlabel('Scale Value')
        axs[i].set_ylabel('k_each Value')

    # Remove unused subplots
    if n < nrows * ncols:
        for i in range(n, nrows * ncols):
            fig.delaxes(axs[i])

    # Set the main title for the figure
    fig.suptitle('k_each values by scale_value for each parameter')

    # Adjust the layout so the plots do not overlap
    plt.tight_layout()

    # Show the plot
    plt.show()



def plot_swelling_graphs():
    # Read the file into a pandas DataFrame
    df = pd.read_csv('k_each.txt', delim_whitespace=True)

    # Only keep the first 6 rows
    df = df.iloc[:6]

    # Determine the number of rows and columns for subplots
    n = len(df)
    ncols = 3
    nrows = n // ncols if n % ncols == 0 else n // ncols + 1

    # Initialize a figure with n subplots, arranged in nrows and ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 10))

    # Flatten the axes array, to make it easier to iterate over
    axs = axs.flatten()

    # Plot each row
    for i, row in enumerate(df.iterrows()):
        _, row = row
        scale_values = [row[f'scale_value_{j+1}'] for j in range(5)]
        swelling_values = [row[f'swelling_value_{j+1}'] for j in range(5)]

        # Plot on the i-th subplot
        axs[i].plot(scale_values, swelling_values, 'o-')

        # Set the title and labels for i-th subplot
        axs[i].set_title(row.name)  # Using the parameter name as title
        axs[i].set_xlabel('Scale Value')
        axs[i].set_ylabel('Swelling Value')

    # Remove unused subplots
    if n < nrows * ncols:
        for i in range(n, nrows * ncols):
            fig.delaxes(axs[i])

    # Set the main title for the figure
    fig.suptitle('Swelling values by scale_value for each parameter')

    # Adjust the layout so the plots do not overlap
    plt.tight_layout()

    # Show the plot
    plt.show()





def retrieve_scaling_factors(file_path):
    scaling_factor = 1.0
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace and newline character
            if not line.startswith('#'):  # Ignore comment lines
                value = float(line)
                if value != 1.0:  # Add to list only if the value is not 1.0
                    #scaling_factor.append(value)
                    scaling_factor = value

    #length = len(scaling_factor)

    return scaling_factor



    # for eqch folder
    # take the last vqlue of the column intrqgrqnulqr szelling
    # 1 reference; 1
    # 1 new one; new scqling fqctors
    # ==> k_eqch = 1 / referece vqlue of swelling * (ref - new)/(_ ref scqle PLUS 1)
def calcul_k_swelling(data,x,i,j):

    ref_intraGranularSwellingPos = findSciantixVariablePosition(data[0], "Intragranular gas swelling (/)")
    ref_swelling_value = 100*data[0][-1,ref_intraGranularSwellingPos].astype(float)

    intraGranularSwellingPos = findSciantixVariablePosition(data[x], "Intragranular gas swelling (/)")
    swelling_value = 100*data[x][-1,intraGranularSwellingPos].astype(float)

    scale_value = retrieve_scaling_factors(f'input_scaling_factors/input_scaling_factors_{i}_{j}.txt')

    print("scale value : ",scale_value)
    print("ref swelling_value : ", ref_swelling_value)
    print("swelling_value : ", swelling_value)

    k_each = ((1/ref_swelling_value)*((ref_swelling_value - swelling_value)/(1 - scale_value)))

    print("k : ", k_each)
    #print("k length : ",len(k_each))

    # Print the k_each list to the text file with title
    print_k_each(k_each, scale_value, swelling_value , x)


def remove_scaling_factor_files(file):

    os.chdir(file)
    try :
        shutil.rmtree("input_scaling_factors")
    except :
        print(f"input_scaling_factors not found in {file}")
    try :
        shutil.rmtree("output")
    except :
        print(f"output not found in {file}")
    try :
        os.remove("output.txt")
    except :
        print(f"output.txt not found in {file}")
    """try :
        os.remove("k_each.txt")
    except :
        print(f"k_each.txt not found in {file}")"""

    os.chdir('..')
    # list all files in the current directory
    #files = os.listdir()
    """
    # iterate over all files
    for file in files:
        # if the file name starts with 'input_scaling_factors_', remove it
        if file.startswith('input_scaling_factors_'):
            os.remove(file)
            print(f'Removed file: {file}')"""

def retrieve_output(x):
    # for n in range i :
        # Keep the ieme output file in a new given folder specialy for outputs
        # stock one set of data for every output possible, if i outputs : i datas
        # plot in the same window the given graph for different set of data
        # calculation of the difference between each parameters for every output, define a scheme to determine which one will be the more inpactful

    # create a directory for output.txt files
    os.makedirs('output', exist_ok=True)

    # move original file to the new directory
    shutil.copy("output.txt", f"output/output_{x}.txt")

    #os.rename('output/output.txt', f'output_{i}.txt')



def extract_scaling_factors(i,j):
    #print("i is :",i)
    #print("j is :", j)
    shutil.copy(f"input_scaling_factors/input_scaling_factors_{i+1}_{j+1}.txt", f"input_scaling_factors_{i+1}_{j+1}.txt")
    os.rename(f'input_scaling_factors_{i+1}_{j+1}.txt', 'input_scaling_factors.txt')


def generate_values_around(value, range_percentage, nb):
    values = []
    for _ in range(nb):
        deviation = value * range_percentage / 100
        generated_value = random.uniform(value - deviation, value + deviation)
        values.append(generated_value)
    return values

def generate_values_below(value, range_percentage, nb):
    values = []
    for _ in range(nb):
        deviation = value * range_percentage / 100
        generated_value = random.uniform(value - deviation, value)
        values.append(generated_value)
    return values


def scaling_factors():

    # create a directory for input_scaling_factors files
    os.makedirs('input_scaling_factors', exist_ok=True)

    # read original file
    with open("input_scaling_factors.txt", "r") as file:
        lines = file.readlines()

    # move original file to the new directory
    shutil.copy("input_scaling_factors.txt", "input_scaling_factors/input_scaling_factors.txt")


    # create a copy of the original file directly in the new directory
    with open("input_scaling_factors/input_scaling_factors_0_0.txt", "w") as file_copy:
        file_copy.writelines(lines)

    os.chdir('input_scaling_factors')







    """ --------------- THIS IS THE PART WHERE WE CHOOSE THE VALUES OF EACH SCALLING FACTOR ---------------
    
        Right now it's just an exemple with 10 basic scaling factors txt with random values"""

    """
    # create 10 files
    for i in range(1, 11):
        # create a copy of the original lines
        new_lines = lines.copy()

        # loop through the lines and change the values
        for j in range(0, len(new_lines), 2):  # step by 2 to get the values only
            new_lines[j] = str(round(random.uniform(1, 10), 1)) + '\n'  # random value between 1 and 10

        # write new file directly in the new directory
        new_file_name = f"input_scaling_factors/input_scaling_factors_{i}.txt"
        with open(new_file_name, "w") as new_file:
            new_file.write("".join(new_lines))"""




    resolution_rate = generate_values_around(1,10, 5)
    trapping_rate = generate_values_around(1,10, 5)
    nucleation_rate = generate_values_below(1,20, 5)
    diffusivity = generate_values_around(1,50, 5)
    temperature = generate_values_around(1,10, 5)
    fission_rate = generate_values_around(1,10, 5)
    screw_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    span_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    cent_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    helium_production_rate = [1.0, 1.0, 1.0, 1.0, 1.0]

    parameters = [resolution_rate, trapping_rate, nucleation_rate, diffusivity,
                  temperature, fission_rate, screw_parameter, span_parameter,
                  cent_parameter, helium_production_rate]

    parameter_names = ['resolution_rate', 'trapping_rate', 'nucleation_rate', 'diffusivity',
                       'temperature', 'fission_rate', 'screw_parameter', 'span_parameter',
                       'cent_parameter', 'helium_production_rate']
    #print(parameters)
    # create the files
    for i in range(10):  # we have 10 parameters
        for j in range(5):  # we create 5 txt files for each parameter

            # add the index i and j to the filename, pad them with zero for proper ordering
            new_input_scaling_factors = f"input_scaling_factors_{i+1}_{j+1}.txt"
            # write new file directly in the new directory
            with open(new_input_scaling_factors, 'w') as file:

                # write unchanged parameters as 1
                for k in range(i):
                    file.write('1\n')
                    file.write(f'# scaling factor - {parameter_names[k]}\n')

                # write the changing parameter
                #print(parameters[i][j])
                file.write(str(parameters[i][j]) + '\n')
                file.write(f'# scaling factor - {parameter_names[i]}\n')

                # write remaining unchanged parameters as 1
                for k in range(i+1, 10):
                    file.write('1.0\n')
                    file.write(f'# scaling factor - {parameter_names[k]}\n')






    # for eqch folder
    # take the last vqlue of the column intrqgrqnulqr szelling
    # 1 reference; 1
    # 1 new one; new scqling fqctors
    # ==> k_eqch = 1 / referece vqlue of swelling * (ref - new)/(_ ref scqle PLUS 1)





    os.chdir('..')
    lenght = len(os.listdir(os.path.join(os.getcwd(), 'input_scaling_factors')))
    print("Done.")
    return lenght

def scaling_factors_individual(parameter_value):

    # create a directory for input_scaling_factors files
    os.makedirs('input_scaling_factors', exist_ok=True)

    # read original file
    with open("input_scaling_factors.txt", "r") as file:
        lines = file.readlines()

    # move original file to the new directory
    shutil.copy("input_scaling_factors.txt", "input_scaling_factors/input_scaling_factors.txt")


    # create a copy of the original file directly in the new directory
    with open("input_scaling_factors/input_scaling_factors_0_0.txt", "w") as file_copy:
        file_copy.writelines(lines)

    os.chdir('input_scaling_factors')

    resolution_rate = generate_values_around(1,10, 5)
    trapping_rate = generate_values_around(1,10, 5)
    nucleation_rate = generate_values_below(1,20, 5)
    diffusivity = generate_values_around(1,50, 5)
    temperature = generate_values_around(1,10, 5)
    fission_rate = generate_values_around(1,10, 5)
    screw_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    span_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    cent_parameter = [1.0, 1.0, 1.0, 1.0, 1.0]
    helium_production_rate = [1.0, 1.0, 1.0, 1.0, 1.0]

    parameters = [resolution_rate, trapping_rate, nucleation_rate, diffusivity,
                  temperature, fission_rate, screw_parameter, span_parameter,
                  cent_parameter, helium_production_rate]

    parameter_names = ['resolution_rate', 'trapping_rate', 'nucleation_rate', 'diffusivity',
                       'temperature', 'fission_rate', 'screw_parameter', 'span_parameter',
                       'cent_parameter', 'helium_production_rate']
    #print(parameters)
    # create the files
    i = parameter_value  # we have 10 parameters
    for j in range(5):  # we create 5 txt files for each parameter

        # add the index i and j to the filename, pad them with zero for proper ordering
        new_input_scaling_factors = f"input_scaling_factors_{i+1}_{j+1}.txt"
        # write new file directly in the new directory
        with open(new_input_scaling_factors, 'w') as file:

            # write unchanged parameters as 1
            for k in range(i):
                file.write('1\n')
                file.write(f'# scaling factor - {parameter_names[k]}\n')

            # write the changing parameter
            #print(parameters[i][j])
            file.write(str(parameters[i][j]) + '\n')
            file.write(f'# scaling factor - {parameter_names[i]}\n')

            # write remaining unchanged parameters as 1
            for k in range(i+1, 10):
                file.write('1.0\n')
                file.write(f'# scaling factor - {parameter_names[k]}\n')






    # for eqch folder
    # take the last vqlue of the column intrqgrqnulqr szelling
    # 1 reference; 1
    # 1 new one; new scqling fqctors
    # ==> k_eqch = 1 / referece vqlue of swelling * (ref - new)/(_ ref scqle PLUS 1)





    os.chdir('..')
    lenght = len(os.listdir(os.path.join(os.getcwd(), 'input_scaling_factors')))
    print("Done.")
    return lenght

def main():

    scaling_factors()
    #remove_scaling_factor_files()
    #extract_scaling_factors(3)


if __name__ == "__main__":
    # This is the entry point of the script. When the script is run directly (not imported as a module),
    main()