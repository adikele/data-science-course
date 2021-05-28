'''
Part Solutions to Exercise 2 
This exercise uses two approaches to create a summary dataframe
-- Option1: using groupby -- summary dataframe that groups flights according to ORIGIN
-- Option2: summary dataframe has been created from dictionaries, grouping flights according to ORIGIN
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

# - Option1 STARTS
#  using groupby - summary dataframe that groups flights according to ORIGIN
#Golda's code
print("Option1 STARTS")

SumFlights_df = flightskeyed_df.groupby(['Origin']).agg(NumberOfFlights=("FlightYear",'count'),
                                                                            AvgDistanceFlown=("Distance", 'mean'),
                                                                            TotalNASDelay=("NASDelay",'sum')).reset_index()
#Aditya's code
#avg_dep_delay = [ total_dep_delay/total_flights for total_dep_delay,total_flights in zip(tot_NASdelay_list, tot_num_of_flights)]
#SumFlights_v2_df['AverageDepartureDelay'] = avg_dep_delay
SumFlights_df ['AverageNASDelay'] = SumFlights_df ['TotalNASDelay']/SumFlights_df ['NumberOfFlights']

print("printing sumflights")
#print(SumFlights_df.head(15))

SumFlights_df = SumFlights_df.sort_values('AverageNASDelay', ascending=False)
print (SumFlights_df)

SumFlights_df['max_flights_rank'] = SumFlights_df['NumberOfFlights'].rank(pct=True)
print ("Now showing 'busyness rank' of airports corresponding to 'number of flights' at the ariport!")
print (SumFlights_df)
print("Option1 ENDS")
print("Option1 ENDS")
# - Option1 ENDS


# - Option2 STARTS
# summary dataframe that groups flights according to ORIGIN
print("Option2 STARTS")
origin_list = list (flightskeyed_df.Origin.unique())
print("origin list:")
print(origin_list)

avg_dist_dict  = {}
avg_air_time_dict = {}
tot_arr_delay_dict = {}
tot_NASdelay_dict = {}
tot_carr_delay_dict = {}
tot_late_delay_dict = {}
tot_nas_delay_dict = {}
tot_sec_delay_dict = {}
tot_wea_delay_dict = {}
tot_dist_dict  = {}
num_of_flights_dict = {}


for x in origin_list:
    avg_dist = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'Distance'].mean()
    tot_NASdelay = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'NASDelay'].sum()
    #tot_dist is used for finding number of flights!
    tot_dist = flightskeyed_df.loc[flightskeyed_df['Origin'] == x, 'Distance'].sum()
     
    avg_dist_dict [x] = avg_dist
    tot_NASdelay_dict [x] = tot_NASdelay
    tot_dist_dict [x] = tot_dist
   
tot_NASdelay_list = list(tot_NASdelay_dict.values())  #used!
avg_dist_list = list(avg_dist_dict.values())
tot_dist_list = list(tot_dist_dict.values()) 
tot_num_of_flights = [ tot/avg for tot,avg in zip(tot_dist_list, avg_dist_list)]

#creating a new dataframe
SumFlights_v2_df = pd.DataFrame( list(tot_NASdelay_dict.items()) )  
SumFlights_v2_df.columns =['Origin', 'NASDelay']
SumFlights_v2_df['NumOfFlights'] = tot_num_of_flights

#adding average departure delay per flight to the dataframe:
avg_dep_delay = [ total_dep_delay/total_flights for total_dep_delay,total_flights in zip(tot_NASdelay_list, tot_num_of_flights)]
SumFlights_v2_df['AverageDepartureDelay'] = avg_dep_delay

SumFlights_v2_df = SumFlights_v2_df.sort_values('AverageDepartureDelay', ascending=False)
print (SumFlights_v2_df)

print ("Now showing 'busyness rank' of airports corresponding to 'number of flights' at the ariport!")
SumFlights_v2_df['max_flights_rank'] = SumFlights_v2_df['NumOfFlights'].rank(pct=True)
print (SumFlights_v2_df)
# prints ok, but the airport with most delay has a business rank of only 0.25
# So are there really busier airports? -- let me arrange another df according to "business"

print("The following df is just to check which airport has the max 'NumOfFlights' and what is the value")  
busy_df = SumFlights_v2_df.sort_values('NumOfFlights', ascending=False)
print (busy_df)

print("Option2 ENDS")
print("Option2 ENDS")
