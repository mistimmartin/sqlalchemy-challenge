import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/yyyy-mm-dd<br/>"
        "/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()

    session.close()

    precip_l = list(np.ravel(precip))

    return jsonify(precip_l)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    stations_l = list(np.ravel(stations))

    return jsonify(stations_l)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    date = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    tobs = session.query(Station.name, Measurement.date, Measurement.tobs).filter(Measurement.date >= date).all()

    session.close()

    tobs_l = list(np.ravel(tobs))

    return jsonify(tobs_l)

@app.route("/api/v1.0/<start>")
def start(start_date):

    session = Session(engine)
    
    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    start_l = []
    for min, avg, max in start:
        start_dict = {}
        start_dict["min"] = min
        start_dict["avg"] = avg
        start_dict["max"] = max
        start_l.append(start_dict)

    return jsonify(start_l)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):

    session = Session(engine)
    
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    start_end_l = []
    for min, avg, max in start:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["avg"] = avg
        start_end_dict["max"] = max
        start_end_l.append(start_end_dict)

    return jsonify(start_end_l)


if __name__ == '__main__':
    app.run(debug=True)
