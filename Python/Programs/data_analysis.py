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

# # Compute population per country
# populations_per_country = road_accidents.groupby(['country']).agg(total_population=('Population','sum')).reset_index()
# print(populations_per_country)

# Compute road accidents per weekday and order by above weekdays for report
casualty_severity_per_country = road_accidents.groupby(['country', 'casualty_severity']).agg(total_casualties=('casualty_severity','count')).reset_index()
print(casualty_severity_per_country)

print(road_accidents.shape)
# # Merge to have population with road accidents per weekday
# casualty_severity_per_country = casualty_severity_per_country.merge(populations_per_country, how='left', left_on='country', right_on='country')
# print(casualty_severity_per_country)

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
for c in ax[0].containers: #- Label bars
    ax[0].bar_label(c)
ax[0].set_title('Accident Severity by Driver Sex')
ax[0].set_xlabel('Sex')
ax[0].set_ylabel('Frequency')
ax[0].legend(title='Casualty Severity')

sns.barplot(data=road_accidents_per_driver_sex_pct,
            x='driver_sex', 
            y='percent',
            palette = 'magma',
            ax=ax[1])
#- Label bars
ax[1].bar_label(ax[1].containers[0], fmt='%.f%%') #- Label bars
ax[1].set_title('Accidents By Driver Sex')
ax[1].set_xlabel('Sex')
ax[1].set_ylabel('Percentage of Total Accidents')
fig.set_size_inches(16, 8)
fig.savefig(reports_path/'road_accidents_per_driver_sex_plot.png')
plt.show()


#-  We see that male drivers are more likely to have an accident than female drivers, and they have more fatal and severe accidents.



### The number of accidents involving animals


## Report On Accidents Involving Animals

# Compute road accidents involving animals for report
accidents_animals = road_accidents.groupby(['animal_involved']).agg(frequency=('index','nunique')).reset_index()

# Graphing and exporting to reports
plt.figure()
accidents_animals_plot = sns.barplot(data=accidents_animals,
                                     x='animal_involved',
                                     y='frequency',
                                     palette = 'magma')
plt.xlabel("Animal Involved")
plt.ylabel("Frequency")
plt.bar_label(accidents_animals_plot.containers[0], label_type='edge') #- Label bars
plt.title("Animal Involved in Accident")
fig = accidents_animals_plot.get_figure()
fig.set_size_inches(16, 8)
fig.savefig(reports_path/'animal_involved_plot.png')
plt.show()



### The number of accidents per day. 


## Report On Accidents Per Day

# Reusing road_accidents_per_weekday
# Graphing and exporting to reports
plt.figure()
road_accidents_per_weekday_plot = sns.barplot(data=road_accidents_per_weekday,
                                              x='weekday',
                                              y='total',
                                              palette = 'magma')
plt.xlabel("Weekday")
plt.ylabel("Number of Accidents")
plt.title("Road Accidents Per Weekday")
plt.bar_label(road_accidents_per_weekday_plot.containers[0], label_type='edge') #- Label bars
fig = road_accidents_per_weekday_plot.get_figure()
fig.set_size_inches(16, 8)
fig.savefig(reports_path/'road_accidents_per_weekday_plot.png')
plt.show()

# - The 5 most frequent number of accidents per day are Monday-Friday, increasing across successive weekdays.



### The number of accidents per season 


## Report on Number Accidents by Season

# Ordering Weekdays For Report
seasons = ["Spring", "Summer", "Autumn", "Winter"]

# Compute road accident severity per sex and order by above weekdays for report
accidents_per_season = road_accidents.groupby(['season']).agg(frequency=('index','nunique')).reindex(seasons).reset_index()

# Graphing and exporting to reports
plt.figure()
accidents_per_season_plot = sns.barplot(data=accidents_per_season,
                                              x='season',
                                              y='frequency',
                                              palette = 'magma')
plt.xlabel("Season")
plt.ylabel("Number of Accidents")
plt.title("Road Accidents Per Season")
plt.bar_label(accidents_per_season_plot.containers[0], label_type='edge') #- Label bars
fig = accidents_per_season_plot.get_figure()
fig.set_size_inches(16, 8)
fig.savefig(reports_path/'accidents_per_season_plot.png')
plt.show()



### How  the number of inhabitants in an area affects the likelihood of an accident


## Report On Number of Accidents by Area Population

# Compute road accidents and population by area
#- Number of unique accidents from indexs
#- Number of people in area (Population is repeated by rows associated with accident, but the same for all, so just choose maximum value)
pop_vs_accidents = road_accidents.groupby(['Area_Name']).agg(frequency=('index','nunique'), population=('Population','max'))

# Graphing and exporting to reports
plt.figure()
pop_vs_accidents_plot = sns.scatterplot(data=pop_vs_accidents,
                                        x='population',
                                        y='frequency',
                                        color='purple')
plt.xlabel("Population")
plt.ticklabel_format(style='plain')
plt.xticks(rotation=25)
plt.ylabel("Number of Accidents")
plt.title("Accidents versus Population")
fig = pop_vs_accidents_plot.get_figure()
fig.set_size_inches(16, 8)
fig.savefig(reports_path/'pop_vs_accidents_plot.png')
plt.show()


#- We see that the number of accidents increases by population of an area