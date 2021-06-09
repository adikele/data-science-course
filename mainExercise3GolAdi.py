'''
Notes For finding the Reliability Index for OPtion1:
Step 1: 
For a unique carrier ‘X’, find the average of the relevant delays for all of the (long-haul) flights for the unique carrier ‘X’
The weather delay is scaled to account for mileage. If a carrier A flies a total of (long-haul) distances of x kms and another carrier B flies a total of (long-haul) distances of 2x, then Flight B’s weather delay is multiplied by 0.5

Step 2:
Calculate Reliability Index based on the average delays found in step 1

Steps in detail:
Step 1: 
1. Find all concerned delays 
(i) five types of long-haul flight delays are included for calculating Reliability Index of every unique carrier: 
'ArrDelayLh', 'DepDelayLh', 'CarrierDelayLh', 'WeatherDelayLh', 'LateAircraftDelayLh’	
(ii) For every unique carrier, 'WeatherDelayLh' is scaled so as to depend on the total long-haul flight distance ‘TotDistanceLh’ of that unique carrier

(iii) ‘TotalDelayLh’  = 'ArrDelayLh' + 'DepDelayLh' + 'CarrierDelayLh' + 'ScaledWeatherDelayLh' + 'LateAircraftDelayLh’	

(iv) grouped_df['AverageDelayLh'] = grouped_df['TotalDelayLh'] / grouped_df['NumOfFlightsLh']
Dataframe is called grouped_df

Step 2:
2. Reliability Index scale is created and based on the following reference figures:

MAX_RELIABILITY = 9.9
MIN_RELIABILITY = 8.0

least_average_delay = grouped_df['AverageDelayLh'].min()
most_average_delay = grouped_df['AverageDelayLh'].max()

least_average_delay → corresponds to a reliability index 9.9
most_average_delay → corresponds to a reliability index 8.0

delay_range = most_average_delay  - least_average_delay

Reliability_Index (of a carrier A) = MAX_RELIABILITY - ( (carrier A's ‘AverageDelayLh’ - least_average_delay) * reliability_range / delay_range)

REPORT: AQ is the most reliable airline with an index of 9.9.
'''

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

MAX_RELIABILITY = 9.9
MIN_RELIABILITY = 8.0

#DELETE
DATA_FILE = 'data2008.csv'
flights_df = pd.read_csv(DATA_FILE)
#DELETE

#INSERT
# loading flightskeyed_df 
#flightskeyed_df = pd.read_csv("flightskeyed_df.csv")
#INSERT
flights_df.rename(columns={'Year': 'FlightYear', 'Month': 'FlightMonth'}, inplace=True)
flights_df.fillna(0, inplace=True)
flights_df2 = flights_df.astype({'CarrierDelay': 'int32', 'WeatherDelay': 'int32', 'NASDelay': 'int32', 'SecurityDelay': 'int32', 'LateAircraftDelay' : 'int32', 'ArrDelay': 'int32', 'DepDelay': 'int32' })
flights_df3 = flights_df2.astype({'AirTime': 'float64',  'Distance': 'float64' })

#creating a column with serial numbers:
flights_df3 ['SerialNo'] = np.arange(len(flights_df3 ))
first_col = flights_df3.pop('SerialNo')
flights_df3.insert(0, 'SerialNo', first_col)
flightskeyed_df = flights_df3
flightskeyed_option1_df = flightskeyed_df 

# filtering long haul flights
flightskeyed_df = flightskeyed_df.loc[flightskeyed_df['AirTime']>360]

#a)
print("a) Total number of flights per airline")
print(pd.crosstab(flightskeyed_df.UniqueCarrier, flightskeyed_df.FlightYear,colnames=['Total Flights']))


print("b) Primary type of delay for long haul flights")
print(flightskeyed_df.groupby('FlightYear').agg(TotalNASDelay=("NASDelay",'sum'),
                                         TotalDepDelay=("DepDelay",'sum'),
                                         TotalArrDelay=("ArrDelay",'sum'),
                                         TotalCarrierDelay=("CarrierDelay",'sum'),
                                         TotalWeatherDelay=("SecurityDelay",'sum'),
                                         TotalLateAircraftDelay=("LateAircraftDelay",'sum')).reset_index().T)
print()                                       
print("Primary type of delay for long haul flights are ArrDelay")

#OPTION1 for RELIABILITY INDEX
print("OPTION1 for RELIABILITY INDEX..")

unique_carrier_list_orig = flightskeyed_option1_df.UniqueCarrier.unique()
carrier_list = [ ]
for x in unique_carrier_list_orig:
    carrier_list.append(x)

avg_dist_longhaul_dict = {}
tot_dist_longhaul_dict = {}
tot_arr_delay_longhaul_dict = {}
tot_dep_delay_longhaul_dict = {}
tot_carr_delay_longhaul_dict = {}
tot_late_delay_longhaul_dict = {}
tot_wea_delay_longhaul_dict = {}

for x in carrier_list:
    tot_arr_delay_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'ArrDelay'].sum()    
    tot_dep_delay_longhaul = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'DepDelay'].sum()
    tot_carr_delay_longhaul = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'CarrierDelay'].sum()
    tot_late_delay_longhaul = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'LateAircraftDelay'].sum()
    tot_wea_delay_longhaul = flightskeyed_df.loc[(flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360),  'WeatherDelay'].sum()    
    #avg_dist_longhaul and tot_dist_longhaul is used for finding number of long-haul flights!
    avg_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].mean()
    tot_dist_longhaul = flightskeyed_df.loc[ (flightskeyed_df['UniqueCarrier'] == x) & (flightskeyed_df['AirTime'] > 360), 'Distance'].sum()
           
    tot_arr_delay_longhaul_dict [x] = tot_arr_delay_longhaul       
    tot_dep_delay_longhaul_dict [x] = tot_dep_delay_longhaul
    tot_carr_delay_longhaul_dict [x] = tot_carr_delay_longhaul
    tot_late_delay_longhaul_dict [x] = tot_late_delay_longhaul
    tot_wea_delay_longhaul_dict [x] = tot_wea_delay_longhaul
    avg_dist_longhaul_dict [x] = avg_dist_longhaul
    tot_dist_longhaul_dict [x] = tot_dist_longhaul 

avg_dist_longhaul_list = list(avg_dist_longhaul_dict.values())
tot_dist_longhaul_list = list(tot_dist_longhaul_dict.values()) 
# A total of 5 delays. but only 4 delays here because "ArrDelayLonghaul" goes in the making of the df 
tot_carr_delay_longhaul_list = list(tot_carr_delay_longhaul_dict.values())
tot_late_delay_longhaul_list = list(tot_late_delay_longhaul_dict.values())
tot_wea_delay_longhaul_list = list(tot_wea_delay_longhaul_dict.values())
tot_dep_delay_longhaul_list = list(tot_dep_delay_longhaul_dict.values())
tot_num_of_flights_longhaul = [ tot/avg for tot,avg in zip(tot_dist_longhaul_list, avg_dist_longhaul_list)]

#creating a new dataframe
grouped_df = pd.DataFrame( list(tot_arr_delay_longhaul_dict.items()) )  
grouped_df.columns =['UniqueCarrier', 'ArrDelayLh']
grouped_df['NumOfFlightsLh'] = tot_num_of_flights_longhaul
grouped_df['DepDelayLh'] = tot_dep_delay_longhaul_list
grouped_df['CarrierDelayLh'] = tot_carr_delay_longhaul_list 
grouped_df['LateAircraftDelayLh'] = tot_late_delay_longhaul_list 
grouped_df['TotWeatherDelayLh'] = tot_wea_delay_longhaul_list 
grouped_df['TotDistanceLh'] = tot_dist_longhaul_list 

#clearing the df of carriers with zero long-haul flights
grouped_df = grouped_df.dropna()

#to create a "Scaled Weather Delay" column
least_total_distance = grouped_df['TotDistanceLh'].min()
scaled_wea_delay_list = grouped_df['TotWeatherDelayLh'] * least_total_distance / grouped_df['TotDistanceLh']
grouped_df['ScaledWeatherDelayLh']  = grouped_df['TotWeatherDelayLh'] * least_total_distance / grouped_df['TotDistanceLh']  

grouped_df['TotalDelayLh']  = grouped_df['ScaledWeatherDelayLh'] + grouped_df['DepDelayLh'] + grouped_df['CarrierDelayLh'] + grouped_df['LateAircraftDelayLh'] + grouped_df['ArrDelayLh']  

#finding average delay for each unique carrier
grouped_df['AverageDelayLh'] = grouped_df['TotalDelayLh'] / grouped_df['NumOfFlightsLh']

least_average_delay = grouped_df['AverageDelayLh'].min()
most_average_delay = grouped_df['AverageDelayLh'].max()
delay_range = most_average_delay  - least_average_delay

reliability_range = MAX_RELIABILITY - MIN_RELIABILITY 
grouped_df['ReliabilityIndex'] = MAX_RELIABILITY - ( (grouped_df['AverageDelayLh'] - least_average_delay) * reliability_range / delay_range)
#(a) REPORT Table showing the total no of long-haul flights per each airline
print (grouped_df[['UniqueCarrier','NumOfFlightsLh']])

print (grouped_df)

#OPTION1 ENDS

#OPTION 2 for RELIABILITY INDEX
print("OPTION2 for RELIABILITY INDEX..")

# finding total delay for the airlines , discarding weather delay as these type delays are uncertain and unfortunate 
flightskeyed_df['TotalDelay'] = flightskeyed_df['DepDelay']+flightskeyed_df['ArrDelay']+flightskeyed_df['CarrierDelay']+flightskeyed_df['NASDelay']+flightskeyed_df['SecurityDelay']+flightskeyed_df['LateAircraftDelay']

# grouping by airline carrier and finding the total delay, number of flights and total distance
reliability_df = flightskeyed_df.groupby(['UniqueCarrier']).agg(TotalDelay=("TotalDelay",'sum'),
                                                               NumberOfFlights=('FlightYear','count'),
                                                               TotalDistance=('Distance','sum')).reset_index()
print()
print("----------------Before scaling----------------")
print(reliability_df)
print("----------------------------------------------")
                                                               
mms = MinMaxScaler()

# scaling the values between 0 and 1
reliability_df[['TotalDelay','NumberOfFlights','TotalDistance']] = mms.fit_transform(reliability_df[['TotalDelay','NumberOfFlights','TotalDistance']])

# simple reliability index using number of flights * total distance / total delay
reliability_df['reliability_index'] = (reliability_df['NumberOfFlights']*reliability_df['TotalDistance'])/reliability_df['TotalDelay']
print()
print("Reliability indexes : higher the better (values are between 0 and 1)")
print(reliability_df.sort_values(by='reliability_index',ascending=False).fillna(0))