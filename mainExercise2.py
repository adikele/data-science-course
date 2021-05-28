'''
Part Solutions to Exercise 2 
notes:

'''
import pandas as pd
import numpy as np
import time


DATA_FILE = 'data2008.csv'
flights_df = pd.read_csv(DATA_FILE)
flights_df.rename(columns={'Year': 'FlightYear', 'Month': 'FlightMonth'}, inplace=True)
flights_df.fillna(0, inplace=True)
flights_df2 = flights_df.astype({'CarrierDelay': 'int32', 'WeatherDelay': 'int32', 'NASDelay': 'int32', 'SecurityDelay': 'int32', 'LateAircraftDelay' : 'int32', 'ArrDelay': 'int32', 'NASDelay': 'int32' })
flights_df3 = flights_df2.astype({'AirTime': 'float64',  'Distance': 'float64' })

#creating a column with serial numbers:
flights_df3 ['SerialNo'] = np.arange(len(flights_df3 ))
first_col = flights_df3.pop('SerialNo')
flights_df3.insert(0, 'SerialNo', first_col)
flightskeyed_df = flights_df3
print(flightskeyed_df.head())


#to find 'Diverted' column's values
flightskeyed_df = flightskeyed_df[flightskeyed_df.Diverted != 1]
total_num_of_rows = flightskeyed_df.shape[0]
flightskeyed_df = flightskeyed_df[flightskeyed_df.Cancelled!= 1]
total_num_of_rows = flightskeyed_df.shape[0]
print(f'Total number of rows with Diverted and Cancelled flights removed is {total_num_of_rows}')

# - summary dataframe that groups flights according to ORIGIN
origin_list = list (flightskeyed_df.Origin.unique())
print("origin list:")
print(origin_list)

avg_dist_dict  = {}
avg_air_time_dict = {}
tot_arr_delay_dict = {}
tot_dep_delay_dict = {}
tot_carr_delay_dict = {}
tot_late_delay_dict = {}
tot_nas_delay_dict = {}
tot_sec_delay_dict = {}
tot_wea_delay_dict = {}
tot_dist_dict  = {}
num_of_flights_dict = {}

start_time = time.time()
for x in origin_list:
    avg_dist = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'Distance'].mean()
    tot_dep_delay = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'NASDelay'].sum()
    #tot_dist is used for finding number of flights!
    tot_dist = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'Distance'].sum()
     
    avg_dist_dict [x] = avg_dist
    tot_dep_delay_dict [x] = tot_dep_delay
    tot_dist_dict [x] = tot_dist
   
tot_dep_delay_list = list(tot_dep_delay_dict.values())  #used!
avg_dist_list = list(avg_dist_dict.values())

tot_dist_list = list(tot_dist_dict.values()) 

tot_num_of_flights = [ tot/avg for tot,avg in zip(tot_dist_list, avg_dist_list)]
print("--- %s seconds ---" % (time.time() - start_time))  # prints about 160 seconds 

#creating a new dataframe
grouped_orig_df = pd.DataFrame( list(tot_dep_delay_dict.items()) )  
grouped_orig_df.columns =['Origin', 'NASDelay']
print (grouped_orig_df)

grouped_orig_df['NumOfFlights'] = tot_num_of_flights

#for average departure delay per flight:
avg_dep_delay = [ total_dep_delay/total_flights for total_dep_delay,total_flights in zip(tot_dep_delay_list, tot_num_of_flights)]

grouped_orig_df['AverageDepartureDelay'] = avg_dep_delay

tot_num_of_flights_tot = sum(tot_num_of_flights)

grouped_orig_df = grouped_orig_df.sort_values('AverageDepartureDelay', ascending=False)
print (grouped_orig_df)

grouped_orig_df['max_flights_rank'] = grouped_orig_df['NumOfFlights'].rank(pct=True)

print ("now showing 'busyness rank' of airports corresponding to 'number of flights' at the ariport!")
print (grouped_orig_df)
# prints ok, but the airport with most delay has a business rank of only 0.25
# So are there really busier airports -- let me arrange another df according to "business"

print("--- %s seconds ---" % (time.time() - start_time))  # prints about 160.2 seconds 

print("The following df is just to check which airport has the max 'NumOfFlights' and what is the value")  
busy_df = grouped_orig_df.sort_values('NumOfFlights', ascending=False)
print (busy_df)

if tot_num_of_flights_tot == total_num_of_rows:
    print ("Sum of flights taken one carrier at a time = sum of all rows: All well!")

