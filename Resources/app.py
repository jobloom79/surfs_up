import datetime as dt
from telnetlib import SE
from unittest import result
from itsdangerous import JSONWebSignatureSerializer, json
import numpy as np
import pandas as pd
from requests import session

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, engine_from_config, func

from flask import Flask, jsonify
from sympy import preview

# Create Engine and declare base
engine = create_engine("sqlite:///hawaii.sqlite")
base = automap_base()
# reflect base in order to refernce tables
base.prepare(engine, reflect=True)
# create variables referencing tables
measurement = base.classes.measurement
station = base.classes.station
# Create a session link from Python to the database
session = Session(engine)
# define app for Flask application
app = Flask(__name__)

# Add Welcome Route
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

# Add Percipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Add Station route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)