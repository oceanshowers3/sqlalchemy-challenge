import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine) 

# Flask Setup
app = Flask(__name__)


# Flask Routes

@app.route("/")
def welcome():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation Data: /api/v1.0/precipitation<br/>"
        f"Station List: /api/v1.0/stations<br/>"
        f"Temperatures for one year: /api/v1.0/tobs<br/>"
        f"Temperatures at the start date: /api/v1.0/<start><br/>"
        f"Temperatures from start to end dates: /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    precipitation_date = []
    for date, precipitation in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = precipitation
        precipitation_date.append(precip_dict)

    return jsonify(precipitation_date)


@app.route("/api/v1.0/stations")
def stations():

    station_results = session.query(Station.station).all()
    station_list = list(np.ravel(station_results))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp_observations = session.query(Measurement.tobs).filter(Measurement.date >= query_date).\
        filter(Measurement.station == 'USC00519281').all()

    tobs_list = list(np.ravel(temp_observations))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def temperature_start_date(date_start=None):
    temperature_start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    temperature_start_list = list(np.ravel(temperature_start_date_results))
    return jsonify(temperature_start_list)


@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(date_start=None, date_end=None):
    temperature_start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date_start).filter(Measurement.date <= date_end).all()
    temperature_start_end_list = list(np.ravel(temperature_start_end_results))
    return jsonify(temperature_start_end_list)


if __name__ == '__main__':
    app.run(debug=True)