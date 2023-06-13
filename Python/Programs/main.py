##################################################################################################
# Name: main.py                                                                                  #
# Description: Program to Run Project                                                            #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################




## Path to root folder
root_path = "/Users/jameswright/Desktop/accidents-data-analysis"

print(root_path)

#---------------------------------------- Do not unintentionally edit below this line ---------------------------------------- 


## Import required libraries
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Set up paths to file structure
raw_data_path = Path(root_path+"/Python"+"/Data"+"/Raw")
print(raw_data_path)
cleaned_data_path = Path(root_path+"/Python"+"/Data"+"/Cleaned")
print(cleaned_data_path)
programs_path = Path(root_path+"/Python"+"/Programs")
print(programs_path)

## Run data import program
with open(programs_path/"data_import.py") as data_import:
    exec(data_import.read())


## Run data transformation progam
with open(programs_path/"data_transformation.py") as data_transformation:
    exec(data_transformation.read())


## Run data analysis program
with open(programs_path/"data_analysis.py") as data_analysis:
    exec(data_analysis.read())


## Run hypothesis testing program
with open(programs_path/"hypothesis_testing.py") as hypothesis_testing:
    exec(hypothesis_testing.read())