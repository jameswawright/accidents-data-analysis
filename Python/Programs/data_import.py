##################################################################################################
# Name: data_import.py                                                                           #
# Description: Program to Import Study Data                                                      #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################


## Segregating Data Import Section In Terminal
print('\n ---------------------------------------- Data Import ---------------------------------------- \n')


## Importing Data

# Import accients data
accidents_uncleaned_df = pd.read_csv(raw_data_path/"accidents.csv")
print(accidents_uncleaned_df.dtypes)
print(accidents_uncleaned_df.head(10))

# Import accients data
casualties_uncleaned_df = pd.read_csv(raw_data_path/"casualties.csv")
print(casualties_uncleaned_df.dtypes)
print(casualties_uncleaned_df.head(10))

# Import vehicles data
vehicles_uncleaned_df = pd.read_csv(raw_data_path/"vehicles.csv")
print(vehicles_uncleaned_df.dtypes)
print(vehicles_uncleaned_df.head(10))

# Import population statistics data
population_statistics_uncleaned_df = pd.read_csv(raw_data_path/"population_statistics.csv")
print(population_statistics_uncleaned_df.dtypes)
print(population_statistics_uncleaned_df.head(10))