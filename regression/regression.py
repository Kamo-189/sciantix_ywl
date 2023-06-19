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
from regression_talip_old import regression_talip_old
from regression_contact import regression_contact
from regression_oxidation import regression_oxidation


def remove_output(file):
    os.chdir(file)
    print(f"Now in folder {file}...")
    print(os.listdir('.'))
    try :
        os.remove("output.txt")
    except :
        print("no output.txt")
    print(os.listdir('.'))
    os.chdir('..')

" ------------------- Main part -------------------"
def main():

    print(os.listdir('.'))
    shutil.copy("../bin/sciantix.x", os.getcwd())
    print(os.listdir('.'))

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
        folderListT, number_of_tests_t, number_of_tests_failed_t = regression_talip_old(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListC, number_of_tests_c, number_of_tests_failed_c = regression_contact(wpath, mode_CONTACT, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
        folderListO, number_of_tests_o, number_of_tests_failed_o = regression_oxidation(wpath, mode_oxidation, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)

        folderList = folderListB + folderListW + folderListT + folderListC + folderListO
        number_of_tests = number_of_tests_b + number_of_tests_w + number_of_tests_t + number_of_tests_c + number_of_tests_o
        number_of_tests_failed = number_of_tests_failed_b + number_of_tests_failed_w + number_of_tests_failed_t + number_of_tests_failed_c + number_of_tests_failed_o



    if os.environ.get('GITHUB_ACTIONS') != 'true':
        # For user utilisation :
        # 0 : default
        # 1 : choose all inputs


        # Chosing the type of execution, default values or given by the user
        print("\n-----------------This script executes SCIANTIX into the validation cases-----------------\n")
        print("\tExecution option == 0 USE DEFAULT MODES")
        print("\tExecution option == 1 PERSONALISED MODES")
        print("\tExecution option == 2 REMOVE ALL OUTPUT FILES")
        execution_option = int(input("\nEnter Execution option (0, 1, 2) = "))

        # Case where we just remove all output files
        if execution_option == 2 :
            for file in os.listdir(wpath):
                if "Baker" in file and os.path.isdir(file) is True:
                    remove_output(file)
                if "White" in file and os.path.isdir(file) is True:
                    remove_output(file)
                if "Talip" in file and os.path.isdir(file) is True:
                    remove_output(file)
                if "CONTACT" in file and os.path.isdir(file) is True:
                    remove_output(file)
                if "oxidation" in file and os.path.isdir(file) is True:
                    remove_output(file)
                mode_gold = -1
                mode_plot = -1

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
                mode_Talip = 1
                which_Talip = int(input("Enter Which Talip : - New : 0 / - Old : 1 "))
                if which_Talip == 0:
                    folderList, number_of_tests, number_of_tests_failed = regression_talip(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)
                if which_Talip == 1:
                    folderList, number_of_tests, number_of_tests_failed = regression_talip_old(wpath, mode_Talip, mode_gold, mode_plot, folderList, number_of_tests, number_of_tests_failed)

            print("\nRegression selected : Talip")
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
