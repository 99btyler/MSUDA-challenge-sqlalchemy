from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, func # for MIN, AVG, MAX
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# database reflection
engine = create_engine("sqlite:///../database/hawaii.db")
session = Session(engine)

Base = automap_base()
Base.prepare(autoload_with=engine) # reflection

for table in Base.classes.keys():
    print(table)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask
app = Flask(__name__)

# Flask API
@app.route("/api/precipitation")
def precipitation():

    response = session.query(
        Measurement.date,
        Measurement.prcp
    ).filter(
        Measurement.date >= "2016-08-23",
        Measurement.date <= "2017-08-23"
    ).all()

    response_dict = {item[0]:item[1] for item in response}
    return jsonify(response_dict)

@app.route("/api/stations")
def stations():

    response = session.query(
        Station.station
    ).all()

    response_list = [item[0] for item in response]
    return jsonify(response_list)

@app.route("/api/tobs")
def tobs():

    response = session.query(
        Measurement.tobs
    ).filter(
        Measurement.station == "USC00519281",
        Measurement.date >= "2016-08-23",
        Measurement.date <= "2017-08-23"
    ).all()

    response_list = [item[0] for item in response]
    return jsonify(response_list)

@app.route("/api/range/<start>")
def range_start(start):
    
    response = session.query(
        func.MIN(Measurement.tobs),
        func.AVG(Measurement.tobs),
        func.MAX(Measurement.tobs)
    ).filter(
        Measurement.date >= start
    ).all()

    response_list = [item[0] for item in response]
    return jsonify(response_list)

@app.route("/api/range/<start>/<end>")
def range_start_end(start, end):
    
    response = session.query(
        func.MIN(Measurement.tobs),
        func.AVG(Measurement.tobs),
        func.MAX(Measurement.tobs)
    ).filter(
        Measurement.date >= start,
        Measurement.date <= end
    ).all()

    response_list = [item[0] for item in response]
    return jsonify(response_list)

# Flask pages
@app.route("/")
def home():
    return render_template("home.html")

# main
if __name__ == "__main__":
    app.run(debug=True)