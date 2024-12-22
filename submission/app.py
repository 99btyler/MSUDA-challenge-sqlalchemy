from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# database
engine = create_engine("sqlite:///resources/hawaii.sqlite")
session = Session(engine)

Base = automap_base()
Base.prepare(autoload_with=engine)

Station = Base.classes.station
Measurement = Base.classes.measurement

# flask
app = Flask(__name__)

@app.route("/")
def index():
    return  """
            <html style="font-family:arial;">
                <head>
                    <h1>Climate App</h1>
                </head>
                <body>
                    <ul style="list-style-type:none; padding:0;">
                        <li><span style="color:#006eff;">    /                       </span> - returns the index with available routes</li>
                        <li><span style="color:#006eff;">    /api/v1.0/precipitation </span> - returns a JSON list of the last 12 months of precipitation data</li>
                        <li><span style="color:#006eff;">    /api/v1.0/stations      </span> - returns a JSON list of the stations</li>
                        <li><span style="color:#006eff;">    /api/v1.0/tobs          </span> - returns a JSON list of the last 12 months of temperature data for the most-active station</li>
                        <li><span style="color:#006eff;">    /api/v1.0/start         </span> - returns a JSON list of the minimum, average, and maximum temperature from the specified range</li>
                        <li><span style="color:#006eff;">    /api/v1.0/start/end     </span> - returns a JSON list of the minimum, average, and maximum temperature from the specified range</li>
                    </ul>
                </body>
            </htm>
            """

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(
        Measurement.prcp
    ).filter(
        Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23"
    ).all()
    precipitation_list = [item[0] for item in precipitation]
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    station_list = [item[0] for item in stations]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    temperature = session.query(
        Measurement.tobs
    ).filter(
        Measurement.station == "USC00519281", Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23"
    ).all()
    temperature_list = [item[0] for item in temperature]
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start(start):
    min_avg_max = session.query(
        func.MIN(Measurement.tobs), func.AVG(Measurement.tobs), func.MAX(Measurement.tobs)
    ).filter(
        Measurement.date >= start
    ).all()
    min_avg_max_list = [f"min:{item[0]}, avg:{item[1]}, max:{item[2]}" for item in min_avg_max]
    return jsonify(min_avg_max_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    min_avg_max = session.query(
        func.MIN(Measurement.tobs), func.AVG(Measurement.tobs), func.MAX(Measurement.tobs)
    ).filter(
        Measurement.date >= start, Measurement.date <= end
    ).all()
    min_avg_max_list = [f"min:{item[0]}, avg:{item[1]}, max:{item[2]}" for item in min_avg_max]
    return jsonify(min_avg_max_list)

# main
if __name__ == "__main__":
    app.run(port=8000, debug=True)