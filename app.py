import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
   
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.prcp, Measurement.date).all()

    all_precipitation = []
    for prcp, date in results:
        precipitation_dict = {}
        precipitation_dict["Precipitation"] = prcp
        precipitation_dict["Date"] = date
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    Date = dt.datetime(2016, 8, 23)
 
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station =="USC00519397").filter(Measurement.date > Date).all()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start = None): 
    
    print(start)    

    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs).filter(Measurement.date >= start)).all()

    all_start = list(np.ravel(results))

    return jsonify(all_start)

    

@app.route("/api/v1.0/<start>/<end>")
def end(end):
    
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs).filter(Measurement.date < end)).all()

    all_end = list(np.ravel(results))

    return jsonify(all_end)

    

if __name__ == '__main__':
    app.run(debug=True)