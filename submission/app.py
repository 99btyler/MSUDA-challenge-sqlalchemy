from flask import Flask, jsonify
from sqlalchemy import create_engine
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
            <html style="font-family:arial; text-align:center;">
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
    precipitation_data = session.query(
        Measurement.prcp
    ).filter(
        Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23"
    ).all()
    precipitation_data_list = [item[0] for item in precipitation_data]
    return jsonify(precipitation_data_list)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    station_list = [item[0] for item in stations]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    temperature_data = session.query(
        Measurement.tobs
    ).filter(
        Measurement.station == "USC00519281", Measurement.date >= "2016-08-18", Measurement.date <= "2017-08-18"
    ).all()
    temperature_data_list = [item[0] for item in temperature_data]
    return jsonify(temperature_data_list)

@app.route("/api/v1.0/start")
def start():
    return "returns a JSON list of the minimum, average, and maximum temperature from the specified range"

@app.route("/api/v1.0/start/end")
def start_end():
    return "returns a JSON list of the minimum, average, and maximum temperature from the specified range"

# main
if __name__ == "__main__":
    app.run(port=8000, debug=True)