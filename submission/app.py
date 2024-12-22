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
                        <li><span style="color:#006eff;">    /api/v1.0/tobs          </span> - returns a JSON list of the last 12 months of temperature data</li>
                        <li><span style="color:#006eff;">    /api/v1.0/start         </span> - returns a JSON list of the minimum, average, and maximum temperature from the specified range</li>
                        <li><span style="color:#006eff;">    /api/v1.0/start/end     </span> - returns a JSON list of the minimum, average, and maximum temperature from the specified range</li>
                    </ul>
                </body>
            </htm>
            """

# main
if __name__ == "__main__":
    app.run(port=8000, debug=True)