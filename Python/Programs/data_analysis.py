##################################################################################################
# Name: data_analysis.py                                                                         #
# Description: Program to Perform Data Analysis                                                  #
# Creation Date: 13/06/2023                                                                      #
# Created by: James Wright                                                                       #
#             Graduate Programmer                                                                #
#             Katalyze Data Ltd.                                                                 #
##################################################################################################



#### Segregating Data Analysis Section In Terminal
print('\n ---------------------------------------- Data Analysis ---------------------------------------- \n')

print(road_accidents.columns)


#### Analyse Road Accidents



### The number of accidents per weekday. Do any days have a significantly different number of accidents to others?


## Report On Road Accidents Per Weekday

# Ordering Weekdays For Report
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Compute road accidents per weekday and order by above weekdays for report
road_accidents_per_weekday = road_accidents.groupby(['weekday']).agg(total=('index','nunique')).reindex(days).reset_index()

# Compute average accidents over week for report, append to weekday report
road_accidents_avg_weekday = road_accidents_per_weekday.agg(Mean=('total', 'mean')).rename_axis('weekday').reset_index().round(0).astype({'total' : 'int'})
road_accidents_per_weekday_mean = pd.concat([road_accidents_per_weekday, road_accidents_avg_weekday], axis=0, ignore_index=True)

# Conclusion
#- There are significantly more accidents on Friday with 22579 accidents compared to the weekly average 19517
#- There are significantly more accidents on Sunday with 15024 accidents compared to the weekly average 19517

# Send Road Accidents Per Weekday To Reports As CSV
road_accidents_per_weekday_mean.to_csv(reports_path/'road_accidents_per_weekday.csv', 
                                  index=False,
                                  header= ['Weekday', 'Total'])



### A table showing the frequency of casualty severity by country per 1,000,000 inhabitants of each country.

## Report On Casualty Severity Frequency by Country per 1,000,000 Inhabitants of Each Country

# Compute population per country
populations_per_country = road_accidents.groupby(['country']).agg(total_population=('Population','sum')).reset_index()
print(populations_per_country)

# Compute road accidents per weekday and order by above weekdays for report
casualty_severity_per_country = road_accidents.groupby(['country', 'casualty_severity']).agg(total_casualties=('casualty_severity','count')).reset_index()
print(casualty_severity_per_country)

casualty_severity_per_country = casualty_severity_per_country.merge(populations_per_country, how='left', left_on='country', right_on='country')
print(casualty_severity_per_country)

# # Send Casualty Severity Frequency by Country per 1,000,000 Inhabitants of Each Country To Reports As CSV
# casualty_severity_per_country.to_csv(reports_path/'casualty_severity_per_country.csv',
#                                      index=False,
#                                      header= ['Country', 'Casualty Severity', 'Frequency Per 1,000,000 Inhabitants', 'pop.'])




### The frequency of casualty severity by driver sex.


## Report On Accidents Per Sex

# Compute percent road accidents per sex
road_accidents_per_driver_sex_pct = road_accidents.groupby(['driver_sex']).agg(percent=('index','nunique')).apply(lambda x: np.round(x*100/x.sum(), 2)).reset_index()

# Compute road accident severity per sex and order by above weekdays for report
road_accidents_severity_per_driver_sex = road_accidents.groupby(['driver_sex', 'casualty_severity']).agg(frequency=('index','nunique')).reset_index()

# Graphing and exporting to reports
fig, ax =plt.subplots(1,2)
sns.barplot(data=road_accidents_severity_per_driver_sex,
            x='driver_sex', 
            y='frequency',
            hue='casualty_severity',
            palette = 'magma',
            ax=ax[0])
ax[0].set_title('Accident Severity by Driver Sex')
ax[0].set_xlabel('Sex')
ax[0].set_ylabel('Frequency')
ax[0].legend(title='Casualty Severity')
sns.barplot(data=road_accidents_per_driver_sex_pct,
            x='driver_sex', 
            y='percent',
            palette = 'magma',
            ax=ax[1])
ax[1].set_title('Accidents By Driver Sex')
ax[1].set_xlabel('Sex')
ax[1].set_ylabel('Percentage of Total Accidents')
fig.savefig(reports_path/'road_accidents_per_driver_sex_plot.png')
plt.show()


#-  We see that male drivers are more likely to have an accident than female drivers, and they have more fatal and severe accidents.



### The number of accidents involving animals


## Report On Accidents Involving Animals

# Compute road accidents per weekday and order by above weekdays for report
accidents_animals = road_accidents.groupby(['animal_involved']).agg(frequency=('index','nunique')).reset_index()

# Graphing and exporting to reports
accidents_animals_plot = sns.barplot(data=accidents_animals,
                                     x='animal_involved',
                                     y='frequency',
                                     palette = 'magma')
plt.xlabel("Animal Involved")
plt.ylabel("Frequency")
plt.title("Animal Involved in Accident")
fig = accidents_animals_plot.get_figure()
fig.savefig(reports_path/'animal_involved_plot.png')
plt.show()



### The number of accidents per day. What are the top 5 quietest and busiest days in terms of the number of accidents?


## Report On Accidents Per Day

# Reusing road_accidents_per_weekday

# Graphing and exporting to reports
road_accidents_per_weekday_plot = sns.barplot(data=road_accidents_per_weekday,
                                     x='weekday',
                                     y='total',
                                     palette = 'magma')
plt.xlabel("Weekday")
plt.ylabel("Number of Accidents")
plt.title("Road Accidents Per Weekday")
fig = road_accidents_per_weekday_plot.get_figure()
fig.savefig(reports_path/'road_accidents_per_weekday_plot.png')
plt.show()

# - The 5 most frequent number of accidents per day are Monday-Friday, increasing across successive weekdays.



### How does the number of inhabitants in an area affect the likelihood of an accident

# Graphing


### The number of accidents per season occurring in that area?

# Graphing