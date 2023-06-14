##################################################################################################
# Name: data_import.py                                                                           #
# Description: Program to Import Study Data                                                      #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################
#### Import required libraries - temporary
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#### Segregating Data Import Section In Terminal Output
print('\n ---------------------------------------- Data Import ---------------------------------------- \n')




#### Importing Data



### Import accidents data


## Load data
#- Define '-1' as possible missing values - safe to do as none of these columns should be -1 otherwise.
#- Defining 'Data missing or out of range' as defined in documentation as -1 equivalent
accidents_uncleaned_df = pd.read_csv(raw_data_path/"accidents.csv",
                                      na_values=['-1', 'Data missing or out of range'])


## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform date to datetime
accidents_uncleaned_df['date'] = pd.to_datetime(accidents_uncleaned_df['date'], 
                                                format='%d%b%Y', 
                                                errors='coerce')
#- Transform time to datetime
accidents_uncleaned_df['time'] = pd.to_datetime(accidents_uncleaned_df['time'], 
                                                format='%H:%M', 
                                                errors='coerce')

print(accidents_uncleaned_df['speed_limit'].unique())

# Make index column the index
print('Duplicates accidents:', accidents_uncleaned_df[accidents_uncleaned_df['index'].duplicated()]['index'].count())
print('Overall accidents:', accidents_uncleaned_df['index'].count())
#accidents_uncleaned_df.set_index('index', inplace=True)



### Import casualties data


## Load data
# Define -1 as possible missing values - safe to do as none of these columns should be -1 otherwise.
casualties_uncleaned_df = pd.read_csv(raw_data_path/"casualties.csv",
                                      na_values=['-1', 'Data missing or out of range'])



## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform vehicle_ref and casualty_ref from int64 to object as they are just a reference number with no mathematical meaning
casualties_uncleaned_df = casualties_uncleaned_df.astype({'vehicle_ref' : 'object',
                                                          'casualty_ref' : 'object'})

# Make index column the index
print('Duplicates Casualties:', casualties_uncleaned_df[casualties_uncleaned_df['index'].duplicated()]['index'].count())
print('Overall Casualties:', casualties_uncleaned_df['index'].count())
#casualties_uncleaned_df.set_index('index', inplace=True)



### Import vehicles data


## Load data
# Define -1 as possible missing values - safe to do as none of these columns should be -1 otherwise.
vehicles_uncleaned_df = pd.read_csv(raw_data_path/"vehicles.csv",
                                      na_values=['-1', 'Data missing or out of range'])


## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform vehicle_ref from int64 to object as it is just a reference number with no mathematical meaning
vehicles_uncleaned_df = vehicles_uncleaned_df.astype({'vehicle_ref' : 'object'})


# Make index column the index
print('Duplicates Vehicle:', vehicles_uncleaned_df[vehicles_uncleaned_df['index'].duplicated()]['index'].count())
print('Overall Vehicle:',vehicles_uncleaned_df['index'].count())
#vehicles_uncleaned_df.set_index('index', inplace=True)



### Import population statistics data


## Load data
population_statistics_uncleaned_df = pd.read_csv(raw_data_path/"population_statistics.csv",
                                                 na_values=['-1', 'Data missing or out of range'])


## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform population comma-separated string data type from string to int: first regex to replace non-integers with nothing, then convert to numeric
population_statistics_uncleaned_df['Population'] = pd.to_numeric(population_statistics_uncleaned_df['Population'].str.replace('[^0-9]', ''))

# Make Code column the index - tested and contains no duplicates so safe to do so
# population_statistics_uncleaned_df.set_index('Code', inplace=True)




#### Create a dictionary of data frame names
df_dict = {'Casualties' : casualties_uncleaned_df,
           'Vehicles' : vehicles_uncleaned_df,
           'Accidents' : accidents_uncleaned_df,
           'Population' : population_statistics_uncleaned_df}




#### Let know completed stage in terminal
print('NOTE: Data Imported.')