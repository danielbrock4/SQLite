#Set Up the Flask Weather App
    # Import Dependencies for datetime, NumPy, and Pandas
import datetime as dt
import numpy as np
import pandas as pd
    # Import Dependencies for sqlAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, MetaData, Table
     # Add the code to import the dependencies that we need for Flask.
from flask import Flask, jsonify

    # Set Up the Database
        # Access Database with create_engine() function allows us to access and query our SQLite database file.
engine = create_engine('sqlite:///hawaii.sqlite')     
        # Reflect Database Tables using Python function
Base = automap_base()
Base.prepare(engine, reflect=True)
        # With the database reflected, we can save our references to each table.
        # Create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station
        # Create a session link from Python to our database
session = Session(engine)

    # Set Up Flask
        # To define our Flask app we will create a Flask application called "app."
app = Flask(__name__)
 
 # Create the Welcome Route
    # Step 1: Define the welcome route 
    # Step 2: Create a function welcome() with a return statement
    # Step 3: Use f-strings to display the precipitation, stations, tobs, and temp routes 
       # When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
       # This convention signifies that this is version 1 of our application. This line can be updated to support future versions of the app as well.
@app.route('/')
def welcome():
    return(
    '''
     Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    '''
    )
# Precipitation Route
    # Step 1: Create the route
    # Step 2: Create  the precipitation() function.
    # Step 3: Add the line of code that calculates the date one year ago from the most recent date in the database
    # Step 4: Write a query to get the date and precipitation for the previous year
    # Step 5: Create a dictionary with the date as the key and the precipitation as the value. 
        # To do this, we will "jsonify" our dictionary. Jsonify() is a function that converts the dictionary to a JSON file
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#  Stations Route
    # Step 1: Create the route
    # Step 2: Create  the stations() function.
    # Step 3: Create a query that will allow us to get all of the stations in our database
    # Step 4: Unravel our results into a one-dimensional array by using  the function np.ravel() with results as our parameter.
    # Step 5: Convert our unraveled results into a list. To convert the results to a list, we will need to use the list function, which is list(), and then convert that array into a list. 
    # Step 6: jsonify the list and return it as JSON
        # You may notice here that to return our list as JSON, we need to add stations=stations. This formats our list into JSON        
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature Route
    # Step 1: Create the route
    # Step 2: Create function called temp_monthly()
    # Step 3: Add the line of code that calculates the date one year ago from the most recent date in the database
    # Step 4: Create a query for all the temperature observations from the previous year
    # Step 5: Unravel our results into a one-dimensional array by using  the function np.ravel() with results as our parameter.
    # Step 6: Convert our unraveled results into a list. To convert the results to a list, we will need to use the list function, which is list(), and then convert that array into a list. 
    # Step 7: jsonify the list and return it as JSON
        # You may notice here that to return our list as JSON, we need to add temps=temps. This formats our list into JSON
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))    
    return jsonify(temps=temps)


 #Statistics Route
    # Step 1: Create the routes to provide oth a starting and ending date
    # Step 2: Create a function called stats()
        # Step 2a: Add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None
    # Step 3: Create a list called sel to select the minimum, average, and maximum temperatures from our SQLite database
    # Step 4: Determine the starting and ending date by adding an if-not statement to our code
        # Step 4a. Query our database
        # Step 4b: Unravel the results into a one-dimensional array and convert them to a list     
    # Step 5: 
    # Step 6: 
    # Step 7: 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=none, end=none):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)