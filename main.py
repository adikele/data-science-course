'''
Part Solutions to Exercise 1 
notes:

'''
import pandas as pd
import numpy as np

DATA_FILE = 'data2008.csv'

flights_df = pd.read_csv(DATA_FILE)
flights_df.rename(columns={'Year': 'FlightYear', 'Month': 'FlightMonth'}, inplace=True)

flights_df.fillna(0, inplace=True)
flights_df2 = flights_df.astype({'CarrierDelay': 'int32', 'WeatherDelay': 'int32', 'NASDelay': 'int32', 'SecurityDelay': 'int32', 'LateAircraftDelay' : 'int32' })
flights_df3 = flights_df2.astype({'AirTime': 'float64',  'Distance': 'float64' })

total_num_of_rows = flights_df3.shape[0]
print(f'Total number of rows in dataframe is {total_num_of_rows}')

total_num_of_columns = len(flights_df3.columns)
print(f'Total number of columns in dataframe is {total_num_of_columns}')

month_no = 0
total_num_of_rows_2ndmethod = 0 
for month_no in range (0,13):
    seriesObj = flights_df3.apply(lambda x: True if x['FlightMonth'] == month_no else False , axis=1)
    numOfRows = len(seriesObj[seriesObj == True].index)
    print(f'Number of Rows in dataframe in which month = {month_no} is {numOfRows} ')
    total_num_of_rows_2ndmethod  +=  numOfRows
print (total_num_of_rows_2ndmethod)


if total_num_of_rows == total_num_of_rows_2ndmethod:
    print('The total number of rows counted on per-month basis is equal to the total number of rows')
else:
    print('The count for total number of rows has problems!')

# creating a column with serial numbers:
flights_df3 ['SerialNo'] = np.arange(len(flights_df3 ))
first_col = flights_df3.pop('SerialNo')
flights_df3.insert(0, 'SerialNo', first_col)
flightskeyed_df = flights_df3

#to find 'Diverted' column's values
print(flightskeyed_df.Diverted.unique()) 

flightskeyed_new_df = flightskeyed_df[flightskeyed_df.Diverted != 1]
total_num_of_rows = flightskeyed_new_df.shape[0]
print(f'Total number of rows with Diverted flights removed is {total_num_of_rows}')

flightskeyed_new_df.to_csv(r'flightskeyed_new.csv')

print(flightskeyed_df.Cancelled.unique())

flightskeyed_new2_df = flightskeyed_new_df[flightskeyed_new_df.Cancelled!= 1]
total_num_of_rows = flightskeyed_new2_df.shape[0]
print(f'Total number of rows with Diverted and Cancelled flights removed is {total_num_of_rows}')

print(flightskeyed_new2_df.head())
