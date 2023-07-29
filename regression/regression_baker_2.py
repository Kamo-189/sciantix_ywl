"""

This is a python script to execute the regression (running the validation database) of sciantix.

@author G. Zullo

"""

""" ------------------- Import requiered depedencies ------------------- """

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil
from regression_functions import *
from scaling_factors import scaling_factors
from scaling_factors import extract_scaling_factors
from scaling_factors import *
from scaling_factors import remove_scaling_factor_files
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import sys

""" ------------------- Global Variables ------------------- """

# Intergranular gaseous swelling database from Baker 1977 experiments
igSwellingBaker = [0.06, 0.07, 0.08, 0.09, 0.12, 0.15, 0.18, 0.24, 0.31]
# Data from SCIANTIX 1.0
igSwelling1 = [0.033, 0.048, 0.062, 0.073, 0.079, 0.082, 0.083, 0.084, 0.086]
# Data generated from SCIANTIX 2.0
igSwelling2 = []
intraGranularSwellingPos = []
FGR2 = []
FGRPos = []

number_of_tests_failed = 0
gold = []
sample_number = len(igSwelling1)


""" ------------------- Functions ------------------- """

# Verify the test results
""" Need to change something on this function because it only check the last output"""
def check_result(number_of_tests_failed):
  if are_files_equal('output.txt', 'output_gold.txt') == True:
    print(f"Test passed!\n")
  else:
    print(f"Test failed!\n")
    number_of_tests_failed += 1

  return number_of_tests_failed

# Verify the existence of the files: output.txt and output_gold.txt
def check_output(file, l):

  data = [None]*(l-1)

  os.chdir('output')
  for i in range(0,l-1):
    try :
      data[i] = import_data(f"output_{i}.txt")
    except :
      print(f"output.txt not found in {file}")
      data[i] = np.zeros(shape=(1, 1))

    print("data[",i,"] :", data[i])

  os.chdir('..')
  """
  try :
    data = import_data("output.txt")
  except :
    print(f"output.txt not found in {file}")
    data = np.zeros(shape=(1, 1))"""

  try :
    data_gold = import_data("output_gold.txt")
  except :
    print(f"output_gold.txt not found in {file}")
    data_gold = np.ones(shape=(1, 1))

  return data, data_gold

# Execute sciantix in the current test folder
def do_sciantix():
  # copying input files from the regression folder into the current folder
  #shutil.copy("../input_settings.txt", os.getcwd())


  shutil.copy("../input_scaling_factors.txt", os.getcwd())

  l = scaling_factors()
  #remove_scaling_factor_files()

  # copying and executing sciantix.exe into cwd
  shutil.copy("../sciantix.x", os.getcwd())

  continu = 1

  for i in range(0,l-1):
    extract_scaling_factors(i)
    os.system("./sciantix.x")
    retrieve_output(i)

    """print("\t------------------ Are you done ? ------------------")
    are_done = int(input("\n Yes : 0 or No : 1 \n"))
    if are_done == 0:
      sys.exit(1)"""

  # copying and executing sciantix.exe into cwd
  #shutil.copy("../sciantix.x", os.getcwd())
  #os.system("./sciantix.x")

  # removing useless file
  os.remove("sciantix.x")
  os.remove("execution.txt")
  os.remove("input_check.txt")
  # os.remove("overview.txt")

  """print("\t------------------ Are you finish ? ------------------")
  are_finish = int(input("\n Yes : 0 or No : 1 \n"))
  if are_finish == 0:
    remove_scaling_factor_files()
    sys.exit(1)"""

  #remove_scaling_factor_files()

  return l

# Replace the existing output_gold.txt with the new output.txt
def do_gold():
  try :
    os.path.exists('output.txt')

    os.remove('output_gold.txt')
    os.rename('output.txt', 'output_gold.txt')

  except :
    print(f"output.txt not found in {file}")

# Plot the regression test results
def do_plot(i):
  # SCIANTIX 1.0 vs. SCIANTIX 2.0
  fig, ax = plt.subplots()

  ax.scatter(igSwellingBaker, igSwelling1, c = '#FA82B4', edgecolors= '#999AA2', marker = 'o', s=20, label='SCIANTIX 1.0')
  ax.scatter(igSwellingBaker, igSwelling2[i], c = '#98E18D', edgecolors= '#999AA2', marker = 'o', s=20, label='SCIANTIX 2.0')

  ax.plot([1e-3, 1e2],[1e-3, 1e2], '-', color = '#757575')
  ax.plot([1e-3, 1e2],[2e-3, 2e2],'--', color = '#757575')
  ax.plot([1e-3, 1e2],[5e-4, 5e1],'--', color = '#757575')
  ax.set_xlim(1e-2, 1e1)
  ax.set_ylim(1e-2, 1e1)

  ax.set_xscale('log')
  ax.set_yscale('log')

  # ax.set_title('Intragranular gaseous swelling')
  ax.set_xlabel('Experimental (%)')
  ax.set_ylabel('Calculated (%)')
  ax.legend()

  plt.show()


  # GOLD vs. SCIANTIX 2.0
  fig, ax = plt.subplots()

  ax.scatter(igSwellingBaker, gold, c = '#C9C954', edgecolors= '#999AA2', marker = 'o', s=20, label='Gold')
  ax.scatter(igSwellingBaker, igSwelling2[i], c = '#98E18D', edgecolors= '#999AA2', marker = 'o', s=20, label='SCIANTIX 2.0')

  ax.plot([1e-3, 1e2],[1e-3, 1e2], '-', color = '#757575')
  ax.plot([1e-3, 1e2],[2e-3, 2e2],'--', color = '#757575')
  ax.plot([1e-3, 1e2],[5e-4, 5e1],'--', color = '#757575')

  ax.set_xlim(1e-2, 1e1)
  ax.set_ylim(1e-2, 1e1)

  ax.set_xscale('log')
  ax.set_yscale('log')

  # ax.set_title('Intergranular gaseous swelling')
  ax.set_xlabel('Experimental (%)')
  ax.set_ylabel('Calculated (%)')
  ax.legend()

  plt.show()

  # Fission gases release plot
  fig, ax = plt.subplots()
  ax.scatter(igSwelling2[i], FGR2[i], c = '#98E18D', edgecolors= '#999AA2', marker = 'o', s=20, label='FGR SCIANTIX 2.0')

  ax.set_xscale('log')
  ax.set_yscale('log')

  ax.set_xlabel('Swelling (%)')
  ax.set_ylabel('FGR (%)')
  ax.legend()

  plt.show()


# Main function of the baker regression
def regression_baker(wpath, mode_Baker, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed):

  # Exit of the function without doing anything
  if mode_Baker == 0 :
    return folderList, number_of_tests, number_of_tests_failed

  # Get list of all files and directories in wpath
  files_and_dirs = os.listdir(wpath)

  # Sort them by filename
  sorted_files_and_dirs = sorted(files_and_dirs)

  # Iterate over sorted list
  for file in sorted_files_and_dirs:
    # Verify on a given folder, if Baker is in it's name
    if "Baker" in file and os.path.isdir(file):
      folderList.append(file)
      os.chdir(file)


      print(f"Now in folder {file}...")
      number_of_tests += 1

      # mode_gold = 0 : Use SCIANTIX / Don't use GOLD and check result
      if mode_gold == 0:

        l = do_sciantix()
        data, data_gold = check_output(file, l)
        number_of_tests_failed = check_result(number_of_tests_failed)

      # mode_gold = 1 : Use SCIANTIX / Use GOLD
      if mode_gold == 1:

        l = do_sciantix()
        data, data_gold = check_output(file, l)
        # Need to change the gold because now we have many different output
        print("...golding results.")
        do_gold()

      # mode_gold = 2 : Don't use SCIANTIX / Don't use GOLD and check result
      if mode_gold == 2:

        data, data_gold = check_output(file)
        number_of_tests_failed = check_result(number_of_tests_failed)

      # mode_gold = 3 : Don't use SCIANTIX / Use GOLD
      if mode_gold == 3:

        data, data_gold = check_output(file)
        print("...golding existing results.")
        do_gold()


      for i in range(0,l-1):

        print("i is : ",i)
        FGRPos = [None]*(l-1)
        intraGranularSwellingPos = [None]*(l-1)

        #FGR2 = [None]*(l-1)
        #igSwelling2 = [None]*(l-1)


        # Retrieve the generated data of Fission gas release
        FGRPos[i] = findSciantixVariablePosition(data[i], "Fission gas release (/)")
        if i >= len(FGR2):
          FGR2.append([])  # Append a new list if FGR2 doesn't have a list at position i
        FGR2[i].append(100 * data[i][-1,FGRPos[i]].astype(float))  # Now it's safe to append to FGR2[i]


        print(FGR2[i])

        # Retrieve the generated data of Intragranular gas swelling
        intraGranularSwellingPos[i] = findSciantixVariablePosition(data[i], "Intragranular gas swelling (/)")
        if i >= len(igSwelling2):
          igSwelling2.append([])
        igSwelling2[i].append(100*data[i][-1,intraGranularSwellingPos[i]].astype(float))

        print(igSwelling2[i])
        """
        print("data_gold is : ", data_gold)
        print("data[i] is : ", data[i])
        print("lenght of data_gold : ",len(data_gold))
        print("lenght of data[i] : ",len(data[i]))
        print("gold is : ", gold)
        print("lenght of gold : ",len(gold))
        print("lenght of igSwelling2 : ",len(igSwelling2[i]))"""

      # Retrieve the gold data of Intragranular gas swelling
      intraGranularSwellingGoldPos = findSciantixVariablePosition(data_gold, "Intragranular gas swelling (/)")
      gold.append(100*data_gold[-1,intraGranularSwellingGoldPos].astype(float))
      os.chdir('..')


  # Check if the user has chosen to display the various plots
  if mode_plot == 1:
    do_plot(i)

  # Experimental data: mean, median, ...
  print(f"Experimental data - mean: ", np.mean(igSwellingBaker))
  print(f"Experimental data - median: ", np.median(igSwellingBaker))
  print(f"Experimental data - Q1: ", np.percentile(igSwellingBaker, 25, interpolation = 'midpoint'))
  print(f"Experimental data - Q3: ", np.percentile(igSwellingBaker, 75, interpolation = 'midpoint'))

  # SCIANTIX 1.0: mean, median, ...
  print(f"SCIANTIX 1.0 - mean: ", np.mean(igSwelling1))
  print(f"SCIANTIX 1.0 - median: ", np.median(igSwelling1))
  print(f"SCIANTIX 1.0 - Q1: ", np.percentile(igSwelling1, 25, interpolation = 'midpoint'))
  print(f"SCIANTIX 1.0 - Q3: ", np.percentile(igSwelling1, 75, interpolation = 'midpoint'))

  # SCIANTIX 2.0: mean and median, ...
  print(f"SCIANTIX 2.0 - mean: ", np.mean(igSwelling2))
  print(f"SCIANTIX 2.0 - median: ", np.median(igSwelling2))
  print(f"SCIANTIX 2.0 - median: ", np.percentile(igSwelling2, 25, interpolation = 'midpoint'))
  print(f"SCIANTIX 2.0 - median: ", np.percentile(igSwelling2, 75, interpolation = 'midpoint'))

  # SCIANTIX 1.0 and 2.0 - Median absolute deviatiosns
  deviations_1 = abs(np.array(igSwellingBaker) - igSwelling1)
  deviations_2 = abs(np.array(igSwellingBaker) - igSwelling2)
  print(f"SCIANTIX 1.0 - MAD: ", np.median(deviations_1))
  print(f"SCIANTIX 2.0 - MAD: ", np.median(deviations_2))

  # RMSE
  print(f"SCIANTIX 1.0 - RMSE: ", np.mean(np.array(igSwellingBaker) - igSwelling1)**2)
  print(f"SCIANTIX 2.0 - RMSE: ", np.mean(np.array(igSwellingBaker) - igSwelling2)**2)
  print("\n")

  return folderList, number_of_tests, number_of_tests_failed
