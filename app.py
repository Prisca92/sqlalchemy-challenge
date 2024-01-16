print("hello")

# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")

def welcome():
    print("    ")
    return(
        f"/api/v1.0/precipitation"
        f""
        f""
        f""
        f""
        f""
    )
#-----------------------------------------------------------------
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def percipitation():
    last_date = dt.date(2017,8,23)- dt.timedelta(days=365)
    last_date
# Calculate the date one year from the last date in data set.
    start_date= last_date - dt.timedelta(365)
    start_date

# Perform a query to retrieve the data and precipitation scores
    date_prcp=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= start_date).all()
    #convert into dictionary
    myData= {date:percipitation for date,percipitation in date_prcp}
    session.close()

    return jsonify(myData)

#-------------------------------------------------------------------------------------------------------------
#Station route
@app.route("/api/v1.0/stations")
def stations():
    #query data
    stations_query = session.query(station.station).all()

    #convert tuples into list
    station_list = list(np.ravel(stations_query))

    session.close()
    return jsonify(station_list)

#-------------------------------------------------------------------------------------------------------------

#Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    last_date = dt.date(2017,8,23)- dt.timedelta(days=365)

    #query data 
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= last_date).all()


    
    #convert Tuples into list 
    results_list = list(np.ravel(results))

    session.close()

    return jsonify(results_list)

#-------------------------------------------------------------------------------------------------------------

#start route
@app.route("/api/v1.0/<start>")
def start (start):
    last_date = dt.date(2017,8,23)- dt.timedelta(days=365)
     


      #query data
    start = session.query(func.min(Measurement.tobs), 
                          func.max(Measurement.tobs),
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()
   


 #convert Tuples into list
    session.close()
    start_list = list(np.ravel(start))
    return jsonify(start_list) 
#-------------------------------------------------------------------------------------------------------------

#query data

#-------------------------------------------------------------------------------------------------------------
#START/END ROUTE
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    last_date = dt.date(2017,8,23)- dt.timedelta(days=365)

    
    #query data
    end = session.query(func.min(Measurement.tobs),
                         func.max(Measurement.tobs),
                        func.avg(Measurement.tobs)).\
                          filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).all()

#convert Tyokes into Lst 
    session.close()
    end_list = list(np.ravel(end))
    return jsonify(end_list)

#Run it
if __name__=="__main__":
    app.run()