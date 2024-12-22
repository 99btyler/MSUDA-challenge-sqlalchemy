from flask import Flask
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
    return "this is the index"

# main
if __name__ == "__main__":
    app.run(port=8000, debug=True)