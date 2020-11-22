import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# generate the engine to the correct sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# # Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"


@app.route("/about")
def about():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )   


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp values"""
    
    # Perform a query to retrieve the precipitation data in the last one year
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>='2016-08-23').\
    order_by(Measurement.date).all()

    session.close()  

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp        
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
    
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station data"""
    # Query all stations in station table
    results = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs data"""
    # Query all tobs for each day

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-23',Measurement.station  == 'USC00519281').all()    

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_route(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset"""
    # Query all temperatures for each day

    results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).group_by(Measurement.date).all()
    
    # Convert list of tuples into normal list
    all_start = list(np.ravel(results))

    session.close()

    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """  Returns the min, max, and average temperatures calculated from the given start date to the given end date"""
    # Query all temperatures for each day

    results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_end = list(np.ravel(results))

    return jsonify(all_end)

    

if __name__ == '__main__':
    app.run(debug=True)



    
    