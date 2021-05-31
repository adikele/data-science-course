'''
Solutions to Exercise 3

Notes:

REPORT on the Reliability Index
Calculation of Reliability Index of (some) carrier A:

Steps:
1. Find all concerned delays 
(i) five types of long-haul flight  delays are included for calculating Reliability Index of a carrier: 
'ArrDelay', 'DepDelay', 'CarrierDelay', 'WeatherDelay', 'LateAircraftDelay	
(ii) 'WeatherDelay' is scaled so as to depend on air distance
(iii) ‘TotalDelay’  = 'ArrDelay' + 'DepDelay' + 'CarrierDelay' + 'ScaledWeatherDelay' + 'LateAircraftDelay	

Dataframe is called grouped_df

2. Reliability Index scale is created and based on the following reference figures:

MAX_RELIABILITY = 9.9
MIN_RELIABILITY = 8.0

Least ‘TotalDelay’ corresponds to reliability index 9.9
Most ‘TotalDelay’ corresponds to reliability index 8.0

LeastTotalDelay = grouped_df['TotalDelay'].min()
MostTotalDelay = grouped_df['TotalDelay'].max()
totaldelay_range = MostTotalDelay  - LeastTotalDelay

Reliability_Index (of a carrier A) = MAX_RELIABILITY - ( (carrier A's total delay - LeastTotalDelay) * reliability_range / totaldelay_range)

Note: 
1.  Dependence of Reliability Index on the total mileage covered per airline (long-haul flights only): 
The weather delay is scaled to account for mileage. If a carrier A flies a total of (long-haul) distances of x kms and another carrier B flies a total of (long-haul) distances of 2x, then Flight B’s weather delay is multiplied by 0.5

2. Dependence of Reliability Index on the no of (long-haul) flights per airline:
Could not understand: whether an airline makes a total of (let’s say) 100 long-haul flights or 200 long-haul flights, in what way could this number affect the reliability index?
Currently, therefore, the no of (long-haul) flights IS NOT CONSIDERED for Reliability Index

3. Dependence of Reliability Index on total delays (you are free to focus on the relevant types of delay)
Described in Steps 1) above.
'''
import pandas as pd
import numpy as np
import time

MAX_RELIABILITY = 9.9
MIN_RELIABILITY = 8.0

DATA_FILE = 'data2008.csv'
flights_df = pd.read_csv(DATA_FILE)
flights_df.rename(columns={'Year': 'FlightYear', 'Month': 'FlightMonth'}, inplace=True)
flights_df.fillna(0, inplace=True)
flights_df2 = flights_df.astype({'CarrierDelay': 'int32', 'WeatherDelay': 'int32', 'NASDelay': 'int32', 'SecurityDelay': 'int32', 'LateAircraftDelay' : 'int32', 'ArrDelay': 'int32', 'DepDelay': 'int32' })
flights_df3 = flights_df2.astype({'AirTime': 'float64',  'Distance': 'float64' })

#creating a column with serial numbers:
flights_df3 ['SerialNo'] = np.arange(len(flights_df3 ))
first_col = flights_df3.pop('SerialNo')
flights_df3.insert(0, 'SerialNo', first_col)
flightskeyed_df = flights_df3
print(flightskeyed_df.head())

unique_carrier_list_orig = flightskeyed_df.UniqueCarrier.unique()
carrier_list = [ ]
for x in unique_carrier_list_orig:
    carrier_list.append(x)

avg_dist_longhaul_dict = {}
tot_dist_longhaul_dict = {}
tot_arr_delay_longhaul_dict = {}
tot_dep_delay_dict = {}
tot_carr_delay_dict = {}
tot_late_delay_dict = {}
tot_wea_delay_dict = {}
tot_dist_dict  = {}
num_of_flights_dict = {}

start_time = time.time()
for x in carrier_list:
    tot_arr_delay = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'ArrDelay'].sum()    
    avg_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].mean()
    tot_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].sum()
    tot_dep_delay = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'DepDelay'].sum()
    tot_carr_delay = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'CarrierDelay'].sum()
    tot_late_delay = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'LateAircraftDelay'].sum()
    tot_wea_delay = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'WeatherDelay'].sum()    
    #tot_dist is used for finding number of flights!
    tot_dist = flightskeyed_df.loc[flightskeyed_df['UniqueCarrier'] == x, 'Distance'].sum()
       
    tot_arr_delay_longhaul_dict [x] = tot_arr_delay
    avg_dist_longhaul_dict [x] = avg_dist_longhaul
    tot_dist_longhaul_dict [x] = tot_dist_longhaul    
    tot_dep_delay_dict [x] = tot_dep_delay
    tot_carr_delay_dict [x] = tot_carr_delay
    tot_late_delay_dict [x] = tot_late_delay
    tot_wea_delay_dict [x] = tot_wea_delay
    tot_dist_dict [x] = tot_dist
    

avg_dist_list_longhaul = list(avg_dist_longhaul_dict.values())
tot_dist_list_longhaul = list(tot_dist_longhaul_dict.values()) 
# A total of 5 delays. but only 4 delays here because "ArrDelay" goes in the making of the df 
tot_carr_delay_list = list(tot_carr_delay_dict.values())
tot_late_delay_list = list(tot_late_delay_dict.values())
tot_wea_delay_list = list(tot_wea_delay_dict.values())
tot_dep_delay_list = list(tot_dep_delay_dict.values())
tot_num_of_flights_longhaul = [ tot/avg for tot,avg in zip(tot_dist_list_longhaul, avg_dist_list_longhaul)]

#creating a new dataframe
grouped_df = pd.DataFrame( list(tot_arr_delay_longhaul_dict.items()) )  
grouped_df.columns =['UniqueCarrier', 'ArrDelay']
grouped_df['NumOfFlights'] = tot_num_of_flights_longhaul
grouped_df['DepDelay'] = tot_dep_delay_list
grouped_df['CarrierDelay'] = tot_carr_delay_list 
grouped_df['LateAircraftDelay'] = tot_late_delay_list 
grouped_df['TotWeatherDelay'] = tot_wea_delay_list 
grouped_df['TotDistance'] = tot_dist_list_longhaul 

#clearing the df of carriers with zero long-haul flights
grouped_df = grouped_df.dropna()

LeastTotalDistance = grouped_df['TotDistance'].min()
scaled_wea_delay_list = grouped_df['TotWeatherDelay'] * LeastTotalDistance / grouped_df['TotDistance']
grouped_df['ScaledWeatherDelay']  = grouped_df['TotWeatherDelay'] * LeastTotalDistance / grouped_df['TotDistance']  #didn't work

grouped_df['TotalDelay']  = grouped_df['TotWeatherDelay'] + grouped_df['DepDelay'] + grouped_df['CarrierDelay'] + grouped_df['LateAircraftDelay'] + grouped_df['ArrDelay']  

LeastTotalDelay = grouped_df['TotalDelay'].min()
MostTotalDelay = grouped_df['TotalDelay'].max()
totaldelay_range = MostTotalDelay  - LeastTotalDelay

reliability_range = MAX_RELIABILITY - MIN_RELIABILITY 
grouped_df['ReliabilityIndex'] = MAX_RELIABILITY - ( (grouped_df['TotalDelay'] - LeastTotalDelay) * reliability_range / totaldelay_range)
#(a) REPORT 
print (grouped_df)

#(b) REPORT The primary type of delay for long-haul flights appers to be "ArrDelay"
print("--- %s seconds ---" % (time.time() - start_time))  # prints --- 22.66365909576416 seconds ---
