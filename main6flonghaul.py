'''
Part Solutions to Exercise 3

Update 25.5.21
Program finds:
a) total no of long-haul flights per each airline
b) total of arrival delay for long-haul flights per each airline

notes:
Not using summary dataframe SumFlights_df. 
Reason for not using SumFlights_df:
SumFlights_df has values for the totals and averages of different flight parameters 
(including  “delays” and “airtime”) for the flights between individual origins and individual destinations. 
How would it be possible to use this summary dataframe to calculate the values for “delays” and “airtime” 
for flights fulfilling a specific condition (long-haul flights)?


'''
import pandas as pd
import numpy as np
import time

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

avg_dist_dict  = {}
avg_air_time_dict = {}

tot_arr_delay_longhaul_dict = {}


'''
tot_dep_delay_dict = {}
tot_carr_delay_dict = {}
tot_late_delay_dict = {}
tot_nas_delay_dict = {}
tot_sec_delay_dict = {}
tot_wea_delay_dict = {}
tot_dist_dict  = {}
num_of_flights_dict = {}
'''
start_time = time.time()
for x in carrier_list:

    tot_arr_delay = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'ArrDelay'].sum()    
    avg_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].mean()
    tot_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].sum()
    
    '''
    tot_dep_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'DepDelay'].sum()
    tot_carr_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'CarrierDelay'].sum()
    tot_late_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'LateAircraftDelay'].sum()
    tot_nas_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'NASDelay'].sum()
    tot_sec_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'SecurityDelay'].sum()
    tot_wea_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'WeatherDelay'].sum()
    
    #tot_dist is used for finding number of flights!
    tot_dist = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'Distance'].sum()
    '''
   
    
    tot_arr_delay_longhaul_dict [x] = tot_arr_delay
    avg_dist_longhaul_dict [x] = avg_dist_longhaul
    tot_dist_longhaul_dict [x] = tot_dist_longhaul    

    '''
    tot_dep_delay_dict [x] = tot_dep_delay
    tot_carr_delay_dict [x] = tot_carr_delay
    tot_late_delay_dict [x] = tot_late_delay
    tot_nas_delay_dict [x] = tot_nas_delay
    tot_sec_delay_dict [x] = tot_sec_delay
    tot_wea_delay_dict [x] = tot_wea_delay
    tot_dist_dict [x] = tot_dist
    '''

avg_dist_list_longhaul = list(avg_dist_longhaul_dict.values())
tot_dist_list_longhaul = list(tot_dist_longhaul_dict.values()) 

'''
tot_dep_delay_dict_list = []
tot_dep_delay_list = list(tot_dep_delay_dict.values())

tot_dist_list = list(tot_dist_dict.values()) 
avg_dist_list = list(avg_dist_dict.values())

avg_air_time_list = list(avg_air_time_dict.values())
tot_carr_delay_list = list(tot_carr_delay_dict.values())
tot_late_delay_list = list(tot_late_delay_dict.values())
tot_sec_delay_list = list(tot_sec_delay_dict.values())
tot_wea_delay_list = list(tot_wea_delay_dict.values())
'''

#finding the total distance and average distance only for long haul
tot_num_of_flights_longhaul = [ tot/avg for tot,avg in zip(tot_dist_list_longhaul, avg_dist_list_longhaul)]
print("--- %s seconds ---" % (time.time() - start_time))  # prints 31.62915301322937 seconds 


#creating a new dataframe
grouped_df = pd.DataFrame( list(tot_arr_delay_longhaul_dict.items()) )  
grouped_df.columns =['UniqueCarrier', 'ArrDelay']
grouped_df['NumOfFlights'] = tot_num_of_flights_longhaul
print (grouped_df)


'''
grouped_df['AverageDistance'] = avg_dist_list
grouped_df['AverageAirTime'] = avg_air_time_list  
grouped_df['DepDelay'] = tot_dep_delay_list

grouped_df['CarrierDelay'] = tot_carr_delay_list 
grouped_df['LateAircraftDelay'] = tot_late_delay_list 
grouped_df['TotSecurityDelay'] = tot_sec_delay_list 

grouped_df['TotWeatherDelay'] = tot_wea_delay_list 
grouped_df['NumOfFlights'] = tot_num_of_flights

tot_num_of_flights_tot = sum(tot_num_of_flights)
'''

