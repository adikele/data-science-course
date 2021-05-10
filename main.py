'''
Part Solutions to Exercise 1 
notes:

'''
import pandas as pd
import numpy as np
import time

'''
a) and b)
I am of the opinion that it is not possible to “clean” data unless one knows what data is expected, 
what data values would be in error, and so on. 
In other words, one would need to make guidelines for “clean data” before the cleaning process.
'''

#b)
DATA_FILE = 'data2008.csv'
flights_df = pd.read_csv(DATA_FILE)

#c)
flights_df.rename(columns={'Year': 'FlightYear', 'Month': 'FlightMonth'}, inplace=True)

#d)
flights_df.fillna(0, inplace=True)
flights_df2 = flights_df.astype({'CarrierDelay': 'int32', 'WeatherDelay': 'int32', 'NASDelay': 'int32', 'SecurityDelay': 'int32', 'LateAircraftDelay' : 'int32', 'ArrDelay': 'int32', 'DepDelay': 'int32' })

#e) 
flights_df3 = flights_df2.astype({'AirTime': 'float64',  'Distance': 'float64' })

#f)
total_num_of_rows = flights_df3.shape[0]
print(f'Total number of rows in dataframe is {total_num_of_rows}')

total_num_of_columns = len(flights_df3.columns)
print(f'Total number of columns in dataframe is {total_num_of_columns}')


#g)
# option 1 -- takes 459.9170300960541 seconds
start_time = time.time()
month_no = 0
total_num_of_rows_2ndmethod = 0 
for month_no in range (0,13):
    seriesObj = flights_df3.apply(lambda x: True if x['FlightMonth'] == month_no else False , axis=1)
    numOfRows = len(seriesObj[seriesObj == True].index)
    print(f'Number of Rows in dataframe in which month = {month_no} is {numOfRows} ')
    total_num_of_rows_2ndmethod  +=  numOfRows
print (total_num_of_rows_2ndmethod)
print("--- %s seconds ---" % (time.time() - start_time))

if total_num_of_rows == total_num_of_rows_2ndmethod:
    print('The total number of rows counted on per-month basis is equal to the total number of rows')
else:
    print('The count for total number of rows has problems!')

'''
#option 2
start_time = time.time()

month_no = 0
total_num_of_rows_2ndmethod = 0 

month_dict = { }
for index, row in flights_df3.iterrows():
    month_no = row['FlightMonth'] 
    if month_no in month_dict.keys(): 
        month_dict[month_no] = month_dict[month_no] + 1
    else:   # first encounter of this month
        month_dict[month_no] = 1
    
total_values = sum (month_dict.values())
total_num_of_rows_2ndmethod = total_values
    
if total_num_of_rows == total_num_of_rows_2ndmethod:
    print('The total number of rows counted on per-month basis is equal to the total number of rows')
else:
    print('The count for total number of rows has problems!')

print("--- %s seconds ---" % (time.time() - start_time))
'''

#h) creating a column with serial numbers:
flights_df3 ['SerialNo'] = np.arange(len(flights_df3 ))
first_col = flights_df3.pop('SerialNo')
flights_df3.insert(0, 'SerialNo', first_col)
flightskeyed_df = flights_df3

#i)
#to find 'Diverted' column's values
print(flightskeyed_df.Diverted.unique()) 

flightskeyed_new_df = flightskeyed_df[flightskeyed_df.Diverted != 1]
total_num_of_rows = flightskeyed_new_df.shape[0]
print(f'Total number of rows with Diverted flights removed is {total_num_of_rows}')

#j)
flightskeyed_new_df.to_csv(r'flightskeyed_new.csv')

#k)
print(flightskeyed_df.Cancelled.unique())

flightskeyed_new2_df = flightskeyed_new_df[flightskeyed_new_df.Cancelled!= 1]
total_num_of_rows = flightskeyed_new2_df.shape[0]
print(f'Total number of rows with Diverted and Cancelled flights removed is {total_num_of_rows}')

#l) PART B - summary dataframe that groups flights according to airline carrier
unique_carrier_list_orig = flightskeyed_df.UniqueCarrier.unique()
print(unique_carrier_list_orig)

carrier_list = [ ]
for x in unique_carrier_list_orig:
    carrier_list.append(x)
print(carrier_list)

print(flightskeyed_new2_df.head())

'''
(I) number of flights, (II) Avg. distance flown, (III) Avg. AirTime 
(IV) Tot. Arrival Delay, (V) Tot. Dept. Delay, (VI) Tot. Carrier Delay, 
(VII) Tot. Late Aircraft Delay, (VIII) Tot. NAS Delay, (IX) Tot. Security Delay, 
(X) Tot. Weather Delay.

['FlightYear' 'FlightMonth' 'DayofMonth' 'DayOfWeek' 'DepTime'
 'CRSDepTime' 'ArrTime' 'CRSArrTime' 'UniqueCarrier' 'FlightNum' 'TailNum'
 'ActualElapsedTime' 'CRSElapsedTime' 'AirTime' 'ArrDelay' 'DepDelay'
 'Origin' 'Dest' 'Distance' 'TaxiIn' 'TaxiOut' 'Cancelled'
 'CancellationCode' 'Diverted' 'CarrierDelay' 'WeatherDelay' 'NASDelay'
 'SecurityDelay' 'LateAircraftDelay']	
'''

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
for x in carrier_list:
    avg_dist = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'Distance'].mean()
    avg_air_time = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'AirTime'].mean()
    tot_arr_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'ArrDelay'].sum()
    tot_dep_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'DepDelay'].sum()
    tot_carr_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'CarrierDelay'].sum()
    tot_late_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'LateAircraftDelay'].sum()
    tot_nas_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'NASDelay'].sum()
    tot_sec_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'SecurityDelay'].sum()
    tot_wea_delay = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'WeatherDelay'].sum()
    #whack! tot_dist is used for finding number of flights!
    tot_dist = flightskeyed_new2_df.loc[flightskeyed_new2_df['UniqueCarrier'] == x, 'Distance'].sum()
     
    avg_dist_dict [x] = avg_dist
    avg_air_time_dict [x] = avg_air_time
    tot_arr_delay_dict [x] = tot_arr_delay
    tot_dep_delay_dict [x] = tot_dep_delay
    tot_carr_delay_dict [x] = tot_carr_delay
    tot_late_delay_dict [x] = tot_late_delay
    tot_nas_delay_dict [x] = tot_nas_delay
    tot_sec_delay_dict [x] = tot_sec_delay
    tot_wea_delay_dict [x] = tot_wea_delay
    tot_dist_dict [x] = tot_dist
   
tot_dep_delay_dict_list = []
tot_dep_delay_list = list(tot_dep_delay_dict.values())
avg_dist_list = list(avg_dist_dict.values())
avg_air_time_list = list(avg_air_time_dict.values())
tot_carr_delay_list = list(tot_carr_delay_dict.values())
tot_late_delay_list = list(tot_late_delay_dict.values())
tot_sec_delay_list = list(tot_sec_delay_dict.values())
tot_wea_delay_list = list(tot_wea_delay_dict.values())
tot_dist_list = list(tot_dist_dict.values()) #new

#whack:
tot_num_of_flights = [ tot/avg for tot,avg in zip(tot_dist_list, avg_dist_list)]
print("--- %s seconds ---" % (time.time() - start_time))  # prints 31.62915301322937 seconds 

#creating a new dataframe
grouped_df = pd.DataFrame( list(tot_arr_delay_dict.items()) )  
grouped_df.columns =['UniqueCarrier', 'ArrDelay']
print (grouped_df)

grouped_df['AverageDistance'] = avg_dist_list
grouped_df['AverageAirTime'] = avg_air_time_list  
grouped_df['DepDelay'] = tot_dep_delay_list
grouped_df['CarrierDelay'] = tot_carr_delay_list 
grouped_df['LateAircraftDelay'] = tot_late_delay_list 
grouped_df['TotSecurityDelay'] = tot_sec_delay_list 
grouped_df['TotWeatherDelay'] = tot_wea_delay_list 
grouped_df['NumOfFlights'] = tot_num_of_flights

tot_num_of_flights_tot = sum(tot_num_of_flights)
print (grouped_df)

if tot_num_of_flights_tot == total_num_of_rows:
    print ("Sum of flights taken one carrier at a time = sum of all rows: All well!")

