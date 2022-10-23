#
# generate_dataframe.py
#

#
# go from 0h to 24h, in 15 minute steps,
# request shelly's mock readings, adjust them according to daylight time, and
# save to dataset & disk
#

import json
import time
import datetime
import requests
import numpy as np
import pandas as pd
from shelly_plug import meter


def get_counters(shelly_meter):
    """
    get the counters from the shelly_meter json object
    return the counters as a list
    """
    r = json.loads(shelly_meter)
    return r['counters']


def request_shelly_meter(shelly_address):
    """
    request the meters from the shelly device
    return the meter status as json
    """
    resp = requests.get(shelly_address)
    if resp.status_code == 200:
        #print(f"response:\n{resp.text}")
        r = resp.text
    else:
        print("no response from Shelly")
        r = False
    return r



def get_shelly_meter(shelly_address):
    """
    directly call the meter function from the shelly mock function
    return the meter status as json
    """
    r = json.dumps(meter(0))
    return r



def save_df_to_disk(df, destination_folder):
    """
    saves the content of a DataFrame to an existing & accessible storage location
    in:     pandas dataframe presumably containing data
            string with the path to the destination folder
    out:    csv file stored in the specified permanent storage location
            returns the number of records contained in the received DataFrame
    """
    df.name = 'Photovoltaic_Production'
    print(f"saving {df.name} to permanent storage")
    if(df.shape[0] == 0):
        print("there is no data for saving to disk")
    else:
        print("there is data for saving to disk. let's go!")
        # set the dataframe's name
        # get the current date & time for file-naming purposes
        current_time = datetime.datetime.now()
        now = str(current_time).split(".")[0].replace(" ", "_").replace(":", "").replace("-", "")

        # now is a good time to store the data
        file_extension = "csv"
        print(f"saving as {file_extension}...")
        #df.export(f'{destination_folder}/{df.name}_{now}.{file_extension}', progress=True)
        filename = f'{destination_folder}/{df.name}_{now}.{file_extension}'
        df.to_csv(filename)
        print(f"{df.name} was saved to permanent storage as {filename} file.")
    return df.shape[0]


# define the dates
first_day = datetime.datetime.strptime("2022-1-01", "%Y-%m-%d")
n_days = 100
days = pd.date_range(first_day, periods=n_days).strftime("%Y-%m-%d").to_list()
#print(days)

# define the daily times
n_hours         = 24
n_min_per_hour  = 60
interval    = 15  # in minutes
daily_times = [
    f"{str(i).zfill(2)}:{str(j).zfill(2)}"
        for i in range(n_hours)
        for j in range(n_min_per_hour)
        if j % interval == 0
    ]
#print(daily_times)


# define the daily power factors (higher during daylight times)
morning_factors = np.sort(abs(np.random.normal(loc=0.0, scale=0.4, size=24*4)))
daily_sun_exposure_factors = np.append(morning_factors, np.flip(morning_factors))
#print(daily_sun_exposure_factors, daily_sun_exposure_factors.size)


# initialize dataframe
cols=['date', 'time', 'pwr_1min', 'pwr_2min', 'pwr_3min']
df = pd.DataFrame(columns = cols)
df.index.name = 'id'

# go along the days and their times, getting readings into production dataframe
print('generating mock shelly data...')
for d in days:
    i = 0
    print(f'current day: {d}')
    for t in daily_times:
        # get mock meters
        # m = get_counters(request_shelly_meter('http://127.0.0.1:8000/meter/0')) # calling the Shelly API
        m = get_counters(get_shelly_meter('http://127.0.0.1:8000/meter/0')) # directly invoking que API's function
        # adjust meters according to time of day
        m = [c * daily_sun_exposure_factors[i] for c in m]
        # add row to dataframe
        row = [ d, t, m[0], m[1], m[2] ]
        #print(f'adding row:\n{row}')
        i += 1 # time of the day counter
        # add row to dataframe
        df.loc[len(df)] = row


# save the dataset to permanent storage
print('saving shelly data to disk...')
save_df_to_disk(df, './')

# check the dataframe contents' stats
print(df.describe())
