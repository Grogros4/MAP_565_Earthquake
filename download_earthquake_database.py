import requests
import os
import argparse
import pandas as pd
import glob


argparser = argparse.ArgumentParser()

argparser.add_argument('-s', '--start_year', help='Start year of the data to download', default=2000, type=int)
argparser.add_argument('-e', '--end_year', help='End year of the data to download', default=2022, type=int)

start_year = argparser.parse_args().start_year
end_year = argparser.parse_args().end_year


#Create a folder to store the data if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

        
#Download the data
for year in range(start_year,end_year + 1):
    # Splitting the year in 3 to prevent exceeding the limit of the number of rows returned
    print("Downloading data for year " + str(year))
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime="+str(year)+"-01-01 00:00:00&endtime="+str(year)+"-04-30 23:59:59&minmagnitude=2.5&orderby=time"
    r = requests.get(url, allow_redirects=True)
    open('data/earthquake_' + str(year) + '_part1.csv', 'wb').write(r.content)
    
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime="+str(year)+"-05-01 00:00:00&endtime="+str(year)+"-08-31 23:59:59&minmagnitude=2.5&orderby=time"
    r = requests.get(url, allow_redirects=True)
    open('data/earthquake_' + str(year) + '_part2.csv', 'wb').write(r.content)
    
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime="+str(year)+"-09-01 00:00:00&endtime="+str(year)+"-12-31 23:59:59&minmagnitude=2.5&orderby=time"
    r = requests.get(url, allow_redirects=True)
    open('data/earthquake_' + str(year) + '_part3.csv', 'wb').write(r.content)

# Merge the data
print("Merging the data")
# Read all the files
df = pd.concat([pd.read_csv(f) for f in glob.glob('data/earthquake_*.csv')], ignore_index = True)

# Order by time
df = df.sort_values(by=['time'])

print("Saving the data")
# Save the file
df.to_csv("earthquake_" + str(start_year) + "_" + str(end_year) + ".csv", index=False)    