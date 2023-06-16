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
for key in df_dict.keys():

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


## Copy dataframes to avoid editing original

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




#### Formatting Columns Entries For Each Table



### Format Equivalent Unique Values So That They Are Read The Same By Python (e.g. same case)


## Convert Case Of All 'String' Columns To Title Case - keep population unchanged as case has meaning

# Change accidents string objects to title case in each data frame
accidents_df = accidents_df.applymap(lambda column: column.title() if type(column) == str else column)

# Change casualties string objects to title case in each data frame
casualties_df = casualties_df.applymap(lambda column: column.title() if type(column) == str else column)

# Change vehicle string objects to title case in each data frame
vehicles_df = vehicles_df.applymap(lambda column: column.title() if type(column) == str else column)


## Remove leading/trailing dots and spaces from columns

# Remove accidents leading/trailing dots and spaces from column strings
accidents_df = accidents_df.applymap(lambda column: column.strip('.! ') if type(column) == str else column)

# Remove casualties leading/trailing dots and spaces from column strings
casualties_df = casualties_df.applymap(lambda column: column.strip('.! ') if type(column) == str else column)

# Remove vehicle leading/trailing dots and spaces from column strings
vehicles_df = vehicles_df.applymap(lambda column: column.strip('.! ') if type(column) == str else column)



### Update a dictionary with cleaned entry data frames
df_dict_cleaned.update({'Casualties' : casualties_df,
           'Vehicles' : vehicles_df,
           'Accidents' : accidents_df,
           'Population' : population_statistics_df})


#### Handling Missing Values and Formats



### Missing Values and Formats in Accidents


## Drop columns with more than half of entires missing if not needed for later analysis

# Drop speed limit, junction control
accidents_df = accidents_df.drop(['speed_limit', 'junction_control'], axis='columns')


## Assign Missing Road Type To Unknown Category

# Replace NA's with 'Unknown'
accidents_df['road_type'].fillna('Unknown', inplace=True)


## Assign Missing Time Values
print(accidents_df.columns)
print(accidents_df[accidents_df['time'].isna()][['time', 'light_conditions', 'site_conditions']])


## Assign Missing Weather Values To Unknown Category

# Replace NA's with 'Unknown'
accidents_df['weather'].fillna('Unknown', inplace=True)


## Assign Missing Light Condition Values

# Assign 'Darkness - lighting unknown' to winter months between 6pm and 9am
winter_night = ((accidents_df['time'].dt.hour < 9) | (accidents_df['time'].dt.hour > 17)) & ((accidents_df['date'].dt.month > 9) | (accidents_df['date'].dt.month < 4))
accidents_df.loc[winter_night, 'light_conditions'] = accidents_df.loc[winter_night, 'light_conditions'].fillna('Darkness - Lighting Unknown')

# # Assign 'Daylight' to winter months between 9am and 6pm
winter_day = ((accidents_df['time'].dt.hour >= 9) & (accidents_df['time'].dt.hour <= 17)) & ((accidents_df['date'].dt.month > 9) | (accidents_df['date'].dt.month < 4))
accidents_df.loc[winter_day, 'light_conditions'] = accidents_df.loc[winter_day, 'light_conditions'].fillna('Daylight')

# Assign 'Darkness - lighting unknown' to summer months between 9pm and 7am
summer_night = ((accidents_df['time'].dt.hour < 7) | (accidents_df['time'].dt.hour >= 21)) & ((accidents_df['date'].dt.month <= 9) & (accidents_df['date'].dt.month >= 4))
accidents_df.loc[summer_night, 'light_conditions'] = accidents_df.loc[summer_night, 'light_conditions'].fillna('Darkness - Lighting Unknown')

# Assign 'Daylight' to summer months between 7am and 9pm
summer_day = ((accidents_df['time'].dt.hour >= 7) & (accidents_df['time'].dt.hour < 21)) & ((accidents_df['date'].dt.month <= 9) & (accidents_df['date'].dt.month >= 4))
accidents_df.loc[summer_day, 'light_conditions'] = accidents_df.loc[summer_day, 'light_conditions'].fillna('Daylight')


## Assign Missing Junction Detail Values

# Turn junction details to same format, assign NA's to 'Unknown'
accidents_df['junction_detail'] = np.select(condlist=[accidents_df['junction_detail'] == 'Notatjunctionorwithin20metres',
                                                      accidents_df['junction_detail'] == 'Otherjunction',
                                                      accidents_df['junction_detail'] == 'Torstaggeredjunction',
                                                      accidents_df['junction_detail'] == 'Morethan4arms(notroundabout)',
                                                      accidents_df['junction_detail'] == 'Privatedriveorentrance',
                                                      accidents_df['junction_detail'] == 'Sliproad',
                                                      accidents_df['junction_detail'].isna()],
                                            choicelist=['Not At junction or within 20 metres',
                                                        'Other Junction',
                                                        'T Or Staggered Junction',
                                                        'More Than 4 Arms (Not Roundabout)',
                                                        'Private Drive Or Entrance',
                                                        'Slip Road',
                                                        'Unknown'],
                                            default=accidents_df['junction_detail'])


## Assign Missing Pedestrian Crossing Detail Values

# Replace NA's with 'Unknown'
accidents_df['pedestrian_crossing_human'].fillna('Unknown', inplace=True)


## Assign Missing Site Condition Values

# Replace NA's with 'Unknown'
accidents_df['site_conditions'].fillna('Unknown', inplace=True)


## Assign Missing Carriageway Hazard Values

# Replace NA's with 'Unknown'
accidents_df['carriageway_hazards'].fillna('Unknown', inplace=True)


## Assign Missing Pedestrian Crossing Physical Values

# Replace NA's with 'Unknown'
accidents_df['pedestrian_crossing_physical'].fillna('Unknown', inplace=True)


## Assign Missing Road Condition Values

# Imputing using typical road condition by weather type
accidents_df['road_conditions'] = np.select(condlist=[accidents_df['weather'].str.contains('Fine') & accidents_df['road_conditions'].isna(), 
                                                      accidents_df['weather'].str.contains('Raining') & accidents_df['road_conditions'].isna(), 
                                                      accidents_df['weather'].str.contains('Snowing') & accidents_df['road_conditions'].isna(),
                                                      accidents_df['road_conditions'].isna()],
                                            choicelist=['Dry',
                                                        'Wet Or Damp',
                                                        'Snow',
                                                        'Unknown'],
                                            default=accidents_df['road_conditions'])



### Missing Values And Formats in Casualties


## Assign Location Values

# Replace NA's with 'Unknown or other'
casualties_df['location'].fillna('Unknown Or Other', inplace=True)


## Assign Missing Pedestrian Movement Values

# Replace NA's with 'Unknown or other'
casualties_df['pedestrian_movement'].fillna('Unknown Or Other', inplace=True)


## Assign Missing bus or coach passenger Values

# Replace NA's with 'Unknown or other'
casualties_df['pedestrian_movement'].fillna('Unknown Or Other', inplace=True)


## Assign Missing Casualty Sex Values

# Replace NA's with 'Unknown'
casualties_df['casualty_sex'].fillna('Unknown', inplace=True)

# Use starting values to identify sex
casualties_df['casualty_sex'] = np.select(condlist=[casualties_df['casualty_sex'].str.startswith('M', 'S'),
                                                    casualties_df['casualty_sex'].str.startswith('F', 'W'),
                                                    casualties_df['casualty_sex'].isna()],
                                          choicelist=['Male',
                                                    'Female',
                                                    'Unknown'],
                                          default = 'Unknown')

## Assign Missing Car Passenger Values

# Assign pedestrians NA's to not car passenger
casualties_df['car_passenger'] = np.where(casualties_df['casualty_class'] == 'Pedestrian', 
                                          'Not Car Passenger',
                                          casualties_df['car_passenger'])

# Replace NA's with 'Unknown'
casualties_df['car_passenger'].fillna('Unknown', inplace=True)


## Assign Missing Casualty Age  Values
print(casualties_df['casualty_age'].unique())



### Missing Values in Vehicles

## Drop columns with more than half of entires missing if not needed for later analysis

# Drop vehicle age, propulsion control
vehicles_df = vehicles_df.drop(['vehicle_age', 'propulsion_code'], axis='columns')


## Assign Missing Driver Sex Values

# Replace NA's with 'Not Known'
vehicles_df['driver_sex'].fillna('Not Known', inplace=True)

# Use starting values to identify sex
vehicles_df['driver_sex'] = np.select([vehicles_df['driver_sex'].str.startswith('M','S'), 
                                       vehicles_df['driver_sex'].str.startswith('F','W')],
                                       ['Male', 'Female'], 
                                       default='Not Known')


## Assign Missing Vehicle Type Values

# Replace NA's with 'Unknown or other'
vehicles_df['vehicle_type'].fillna('Unknown', inplace=True)


## Assign Missing Off Carriageway Values

# Replace NA's with 'Unknown or other'
vehicles_df['hit_object_off_carriageway'].fillna('Unknown', inplace=True)


## Assign Missing Junction Location Values

# Replace NA's with 'Unknown or other'
vehicles_df['junction_location'].fillna('Unknown', inplace=True)


## Assign Missing Skidding Values

# Replace NA's with 'Unknown or other'
vehicles_df['skidding_and_overturning'].fillna('Unknown', inplace=True)


## Assign Missing Towing Values

# Replace NA's with 'Unknown or other'
vehicles_df['towing_and_articulation'].fillna('Unknown', inplace=True)


## Assign Missing Manoeuvre Values

# Replace NA's with 'Unknown or other'
vehicles_df['vehicle_manoeuvre'].fillna('Unknown', inplace=True)


## Assign Missing Leaving Carriageway Values

# Replace NA's with 'Unknown or other'
vehicles_df['vehicle_leaving_carriageway'].fillna('Unknown', inplace=True)


## Assign Missing Left Hand Drive Values

# Replace NA's with 'Unknown or other'
vehicles_df['left_hand_drive'].fillna('Unknown', inplace=True)


## Assign Missing Hit Object Values

# Replace NA's with 'Unknown or other'
vehicles_df['hit_object_in_carriageway'].fillna('Unknown', inplace=True)


## Assign Missing Impact Values

# Replace NA's with 'Unknown or other'
vehicles_df['impact'].fillna('Unknown', inplace=True)

## Assign Missing Driver Age Values
print(vehicles_df['driver_age'].unique())



### Missing Values in Population







#### Handling Duplicates



### Computing duplicate row count table and table of unique value count per column for all data frames


## Initalising Duplicate Data Table To Append Duplicate Row Count Per Table To
duplicates = pd.DataFrame(columns=['Table', 'Number_Duplicate_Rows'])


## Initialising Unique Data Table To Append Unique Values Counted Per Column Of Each Table To
unique = pd.DataFrame(columns=['Table', 'Column', 'Unique_Value', 'Number_Values'])


## Append Duplicate and Unique Counts Per Table to Each Dataframe Initialised Above

# Iterate over dictionary of dataframes
for key in df_dict_cleaned.keys():

    # Don't care about population
    if key != 'Population':
        continue

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

# Use starting value of highway code to identify country, 'Unknown' as catch-all
accidents_df['country'] = np.select(condlist=[accidents_df['highway_authority'].str.startswith('E'), 
                                              accidents_df['highway_authority'].str.startswith('S'), 
                                              accidents_df['highway_authority'].str.startswith('W'), 
                                              accidents_df['highway_authority'].str.startswith('N'), 
                                              accidents_df['highway_authority'].isna()],
                                    choicelist=['England', 
                                                'Scotland', 
                                                'Wales', 
                                                'Northern Ireland', 
                                                'Missing'],
                                    default = 'Unknown')



### Weekday Column

# Obtain weekday from date
accidents_df['weekday'] = accidents_df['date'].dt.day_name()



### Season Column

# Use date months to identify season, unknown as catch-all
accidents_df['season'] = np.select(condlist=[(accidents_df['date'].dt.month >= 12) | (accidents_df['date'].dt.month < 3), 
                                             (accidents_df['date'].dt.month >= 3) & (accidents_df['date'].dt.month < 6),
                                             (accidents_df['date'].dt.month >=6) & (accidents_df['date'].dt.month < 9), 
                                             (accidents_df['date'].dt.month >= 9) & (accidents_df['date'].dt.month < 12),
                                             (accidents_df['date'].isna())],
                                    choicelist=['Winter', 
                                                'Spring', 
                                                'Summer', 
                                                'Autumn',
                                                'Missing'],
                                    default = 'Unknown')




#### Create New Casualties Columns



### Number of Casualties Per Accident Column

# Group by index (unique accident), count number of unique casualty reference numbers
casualties_df['casualties_per_accident'] = casualties_df.reset_index().groupby(['index'])['casualty_ref'].agg(['nunique'])




#### Create New Vehicles Columns



### Number of Vehicles Per Accident Column

# Group by index (unique accident), count number of unique vehicle reference numbers
vehicles_df['vehicles_per_accident'] = vehicles_df.reset_index().groupby(['index'])['vehicle_ref'].agg(['nunique'])




#### Create Road_Accidents


## Combining Accidents, Casualties, Vehicles

# Merge accidents with casualties on common accidents index as key, then merge vehicles on common accidents index and vehicle reference as key, using left joins as we want to retain all accidents as the dominant table of interest
#- Resetting index in accidents table to retain it on merge
#- Validating one-to-many in first accidents merge with casualties, as accidents should be unique
road_accidents = accidents_df.reset_index().merge(casualties_df, how='left', left_on='index', right_on='index', validate='one_to_many').merge(vehicles_df, how='left', left_on=['index', 'vehicle_ref'], right_on=['index', 'vehicle_ref'])


## Merging Population Statistics

# Merge road accidents using highway authority as key with population statistics using code as key; left join used as all accidents should be retained as the dominant table of interest
#- Validating many-to-one as population zone codes should be unique
road_accidents = road_accidents.merge(population_statistics_df, how='left', left_on='highway_authority', right_on='Code', validate='many_to_one')


## Create Animal Involved Column

# If any column columns listed contain an animal description assign 'Yes', else 'No'
road_accidents['animal_involved'] = np.where((road_accidents['carriageway_hazards'] == 'Any Animal In Carriageway (Except Ridden Horse)') | 
                                             (road_accidents['hit_object_in_carriageway'] == 'Any Animal (Except Ridden Horse)') | 
                                             (road_accidents['vehicle_type'] == 'Ridden Horse'), 
                                             'Yes', 
                                             'No')

# Send Road Accidents To Reports As CSV
road_accidents.to_csv(cleaned_data_path/'road_accidents.csv', 
               index=False, 
               header=road_accidents.columns)