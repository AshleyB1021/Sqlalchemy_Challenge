# Import the dependencies.
import numpy as np

import sqlalchemy
import sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine ("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoloaad_with=engine)

# Save references to each table
Measurement= Base.classes.Measurement
Station = Base.classes.Station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@api.route("/")
def welcome():
    """List all available api routes."""
    return(
        f'Available Routes:<br/>'
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temprate Observation: /api/v1.0/tobs<br/>"
        f"Temperature from start date (yyyy-mm-dd):/api/v1.0/<start><br/>"
        f"Temperate from start date (yyyy-mm-dd) to end date (yyyy-mm-dd): /api/v1.0/<start>/<end><br/> "

    )
@app.route('/api/v1.0/precipitation')
def precipitation():
        Session = Session(engine)
        results= Session.query(Measurement.date, Measurement.prcp).all()
        Session.close()
        precipitation_info = list(np.ravel(results))
        return jsonify(precipitation_info)

@app.route('/api/v1.0/stations')
def stations():
      Session = Session(engine)
      station_results= Session.query (Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
      Session.close()
      station_info= list(np.ravel(stations))
      return jsonify(station_info)

@app.route('/api/v1.0/tobs')
def Temperature ():
    Session = Session(engine)
    Temperature_results= Session.query (Measurement.tobs).all()
    Session.close()
    return jsonify(Temperature_results)

@app.route('/api/v1.0/<start>')
def start_date():
      Session = Session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
      filter(Measurement.dt >= start_date).all()
      Session.close()
      return jsonify(start_date)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date():
      Session = Session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
      filter(Measurement.dt >=start_date).filter(Measurement.dt <= start_end_date).all()
      Session.close()
      return jsonify(start_end_date)
if __name__ == '__main__':
    app.run(debug=True)
