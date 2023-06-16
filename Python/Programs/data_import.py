##################################################################################################
# Name: data_import.py                                                                           #
# Description: Program to Import Study Data                                                      #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################




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

# Make accident index column the index
#- 0 Duplicates in this index, makes sense as every accident should be unique - can use later without worry.
#- All rows accounted for.
print('--- Accidents Data Index Check ---')
print('Index Duplicates Accidents:', accidents_uncleaned_df[accidents_uncleaned_df['index'].duplicated()]['index'].count())
print('Number of Indicies Accidents (Non-Missing):', accidents_uncleaned_df['index'].count())
print('Overall Accidents Data Rows:', accidents_uncleaned_df.shape[0])
print('-----------------------------------')
accidents_uncleaned_df.set_index('index', inplace=True)



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

# Make accident index column the index for convenience in data_transformation stage
#- 44763 Duplicates in this index, makes sense as multiple casualties per accident can occur, handle with care later.
#- All rows accounted for.
print('--- Casualties Data Index Check ---')
print('Index Duplicates Casualties:', casualties_uncleaned_df[casualties_uncleaned_df['index'].duplicated()]['index'].count())
print('Number of Indicies Casualties (Non-Missing):', casualties_uncleaned_df['index'].count())
print('Overall Casualties Data Rows:', casualties_uncleaned_df.shape[0])
print('-----------------------------------')
casualties_uncleaned_df.set_index('index', inplace=True)



### Import vehicles data


## Load data
# Define -1 as possible missing values - safe to do as none of these columns should be -1 otherwise.
vehicles_uncleaned_df = pd.read_csv(raw_data_path/"vehicles.csv",
                                      na_values=['-1', 'Data missing or out of range'])


## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform vehicle_ref from int64 to object as it is just a reference number with no mathematical meaning
vehicles_uncleaned_df = vehicles_uncleaned_df.astype({'vehicle_ref' : 'object'})


# Make accident index column the index
#- 115879 Duplicates in this index, makes sense as multiple vehicles can occur in an accident, handle with care later.
#- All rows accounted for.
print('--- Vehicles Data Index Check ---')
print('Index Duplicates Vehicles:', vehicles_uncleaned_df[vehicles_uncleaned_df['index'].duplicated()]['index'].count())
print('Number of Indicies Vehicles (Non-Missing):', vehicles_uncleaned_df['index'].count())
print('Overall Vehicles Data Rows:', vehicles_uncleaned_df.shape[0])
print('-----------------------------------')
vehicles_uncleaned_df.set_index('index', inplace=True)



### Import population statistics data


## Load data
population_statistics_uncleaned_df = pd.read_csv(raw_data_path/"population_statistics.csv",
                                                 na_values=['-1', 'Data missing or out of range'])

# Add London Airport (Heathrow) to population data with average daily passengers in 2016
heathrow_code = pd.DataFrame(data={'Code' : ['EHEATHROW'],
                                   'Area_Name' : ['London Airport (Heathrow)'],
                                   'Population' : ['206,800']})
population_statistics_uncleaned_df = pd.concat([population_statistics_uncleaned_df, heathrow_code], axis=0, ignore_index=True)


## Structure data types and indices for loaded data appropriately

# Correct default loaded data types
#- Transform population comma-separated string data type from string to int: first regex to replace non-integers with nothing, then convert to numeric
population_statistics_uncleaned_df['Population'] = pd.to_numeric(population_statistics_uncleaned_df['Population'].str.replace('[^0-9]', '')).astype('int')

# Make Code column the index - tested and contains no duplicates so safe to do so
#- 0 Duplicates in this index, makes sense as one area should have one code - can use without worry
#- All rows accounted for.
print('--- Population Data Index Check ---')
print('Index Duplicates Population:', population_statistics_uncleaned_df[population_statistics_uncleaned_df['Code'].duplicated()]['Code'].count())
print('Number of Indicies Population (Non-Missing):', population_statistics_uncleaned_df['Code'].count())
print('Overall Population Data Rows:', population_statistics_uncleaned_df.shape[0])
print('-----------------------------------')
population_statistics_uncleaned_df.set_index('Code', inplace=True)









#### Let know completed stage in terminal
print('NOTE: Data Imported.')