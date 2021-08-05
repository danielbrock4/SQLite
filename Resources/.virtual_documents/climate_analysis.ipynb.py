get_ipython().run_line_magic("matplotlib", " inline")
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


import numpy as np
import pandas as pd


import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session #  allows you to create classes in your code that can be mapped to specific tables in a given database. 
from sqlalchemy import create_engine, func, inspect, MetaData, Table


# Database Setup
    # use the create_engine() function to connect to our databaseuse the create_engine() function to connect to our database
engine = create_engine("sqlite:///hawaii.sqlite")


# Get the name of the table by using sqlalchemy inspect dependency
inspector = inspect(engine)
inspector.get_table_names()


# Using the inspector to print ALL column names wiht in the 'measurement' tableand its All types
measurement_columns = inspector.get_columns('measurement')
for columns in measurement_columns:
    print(columns)


# Using the inspector to print All column names wiht in the 'measurement' table & its SPECIFIC types
measurement_columns = inspector.get_columns('measurement')
for column in measurement_columns:
    print(column["name"], column['type'])


# Query Measure Data in Measurement table to view Database
measurement_data = engine.execute("SELECT * FROM measurement LIMIT 5")
for data in measurement_data:
    print(data)


#  Create a meta data object to hold the reflected table schema
metadata = MetaData()


# Create a table object and use 'autoload' and 'autoload_with' to define the columns from the table. 
station_table = Table('station', metadata, autoload=True, autoload_with=engine)


# Get the column names using the 'keys()' method on the column object. 
station_table.columns.keys()


#view specific column type
station_table.columns.station


# Query Station Data in station table to view Database
station_data = engine.execute("SELECT * FROM station LIMIT 5")
for data in station_data:
    print(data)


# reflect an existing database into a new model
    #Automap Base creates a base class for an automap schema in SQLAlchemy
Base = automap_base() 
# reflect the tables
    #the prepare() function reflects the schema of our SQLite tables into our code and create mappings.
Base.prepare(engine, reflect=True) 


# We can view all of the classes that automap found
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)


# Query data and precipitation columns
results = session.query(Measurement.date, Measurement.prcp).all()


# Print out results
    # Use a for loop to check if data ran
# for result in results: 
#     print(result)


# Design a query to retrieve the last 12 months of precipitation data and plot the results.

#Starting from the last data point in the database. 
prev_year = dt.datetime(2017, 8, 23) #This code specifies the most recent date

# Calculate the date one year from the last date in data set.
    #add the dt.timedelta() function to the previous line of code. This function allows us to trace back a certain number of days.
prev_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)

# Create a variable to store the results of the query
results = []

# Perform a query to retrieve the data and precipitation scores
    # session.query() function for this query will take two parameters. We will reference the Measurement table using Measurement.date and Measurement.prcp
    # use the filter() function to filter out the data we don't need.
    # add .all() to the end of our existing query, which extracts all of the results from our query and put them in a list. 
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
# print(results)


# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(results, columns=['date', 'precipation']) 
df.sample(n=3) 


# Use the set_index() Function to set the index to the date column
    # Use the variable inplace to specify whether or not we want to create a new DataFrame
df.set_index(df["date"], inplace=True)
print(df)


# Convert the DataFrame to strings, and then we'll set our index to "False." 
    #This will allow us to print the DataFrame without the index
print(df[:10].to_string(index=False))


# Sort the dataframe by date using the sort_index() function. 
    # Since we set our index to the date column previously, we can use our new index to sort our results
df = df.sort_index()
    # Slice list before .to_string to see partial list
print(df[:10].to_string(index=False))


# Use Pandas Plotting with Matplotlib to plot the data
df.plot()
plt.xticks(rotation=90)
plt.legend()
plt.show()


# Use Pandas to calcualte the summary statistics for the precipitation data using describe() function
df.describe()


# How many stations are available in this dataset?
    # Start by using session.query() to create a query
    # Use func.count, which essentially counts a given dataset we are interested in 
        # By referencing Station.station it give us the number of stations
    #  add the .all() function to the end of this query so that our results are returned as a list.     
stations_count = session.query(func.count(Station.station)).all()
print(stations_count)


# Expression Example
station_count = [station_count for station_count in session.query(func.count(Station.station)).all()]
station_count


# What are the most active stations?
# List the stations and the counts in descending order.
    # Start by using session.query() to create a query
    # Add a few parameters to our query to list the stations and the counts
    # Add group_by() function to group by station name 
    # Add the order_by function to order our results in the order that we specify, in this case, descending order
    # Add the .all() function to  return all of the results of our query 
stations_count_list = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

stations_count_list


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
    # calculate the minimum, maximum, and average temperatures with the following functions: func.min, func.max, and func.avg.
    # filter to most active station
    # Add the .all() function to  return all of the results of our query 
temp_USC00519281 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.station == "USC00519281").all()
temp_USC00519281


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
prev_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)

    # create query using Measurement table data
    # filter to most active station
    # filter to consider only the most recent year
    # Add the .all() function to  return all of the results of our query 
results = session.query(Measurement.tobs).\
            filter(Measurement.station == "USC00519281").\
            filter(Measurement.date >= prev_year).all()
print(results[:9]) #creates super long list that is too much to view
print(" ")

# To make the results easier to read, understand, and use, we'll put them in a DataFrame.
df = pd.DataFrame(results, columns=['tobs'])
df.sample(n=5)


#use the plot() function and the hist() function and add the number of bins as a parameter.
df.plot.hist(bins=12)
#use plt.tight_layout(), we can compress the x-axis labels so that they fit into the box holding our plot.
plt.tight_layout()
    #For this particular graph, using this function won't change much, but it can be a lifesaver in situations where the x-axis doesn't fit into the box.


# Write a function called `calc_temps` that will accept start date and end date in the format 'get_ipython().run_line_magic("Y-%m-%d'", " ")
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end_date:
        results = session.query(*sel).\
         filter(func.strftime('get_ipython().run_line_magic("Y-%m-%d',", " Measurement.date) >= start_date).all()")
        temps = list(np.ravel(results))         
        return temps

    results = results = session.query(*sel).\
     filter(func.strftime('get_ipython().run_line_magic("Y-%m-%d',", " Measurement.date) >= start_date).\")
     filter(func.strftime('get_ipython().run_line_magic("Y-%m-%d',", " Measurement.date) <= end_date).all()")
    temps = list(np.ravel(results))              
    return temps

calc_temps("2017-06-01", "2017-06-30")
