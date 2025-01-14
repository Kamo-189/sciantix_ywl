"""

This is a python script to execute the regression (running the validation database) of sciantix.

@author G. Zullo

"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil
from regression_functions import *

""" Validation: CONTACT1 """
def regression_contact(wpath, mode_CONTACT, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed):
  if mode_CONTACT == '0':
    return folderList, number_of_tests, number_of_tests_failed
  
  for file in os.listdir(wpath):
    if "CONTACT" in file and os.path.isdir(file) is True:
      folderList.append((file))
      os.chdir(file)

      shutil.copy("..\input_scaling_factors.txt", os.getcwd())

      print(f"Now in folder {file}...")
      number_of_tests += 1

      if mode_gold == '0' or mode_gold == '1':

        # copying and executing sciantix.exe into cwd
        shutil.copy("..\sciantix.exe", os.getcwd())
        os.system("sciantix.exe")

        # removing useless file
        os.remove("sciantix.exe")
        os.remove("execution.txt")
        os.remove("input_check.txt")
        # os.remove("overview.txt")
      
      try : 
        data = import_data("output.txt")
      except :
        print(f"output.txt not found in {file}")
        data = np.zeros(shape=(1, 1))
      
      try : 
        data_gold = import_data("output_gold.txt")
      except :
        print(f"output_gold.txt not found in {file}")
        data_gold = np.ones(shape=(1, 1))
        
      if mode_gold == '0':
        if are_files_equal('output.txt', 'output_gold.txt') == True:
          print(f"Test passed!\n")
        else:
          print(f"Test failed!\n")
          number_of_tests_failed += 1

      if mode_gold == '1':
        
        try :
          os.path.exists('output.txt')

          print(f"...golding results.")
          os.remove('output_gold.txt')
          os.rename('output.txt', 'output_gold.txt')

        except :
          print(f"output.txt not found in {file}")

      if mode_gold == '2':
        if are_files_equal('output.txt', 'output_gold.txt') == True:
          print(f"Test passed!\n")
        else:
          print(f"Test failed!\n")
          number_of_tests_failed += 1

        try : 
          data = import_data("output.txt")
        except :
          print(f"output.txt not found in {file}")
          data = data_gold

      if mode_gold == '3':
        print(f"...golding existing results.")
        os.remove('output_gold.txt')
        os.rename('output.txt', 'output_gold.txt')

      exp_Xe133 = import_data("experimental_RB_Xe133.txt")
      exp_Kr85m = import_data("experimental_RB_Kr85m.txt")

      # output.txt
      # find indexes
      timePos = findSciantixVariablePosition(data, "Time (h)")
      temperaturePos = findSciantixVariablePosition(data, "Temperature (K)")
      burnupPos = findSciantixVariablePosition(data, "Burnup (MWd/kgUO2)")
      Xe133Pos = findSciantixVariablePosition(data, "Xe133 R/B (/)")
      Kr85mPos = findSciantixVariablePosition(data, "Kr85m R/B (/)")

      # arrays
      time = data[1:,timePos].astype(float)
      temperature = data[1:,temperaturePos].astype(float)
      burnup = data[1:,burnupPos].astype(float) / 0.8814
      Xe133 = data[1:,Xe133Pos].astype(float)
      Kr85m = data[1:,Kr85mPos].astype(float)

      # import data
      calculated_Kr85m_Zullo2022 = import_data("calculated_Kr85m_Zullo.txt")
      calculated_Xe133_Zullo2022 = import_data("calculated_Xe133_Zullo.txt")

      """ Statistical analysis """
      # Find common position in the burnup vector
      precision = 2
      common_values_1 = np.intersect1d(np.round(burnup,precision), np.round(exp_Xe133[1:,0].astype(float),precision))
      common_values_2 = np.intersect1d(np.round(burnup,precision), np.round(exp_Kr85m[1:,0].astype(float),precision))
      # Find the indices of the common values in each array
      indices_1 = np.where(np.in1d(np.round(burnup,precision), common_values_1))[0]
      indices_2 = np.where(np.in1d(np.round(burnup,precision), common_values_2))[0]
      # finding manually common position to avoid truncation errors
      indices_1 = [934, 2125, 2932, 5862, 7488,  8303, 8705, 10297]
      indices_2 = [934, 2125, 2932, 5862, 7488,  8303, 8705, 10297, 11275, -1]

      # Mean squared error (SCIANTIX 2.0)
      mse_xe133_2 = np.mean(((Xe133[indices_1] - exp_Xe133[1:,1].astype(float)))**2)
      mse_kr85m_2 = np.mean(((Kr85m[indices_2] - exp_Kr85m[1:,1].astype(float)))**2)
      # absolute deviations (SCIANTIX 2.0)
      dev_xe133_2 = abs((Xe133[indices_1] - exp_Xe133[1:,1].astype(float)))
      dev_kr85m_2 = abs((Kr85m[indices_2] - exp_Kr85m[1:,1].astype(float)))

      # Find common position in the burnup vector
      precision = 1
      common_values_1 = np.intersect1d(np.round(calculated_Xe133_Zullo2022[1:,0].astype(float),precision), np.round(exp_Xe133[1:,0].astype(float),precision))
      common_values_2 = np.intersect1d(np.round(calculated_Kr85m_Zullo2022[1:,0].astype(float),precision), np.round(exp_Kr85m[1:,0].astype(float),precision))
      # Find the indices of the common values in each array
      indices_1 = np.where(np.in1d(np.round(calculated_Xe133_Zullo2022[1:,0].astype(float),precision), common_values_1))[0]
      indices_2 = np.where(np.in1d(np.round(calculated_Kr85m_Zullo2022[1:,0].astype(float),precision), common_values_2))[0]
      # finding manually common position to avoid truncation errors
      indices_1 = [98, 221, 305, 613, 781, 864, 903, 1065]
      indices_2 = [98, 221, 305, 613, 781, 864, 903, 1065, 1169, 1328]

      # Mean squared error (SCIANTIX 1.0)
      mse_xe133_1 = np.mean(((calculated_Xe133_Zullo2022[indices_1,1].astype(float) - exp_Xe133[1:,1].astype(float)))**2)
      mse_kr85m_1 = np.mean(((calculated_Kr85m_Zullo2022[indices_2,1].astype(float) - exp_Kr85m[1:,1].astype(float)))**2)
      # absolute deviations (SCIANTIX 1.0)
      dev_xe133_1 = abs((calculated_Xe133_Zullo2022[indices_1,1].astype(float) - exp_Xe133[1:,1].astype(float)))
      dev_kr85m_1 = abs((calculated_Kr85m_Zullo2022[indices_2,1].astype(float) - exp_Kr85m[1:,1].astype(float)))

      print(f"SCIANTIX 1.0 - Xe133, RMSE = ", mse_xe133_1)
      print(f"SCIANTIX 2.0 - Xe133, RMSE = ", mse_xe133_2)
      print(f"SCIANTIX 1.0 - Kr85m, RMSE = ", mse_kr85m_1)
      print(f"SCIANTIX 2.0 - Kr85m, RMSE = ", mse_kr85m_2)
      print(f"SCIANTIX 1.0 - Xe133, Median absolute deviations = ", np.median(dev_xe133_1))
      print(f"SCIANTIX 2.0 - Xe133, Median absolute deviations = ", np.median(dev_xe133_2))
      print(f"SCIANTIX 1.0 - Kr85m, Median absolute deviations = ", np.median(dev_kr85m_1))
      print(f"SCIANTIX 2.0 - Kr85m, Median absolute deviations = ", np.median(dev_kr85m_2))
      print("\n")

      """ Plot: Radiaoctive release """
      if mode_plot == '1':

        fig, ax = plt.subplots(1,2)
        plt.subplots_adjust(left=0.1,
                  bottom=0.1,
                  right=0.9,
                  top=0.9,
                  wspace=0.34,
                  hspace=0.4)
        
        axT = ax[0].twinx()
        axT.set_ylabel('Temperature (K)')
        axT.plot(burnup, temperature, 'r-', linewidth = 1, label="Temperature")
        axT.set_zorder(1)

        ax[0].plot(burnup, Xe133, color = '#98E18D', linewidth = 2, label='SCIANTIX 2.0 ${}^{133}$Xe')
        ax[0].plot(calculated_Xe133_Zullo2022[1:,0].astype(float), calculated_Xe133_Zullo2022[1:,1].astype(float), '--', color = 'black', linewidth = 1, label='Zullo et al. (2022) ${}^{133}$Xe')
        ax[0].plot(exp_Xe133[1:,0].astype(float), exp_Xe133[1:,1].astype(float), 'o', color = '#B3B3B3', label='Data from IFPE ${}^{133}$Xe')
        ax[0].set_zorder(2)
        ax[0].set_frame_on(False)

        # ax.set_title(file + ' - ${}^{133}$Xe')
        ax[0].set_xlabel('Burnup (GWd/tU)')
        ax[0].set_ylabel('Release-to-birth ratio (/)')
        ax[0].legend()
        ax[0].set_yscale('log')
        ax[0].set_ylim(1e-5, 1.0)

        h1, l1 = ax[0].get_legend_handles_labels()
        h2, l2 = axT.get_legend_handles_labels()
        ax[0].legend(h1+h2, l1+l2, loc='lower right')
  
        axT = ax[1].twinx()
        axT.set_ylabel('Temperature (K)')
        axT.plot(burnup, temperature, 'r-', linewidth = 1, label="Temperature")
        axT.set_zorder(1)

        ax[1].plot(burnup, Kr85m, color = '#98E18D', linewidth = 2, label='SCIANTIX 2.0 ${}^{85m}$Kr')
        ax[1].plot(calculated_Kr85m_Zullo2022[1:,0].astype(float), calculated_Kr85m_Zullo2022[1:,1].astype(float), '--', color = 'black', linewidth = 1, label='Zullo et al. (2022) ${}^{85m}$Kr')
        ax[1].plot(exp_Kr85m[1:,0].astype(float), exp_Kr85m[1:,1].astype(float), 'o', color = '#B3B3B3', label='Data from IFPE ${}^{85m}$Kr')
        ax[1].set_zorder(2)
        ax[1].set_frame_on(False)

        # ax.set_title(file + ' - ${}^{85m}$Kr')
        ax[1].set_xlabel('Burnup (GWd/tU)')
        ax[1].set_ylabel('Release-to-birth ratio (/)')
        ax[1].legend()
        ax[1].set_yscale('log')
        ax[1].set_ylim(1e-5, 1.0)

        h1, l1 = ax[1].get_legend_handles_labels()
        h2, l2 = axT.get_legend_handles_labels()
        ax[1].legend(h1+h2, l1+l2, loc='lower right')

        # plt.savefig('CONTACT1_Kr85m.png')
        plt.show()

      os.chdir('..')
        
  return folderList, number_of_tests, number_of_tests_failed