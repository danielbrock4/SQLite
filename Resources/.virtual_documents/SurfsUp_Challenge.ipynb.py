# Dependencies
import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)


# 1. Import the sqlalchemy extract function.
from sqlalchemy import extract

# 2. Write a query that filters the Measurement table to retrieve the temperatures for the month of June. 

temps = session.query(Measurement.date, Measurement.tobs).filter(extract('month', Measurement.date) == "06").all()
temps[:5]


#  3. Convert the June temperatures to a list.
june_temps = list(temps)
june_temps[:5]


# 4. Create a DataFrame from the list of temperatures for the month of June. 
import pandas as pd

june_temps_df = pd.DataFrame(june_temps, columns=["Date", "June Temps"])
june_temps_df.sample(n=5)


# 5. Calculate and print out the summary statistics for the June temperature DataFrame.
june_temps_df.describe()


# 6. Write a query that filters the Measurement table to retrieve the temperatures for the month of December.
temps = session.query(Measurement.date, Measurement.tobs).filter(extract('month', Measurement.date) == "12").all()
temps[:5]


# 7. Convert the December temperatures to a list.
dec_temps = list(temps)


# 8. Create a DataFrame from the list of temperatures for the month of December. 
dec_temps_df = pd.DataFrame(june_temps, columns=["Date", "December Temps"])
dec_temps_df.sample(n=5)


# 9. Calculate and print out the summary statistics for the Decemeber temperature DataFrame.
dec_temps_df.describe()
