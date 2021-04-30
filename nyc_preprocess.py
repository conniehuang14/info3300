import pandas as pd
from datetime import datetime

# Rat Sighting data source: https://www.kaggle.com/new-york-city/nyc-rat-sightings
rat_df = pd.read_csv("Rat_Sightings.csv")

# Create column for year of sighting
rat_df['Year'] = [datetime.strptime(ts.replace(" AM", "").replace(" PM", ""), "%m/%d/%Y %H:%M:%S").strftime("%Y") for ts in rat_df['Created Date']]

# Generate separate output df to export, select only necessary columns
output_df = pd.DataFrame(data={'year' : rat_df['Year'], 'borough': [x.lower() for x in rat_df['Borough']], 'latitude':rat_df['Latitude'], 'longitude':rat_df['Longitude']})
output_df = output_df.rename_axis("id")

output_df.to_csv('rat_data.csv')