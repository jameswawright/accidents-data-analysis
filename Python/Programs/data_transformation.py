##################################################################################################
# Name: data_transformation.py                                                                   #
# Description: Program to Clean Data                                                             #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################




#### Segregating Data Transformation Section In Terminal Output
print('\n ---------------------------------------- Data Transformation ---------------------------------------- \n')




#### Create a dictionary of uncleaned data frame names
df_dict = {'Casualties' : casualties_uncleaned_df,
           'Vehicles' : vehicles_uncleaned_df,
           'Accidents' : accidents_uncleaned_df,
           'Population' : population_statistics_uncleaned_df}





#### Report on Missing Values



### Computing missing values table for all data frames


## Initalising Missing Data Table To Append Missing Count Values To
missing = pd.DataFrame(columns=['Table','Column','Number_Missing'])


## Append Missing Values Count To Missing For Each Data Frame

# Iterate over dictionary of dataframes, excluding population dataframe from dictionary iterated over
for key in {old_key : df_dict[old_key] for old_key in df_dict if old_key !='Population'}:

    # Count missing values in each data frame in dictionary, label index as column, reset index to turn series into data frame with missing count as number_missing
    df_missing = df_dict[key].isna().sum().rename_axis('Column').reset_index(name='Number_Missing')

    # Insert column with data frame name the variable is from
    df_missing.insert(0,'Table',key)

    # Append missing data frame counts to missing data table, each successive data frame
    missing = pd.concat([missing, df_missing], axis=0, ignore_index=True)


## Sort missing dataframe by missing count
missing.sort_values(by='Number_Missing', 
                    ascending=False, 
                    inplace=True, 
                    ignore_index = True)



### Output Missing Data Report CSV to Report Folder

# Export Missing Counts to CSV
missing.to_csv(reports_path/'missing.csv', 
               index=False, 
               header=missing.columns)

print('Note: Missing Data Report Exported To CSV.')




#### Copy for cleaning


## Copy dataframes

# Copy casualties
casualties_df = casualties_uncleaned_df.copy()

# Copy vehicles
vehicles_df = vehicles_uncleaned_df.copy()

# Copy accidents
accidents_df = accidents_uncleaned_df.copy()

# Copy population
population_statistics_df = population_statistics_uncleaned_df.copy()


## Create a dictionary of data frame names
df_dict_cleaned = {'Casualties' : casualties_df,
           'Vehicles' : vehicles_df,
           'Accidents' : accidents_df,
           'Population' : population_statistics_df}




#### Handling Missing Values



### Missing Values in Accidents


## Drop speed_limit column as entirely missing and not needed for analysis
accidents_df = accidents_df.drop(['speed_limit'], axis='columns')


## Assign Missing Road Type To Unknown
accidents_df[['road_type']] = accidents_df[['road_type']].fillna('Unknown')


## Assign Missing Time Values



## Assign Missing Weather Values To Unknown
accidents_df[['weather']] = accidents_df[['weather']].fillna('Unknown')


## Assign Missing Light Condition Values

# Assign 'Darkness - lighting unknown' to winter months between 6pm and 9am
accidents_df[['light_conditions']] = accidents_df.loc[((accidents_df['time'].dt.hour < 9) | (accidents_df['time'].dt.hour > 17)) &
                                                    ((accidents_df['date'].dt.month > 9) & (accidents_df['date'].dt.month < 4))][['light_conditions']].fillna('Darkness - lighting unknown')

# Assign 'Daylight' to winter months between 9am and 6pm
accidents_df[['light_conditions']] = accidents_df.loc[((accidents_df['time'].dt.hour >= 9) & (accidents_df['time'].dt.hour <= 17)) &
                                                    ((accidents_df['date'].dt.month > 9) & (accidents_df['date'].dt.month < 4))][['light_conditions']].fillna('Daylight')


# Assign 'Darkness - lighting unknown' to summer months between 9pm and 7am
accidents_df[['light_conditions']] = accidents_df.loc[((accidents_df['time'].dt.hour < 7) | (accidents_df['time'].dt.hour > 21)) &
                                                    ((accidents_df['date'].dt.month <= 9) | (accidents_df['date'].dt.month >= 4))][['light_conditions']].fillna('Darkness - lighting unknown')

# Assign 'Daylight' to summer months between 7am and 9pm
accidents_df[['light_conditions']] = accidents_df.loc[((accidents_df['time'].dt.hour >= 7) & (accidents_df['time'].dt.hour <= 21)) &
                                                    ((accidents_df['date'].dt.month <= 9) | (accidents_df['date'].dt.month >= 4))][['light_conditions']].fillna('Daylight')


## Assign Missing Junction Detail Values

print(accidents_df['junction_detail'].unique())


## Assign Missing Pedestrian Crossing Detail Values

print(accidents_df['pedestrian_crossing_human'].unique())


## Assign Missing Site Condition Values

print(accidents_df['site_conditions'].unique())


## Assign Missing Carriageway Hazard Values

print(accidents_df['carriageway_hazards'].unique())


## Assign Missing Pedestrian Crossing Physical Values

print(accidents_df['pedestrian_crossing_physical'].unique())


## Assign Missing Road Condition Values

print(accidents_df['road_conditions'].unique())


## Assign Missing Junction Control Values

print(accidents_df['junction_control'].unique())



### Missing Values in Casualties


## Assign Location Values
print(casualties_df['location'].unique())


## Assign Missing Pedestrian Movement Values
print(casualties_df['pedestrian_movement'].unique())


## Assign Missing bus or coach passenger Values
print(casualties_df['bus_or_coach_passenger'].unique())


## Assign Missing Casualty Sex Values
print(casualties_df['casualty_sex'].unique())


## Assign Missing Car Passenger Values
print(casualties_df['car_passenger'].unique())


## Assign Missing Car Passenger Values
print(casualties_df['casualty_age'].unique())


### Missing Values in Vehicles


## Assign Missing Driver Sex Values
print(vehicles_df['driver_sex'].unique())


## Assign Missing Vehicle Type Values
print(vehicles_df['vehicle_type'].unique())


## Assign Missing Off Carriageway Values
print(vehicles_df['hit_object_off_carriageway'].unique())


## Assign Missing Junction Location Values
print(vehicles_df['junction_location'].unique())


## Assign Missing Skidding Values
print(vehicles_df['skidding_and_overturning'].unique())


## Assign Missing Towing Values
print(vehicles_df['towing_and_articulation'].unique())


## Assign Missing Manoeuvre Values
print(vehicles_df['vehicle_manoeuvre'].unique())


## Assign Missing Leaving Carriageway Values
print(vehicles_df['vehicle_leaving_carriageway'].unique())


## Assign Missing Left Hand Drive Values
print(vehicles_df['left_hand_drive'].unique())


## Assign Missing Hit Object Values
print(vehicles_df['hit_object_in_carriageway'].unique())


## Assign Missing Impact Values
print(vehicles_df['impact'].unique())


## Assign Missing Driver Age Values
print(vehicles_df['driver_age'].unique())


## Assign Missing Propulsion Code Values
print(vehicles_df['propulsion_code'].unique())


## Assign Missing Vehicle Age Values
print(vehicles_df['vehicle_age'].unique())



### Missing Values in Population





#### Formatting Columns Entries For Each Table



### Format Equivalent Unique Values So That They Are Read The Same By Python (e.g. same case)


## Convert Case Of All 'String' Columns To Title Case - keep population unchanged as case has meaning

# Change accidents string objects to title case in each data frame
accidents_df = accidents_df.applymap(lambda column: column.title() if type(column) == str else column)

# Change casualties string objects to title case in each data frame
casualties_df = casualties_df.applymap(lambda column: column.title() if type(column) == str else column)

# Change vehicle string objects to title case in each data frame
vehicles_df = vehicles_df.applymap(lambda column: column.title() if type(column) == str else column)


## Update a dictionary with cleaned entry data frames
df_dict_cleaned.update({'Casualties' : casualties_df,
           'Vehicles' : vehicles_df,
           'Accidents' : accidents_df,
           'Population' : population_statistics_df})




#### Handling Duplicates



### Computing duplicate row count table and table of unique value count per column for all data frames


## Initalising Duplicate Data Table To Append Duplicate Row Count Per Table To
duplicates = pd.DataFrame(columns=['Table', 'Number_Duplicate_Rows'])


## Initialising Unique Data Table To Append Unique Values Counted Per Column Of Each Table To
unique = pd.DataFrame(columns=['Table', 'Column', 'Unique_Value', 'Number_Values'])


## Append Duplicate and Unique Counts Per Table to Each Dataframe Initialised Above

# Iterate over dictionary of dataframes
for key in df_dict_cleaned:

    # Count duplicated values in each data frame in dictionary, label index as column, reset index to turn series into data frame with missing count as number_missing
    df_duplicates = pd.DataFrame({'Table' : [key], 
                                  'Number_Duplicate_Rows' : [df_dict_cleaned[key].duplicated().sum()]})
    
    # Counts of each unique value in each column - only objects as numerics would be huge and shouldn't be very unique anyway
    df_unique = df_dict_cleaned[key].select_dtypes(include='object').melt(var_name='Column', value_name='Unique_Value').value_counts().reset_index(name='Number_Values')

    # Insert column with data frame name the variable is from
    df_unique.insert(0,'Table',key)
    
    # Append duplicate data frame counts to duplicate data table, each successive data frame
    duplicates = pd.concat([duplicates, df_duplicates], axis=0, ignore_index=True)

    # Append unique data frame counts to unqiue data table, each successive data frame
    unique = pd.concat([unique, df_unique], axis=0, ignore_index=True)


## Sort duplicates dataframe by missing count
duplicates.sort_values(by='Number_Duplicate_Rows', 
                    ascending=False, 
                    inplace=True, 
                    ignore_index = True)


## Sort missing dataframe by table and column
unique.sort_values(by=['Table', 'Column'], 
                    ascending=False, 
                    inplace=True, 
                    ignore_index = True)



### Output Unique Data Reports CSV to Report Folder

# Export Duplicate Counts to CSV
duplicates.to_csv(reports_path/'duplicates.csv', 
               index=False, 
               header=duplicates.columns)

# Export Duplicate Counts to CSV
unique.to_csv(reports_path/'unique.csv', 
               index=False, 
               header=unique.columns)

print('Note: Duplicate Data Reports Exported To CSV.')




#### Create New Accidents Columns



### Country Column

# Use starting value of highway code to identify country
accidents_df['Country'] = np.select(condlist=[accidents_df['highway_authority'].str.startswith('E'), 
                                              accidents_df['highway_authority'].str.startswith('S'), 
                                              accidents_df['highway_authority'].str.startswith('W'), 
                                              accidents_df['highway_authority'].str.startswith('N'), 
                                              False],
                                    choicelist=['England', 
                                                'Scotland', 
                                                'Wales', 
                                                'Northern Ireland', 
                                                'Unknown'])



### Weekday Column

# Obtain weekday from date
accidents_df['Weekday'] = accidents_df['date'].dt.day_name()



### Season Column

# Use date months to identify season
accidents_df['Season'] = np.select(condlist=[(accidents_df['date'].dt.month >= 12) | (accidents_df['date'].dt.month < 3), 
                                             (accidents_df['date'].dt.month >= 3) & (accidents_df['date'].dt.month < 6),
                                             (accidents_df['date'].dt.month >=6) & (accidents_df['date'].dt.month < 9), 
                                             (accidents_df['date'].dt.month >= 9) & (accidents_df['date'].dt.month < 12),
                                             False],
                                    choicelist=['Winter', 
                                                'Spring', 
                                                'Summer', 
                                                'Autumn',
                                                'Unknown'])





#### Create New Casualties Columns



### Number of Casualties Per Accident Column

# Group by index (unique accident), count number of unique casualty reference numbers
casualties_df['casualties_per_accident'] = casualties_df.reset_index().groupby(['index'])['casualty_ref'].agg(['nunique'])




#### Create New Vehicles Columns



### Number of Vehicles Per Accident Column

# Group by index (unique accident), count number of unique vehicle reference numbers
vehicles_df['vehicles_per_accident'] = vehicles_df.reset_index().groupby(['index'])['vehicle_ref'].agg(['nunique'])








#### Create Road_Accidents



### Combining Accidents, Casualties, Vehicles



### Merging Population Statistics