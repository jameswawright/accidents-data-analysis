##################################################################################################
# Name: main.py                                                                                  #
# Description: Program to Run Project                                                            #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################




#### Path to root folder
root_path = "/Users/jameswright/Desktop/accidents-data-analysis"




#---------------------------------------- Do not unintentionally edit below this line ---------------------------------------- 




#### Import required libraries
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns




#### Set up paths to file structure


## Data paths

# Path to raw data folder
raw_data_path = Path(root_path+"/Python"+"/Data"+"/Raw")

# Path to cleaned data folder
cleaned_data_path = Path(root_path+"/Python"+"/Data"+"/Cleaned")


## Reports paths

# Path to report data folder
reports_path = Path(root_path+"/Python"+"/Reports")


## Program paths

# Path to programs folder
programs_path = Path(root_path+"/Python"+"/Programs")




#### Run data import program
with open(programs_path/"data_import.py") as data_import:
    exec(data_import.read())




#### Run data transformation progam
with open(programs_path/"data_transformation.py") as data_transformation:
    exec(data_transformation.read())




#### Run data analysis program
with open(programs_path/"data_analysis.py") as data_analysis:
    exec(data_analysis.read())




#### Run hypothesis testing program
with open(programs_path/"hypothesis_testing.py") as hypothesis_testing:
    exec(hypothesis_testing.read())