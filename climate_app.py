from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
stations = Base.classes.station
measurements = Base.classes.measurement
session = Session(engine)
#api routes
from flask import Flask, jsonify

# Flask Setup
app = Flask(__name__)
 


@app.route("/")
def welcome():
  return( 
        f"Welcome to the My Trip Page API! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/<mytrip_start_date><br/>"
        f"/api/v1.0/<mytrip_start_date>/<mytrip_end_date><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        )

@app.route('/api/v1.0/precipitation')
def precip():
    """Return date and precipitation data as json"""
    date_prcp=session.query(measurements.date,measurements.prcp).all()
    date_prcp_df=pd.DataFrame(date_prcp).set_index('date')
    date_prcp_dict=date_prcp_df.to_dict()
    return jsonify(date_prcp_dict)

@app.route('/api/v1.0/stations')
def stations():
    """Return station data as json"""
    stats_all=session.query(stations.station).group_by(stations.station).all()
    station_df=pd.DataFrame(stats_all)
    station_dict= station_df.to_dict()
    return jsonify(station_dict)

@app.route('/api/v1.0/tobs')
def temperatures():
    """Returm Highest Active Station Tempuratures and Date as json"""
    hi_act= session.query(measurements.tobs,measurements.date,measurements.station).\
                     filter(measurements.station == 'USC00519281').\
                    filter(measurements.date >last_12).\
                        order_by(measurements.date).all()
    hi_act_df=pd.DataFrame(hi_act).set_index('date')
    hi_act_dict=hi_act_df.to_dict()
    return jsonify(hi_act_dict)

@app.route('/api/v1.0/<mytrip_start_date>')
def date_start(mytrip_start_date):
    """Return min,max,avg temperature for start date and all days after"""
    mytrip_start_date = dt.date(2015, 8, 10)
    prev_year = dt.timedelta(days=365)
    start_dt_strftime=dt.datetime.strptime('2014-08-10',"%Y-%m-%d") 
    date_start_results=session.query(func.min(measurements.tobs), func.avg(measurements.tobs),func.max(measurements.tobs)).\
                        filter(measurements.date >= mytrip_start_date).all()
    return(date_start_results)
@app.route('/api/v1.0/<mytrip_start_date>/<mytrip_end_date>')
def date_start_end(mytrip_start_date,mytrip_end_date):
        """Return min, max and avg temperature for between the start and end dates"""
        mytrip_start_date = dt.date(2015, 8, 10)
        mytrip_end_date= dt.date(2015, 8,14)
        prev_year = dt.timedelta(days=365)
        start_dt_strftime=dt.datetime.strptime('2014-08-10',"%Y-%m-%d")
        end_dt_strftime=dt.datetime.strptime('2014-08-14',"%Y-%m-%d")   
        date_start_end_results=session.query(func.min(measurements.tobs), func.avg(measurements.tobs),func.max(measurements.tobs)).\
                        filter(measurements.date >= mytrip_start_date).filter(measurements.date <= end_dt_strftime).all()
        return(date_start_end_results)
if __name__ == "__main__":
     app.run(debug=True)