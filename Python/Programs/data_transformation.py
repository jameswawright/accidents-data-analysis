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




#### Handling Missing Values






#### Formatting Columns Entries






#### Handling Duplicates



### Computing missing values table for all data frames


## Initalising Duplicate Data Table To Append Duplicate Count Values To
duplicates = pd.DataFrame(columns=['Table', 'Number_Duplicate_Rows'])


## Initialising Unique Data Table To Append Unique Count Values To
unique = pd.DataFrame(columns=['Table', 'Column', 'Unique_Value', 'Number_Values'])

## Append Duplicate Values Count To Duplicate For Each Data Frame

# Iterate over dictionary of dataframes
for key in df_dict:

    # Count duplicated values in each data frame in dictionary, label index as column, reset index to turn series into data frame with missing count as number_missing
    df_duplicates = pd.DataFrame({'Table' : [key], 
                                  'Number_Duplicate_Rows' : [df_dict[key].duplicated().sum()]})
    
    # Counts of each unique value - only objects as numerics would be huge and shouldn't be very unique anyway
    df_unique = df_dict[key].select_dtypes(include='object').melt(var_name='Column', value_name='Unique_Value').value_counts().reset_index(name='Number_Values')

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



### Weekday Column



### Season Column





#### Create New Casualties Columns



### Number of Casualties Per Accident Column





#### Create New Vehicles Columns



### Number of Vehicles Per Accident Column





#### Create Road_Accidents



### Combining Accidents, Casualties, Vehicles



### Merging Population Statistics