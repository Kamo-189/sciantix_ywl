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

from regression_baker import regression_baker
from regression_white import regression_white
from regression_talip import regression_talip
from regression_contact import regression_contact
from regression_oxidation import regression_oxidation

" ------------------- Main part -------------------"
def main():
    # Stocking the directory path of the current file
    wpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(wpath)

    # Initialising different variable needed for the execution :

    # - A list of folder to stock every test that will be executed
    folderList = folderListB = folderListW = folderListT = folderListC = folderListO = []
    # - Number of executed test
    number_of_tests = number_of_tests_b = number_of_tests_w = number_of_tests_t = number_of_tests_c = number_of_tests_o = 0
    # - Number of failed test
    number_of_tests_failed = number_of_tests_failed_b = number_of_tests_failed_w = number_of_tests_failed_t = number_of_tests_failed_c = number_of_tests_failed_o = 0


    # Specific version for the pipeline environment with default values
    # (each test is executed with sciantix, and no modifications of gold)
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        # Default values
        mode_gold = 0
        mode_plot = 0
        mode_Baker = 1
        mode_White = 1
        mode_Talip = 1
        mode_CONTACT = 1
        mode_oxidation = 1

        folderListB, number_of_tests_b, number_of_tests_failed_b = regression_baker(wpath, mode_Baker, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListW, number_of_tests_w, number_of_tests_failed_w = regression_white(wpath, mode_White, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListT, number_of_tests_t, number_of_tests_failed_t = regression_talip(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListC, number_of_tests_c, number_of_tests_failed_c = regression_contact(wpath, mode_CONTACT, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListO, number_of_tests_o, number_of_tests_failed_o = regression_oxidation(wpath, mode_oxidation, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)

        folderList = folderListB + folderListW + folderListT + folderListC + folderListO
        number_of_tests = number_of_tests_b + number_of_tests_w + number_of_tests_t + number_of_tests_c + number_of_tests_o
        number_of_tests_failed = number_of_tests_failed_b + number_of_tests_failed_w + number_of_tests_failed_t + number_of_tests_failed_c + number_of_tests_failed_o



    # For user utilisation :
    # 0 : default
    # 1 : choose all inputs


    # Chosing the type of execution, default values or given by the user
    print("\n-----------------This script executes SCIANTIX into the validation cases-----------------\n")
    print("\tExecution option == 0 USE DEFAULT MODES")
    print("\tExecution option == 1 PERSONALISED MODES")
    execution_option = int(input("\nEnter Execution option (0, 1) = "))

    # Case of default values with all regressions
    if execution_option == 0 :

        # Default values
        mode_Baker = 1
        mode_White = 1
        mode_Talip = 1
        mode_CONTACT = 1
        mode_oxidation = 1

        # Chosing the gold mode
        print("Pleast select one option for the GOLD MODE :\n")
        print("\tMODE GOLD == 0: use S"
              "CIANTIX, check new results.\n")
        print("\tMODE GOLD == 1: use SCIANTIX, new results will be saved as gold results.\n ")
        print("\tMODE GOLD == 2: do not use SCIANTIX, check existing results.\n ")
        print("\tMODE GOLD == 3: do not use SCIANTIX, existing results will be saved as gold results.\n ")

        mode_gold = int(input("Enter MODE GOLD (0, 1, 2, 3)= "))

        # Chosing the if you want to show the different plot
        mode_plot = int(input("Enter MODE PLOT (0 or 1)= "))

        folderListB, number_of_tests_b, number_of_tests_failed_b = regression_baker(wpath, mode_Baker, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListW, number_of_tests_w, number_of_tests_failed_w = regression_white(wpath, mode_White, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListT, number_of_tests_t, number_of_tests_failed_t = regression_talip(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListC, number_of_tests_c, number_of_tests_failed_c = regression_contact(wpath, mode_CONTACT, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListO, number_of_tests_o, number_of_tests_failed_o = regression_oxidation(wpath, mode_oxidation, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)

        folderList = folderListB + folderListW + folderListT + folderListC + folderListO
        number_of_tests = number_of_tests_b + number_of_tests_w + number_of_tests_t + number_of_tests_c + number_of_tests_o
        number_of_tests_failed = number_of_tests_failed_b + number_of_tests_failed_w + number_of_tests_failed_t + number_of_tests_failed_c + number_of_tests_failed_o


    # Case where the user chose values
    if execution_option == 1 :

        # Chosing the type of regression : Baker, White, Talip, Contact, Oxidation
        print("Possible regression options \n")
        print("Baker : 0\nWhite : 1\nTalip : 2\nContact : 3\nOxidation : 4\n")

        regression_mode = int(input("Enter the chosen regression (0, 1, 2, 3, 4) = "))

        # Chosing the gold mode
        print("Pleast select one option for the GOLD MODE :\n")
        print("\tMODE GOLD == 0: use SCIANTIX, check new results.\n")
        print("\tMODE GOLD == 1: use SCIANTIX, new results will be saved as gold results.\n ")
        print("\tMODE GOLD == 2: do not use SCIANTIX, check existing results.\n ")
        print("\tMODE GOLD == 3: do not use SCIANTIX, existing results will be saved as gold results.\n ")

        mode_gold = int(input("Enter MODE GOLD (0, 1, 2, 3)= "))

        # Chosing the if you want to show the different plot
        mode_plot = int(input("Enter MODE PLOT (0 or 1)= "))

        if regression_mode == 0 :
            mode_Baker = 1
            folderList, number_of_tests, number_of_tests_failed = regression_baker(wpath, mode_Baker, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
            print("\nRegression selected : Baker")
        if regression_mode == 1 :
            mode_White = 1
            folderList, number_of_tests, number_of_tests_failed = regression_white(wpath, mode_White, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
            print("\nRegression selected : White")
        if regression_mode == 2 :
            print("Talip doesn't work right now")
            main()
            """mode_Talip = 1
            folderList, number_of_tests, number_of_tests_failed = regression_talip(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
            print("\nRegression selected : Talip")"""
        if regression_mode == 3 :
            mode_CONTACT = 1
            folderList, number_of_tests, number_of_tests_failed = regression_contact(wpath, mode_CONTACT, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
            print("\nRegression selected : Contact")
        if regression_mode == 4 :
            mode_oxidation = 1
            folderList, number_of_tests, number_of_tests_failed = regression_oxidation(wpath, mode_oxidation, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
            print("\nRegression selected : Oxidation")


    print("MODE GOLD ==", mode_gold, "selected.")
    print("MODE PLOT ==", mode_plot, "selected.\n")

    print("-----------------SUMMARY-----------------")
    print("- List of tests performed:\n", folderList, "\n")
    print("! Number of tests = ", number_of_tests)
    print("! Number of tests passed = ", number_of_tests - number_of_tests_failed)
    print("! Number of tests failed = ", number_of_tests_failed, "\n")

if __name__ == "__main__":
    main()
