import pandas as pd
import numpy as np
from datetime import datetime

# Rat Sighting data source: https://www.kaggle.com/new-york-city/nyc-rat-sightings
rat_df = pd.read_csv("Rat_Sightings.csv")

# Create column for year of sighting
rat_df['Year'] = [datetime.strptime(ts.replace(" AM", "").replace(" PM", ""), "%m/%d/%Y %H:%M:%S").strftime("%Y") for ts in rat_df['Created Date']]

# Count rats by zip code and year, append to output dataframe
rat_output_df = pd.DataFrame()
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
for year in years:
    rat_groups = rat_df.loc[rat_df['Year'] == str(year)].loc[rat_df['Incident Zip'] > 10000].groupby('Incident Zip')['Unique Key'].nunique().to_frame()
    rat_groups['year'] = year
    rat_groups['borough'] = rat_df.loc[rat_df['Year'] == str(year)].iloc[0]['Borough'].lower()
    rat_output_df = rat_output_df.append(rat_groups)

# Cast zip codes to int and export as csv
rat_output_df = rat_output_df.reindex(rat_output_df.index.astype(int))
rat_output_df = rat_output_df.rename(columns={'Unique Key':'count'}).rename_axis("zip")
rat_output_df.to_csv('rat_data.csv')

# Create sale property output csv, append filtered data over loop
sale_output_df = pd.DataFrame()

# NYC Property Sales source: https://www.kaggle.com/johnshuford/new-york-city-property-sales
# Construct read_csv statement for looping over multiple csvs by year and borough

boroughs = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'StatenIsland']
for year in years:
    for borough in boroughs:
        csv_string = 'Property_Sales/'+borough+'/'+borough+'/'+str(year)+'_'+borough+".csv"
        sale_csv = pd.read_csv(csv_string, usecols=['Zip Code', 'Sale Price'])

        # Filter out transfer of owner data (price/zip of 0)
        sale_csv = sale_csv.loc[sale_csv['Sale Price'] > 10].loc[sale_csv['Zip Code'] > 0]
        
        # Group data and average sale price by zip code, add year and borough back in and rename to lowercase
        sale_groups = sale_csv.groupby('Zip Code')['Sale Price'].apply(np.average).to_frame()
        sale_groups['Sale Price'] = sale_groups['Sale Price'].round(2)
        sale_groups['year'] = year
        sale_groups['borough'] = borough
        sale_groups = sale_groups.rename(columns={'Sale Price':'price'}).rename_axis('zip')


        # Append to output dataframe
        sale_output_df = sale_output_df.append(sale_groups)

# Export as csv
sale_output_df.to_csv('sale_data.csv')
    
