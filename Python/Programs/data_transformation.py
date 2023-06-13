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


## Initalising Missing Data Table To Append Missing Values To
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


## Sort dataframe by missing count
missing.sort_values(by='Number_Missing', ascending=False, inplace=True, ignore_index = True)



### Output Missing Data Report CSV to Report Folder

# Export to CSV
missing.to_csv(reports_path/'missing.csv', 
               index=False, 
               header=missing.columns)

print('Note: Missing Data Report Exported To CSV.')