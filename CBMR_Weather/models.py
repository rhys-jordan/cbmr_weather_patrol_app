from CBMR_Weather.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Snow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    dateTime=db.Column(db.DateTime, nullable=False)
    day= db.Column(db.Integer)
    month=db.Column(db.Integer)
    year=db.Column(db.Integer)
    time=db.Column(db.Time)
    #top few lines
    forecaster=db.Column(db.String)
    season = db.Column(db.String) #Season ie 24-25
    hs = db.Column(db.Float)  # Snow height (HS)
    hn24 = db.Column(db.Float)  # 24-hour new snow (HN24)
    swe= db.Column(db.Float)
    hst = db.Column(db.Float)  # Total storm snow (HST)
    ytd_snow = db.Column(db.Float)  # Year-to-date snow (YTD)
    ytd_swe= db.Column(db.Float)
    #Current
    sky = db.Column(db.String)  # Sky condition
    current_precip_rate = db.Column(db.String)  # Precipitation rate (current)
    temperature = db.Column(db.Float)  # Temperature in degrees
    wind_mph = db.Column(db.String)  # Wind speed words
    wind_direction = db.Column(db.String)  # Wind direction
    #past 24 hr column
    past_24_hn24= db.Column(db.Float)
    past_24_hn24_swe = db.Column(db.Float)
    past_24_hn24_percent= db.Column(db.Float)
    past_24_hst=db.Column(db.Float)
    past_24_date_cir = db.Column(db.Date)
    past_24_settlement= db.Column(db.Float)
    past_24_wind_mph = db.Column(db.String)  # Wind mph/direction (past 24 hours)
    past_24_wind_direction = db.Column(db.String)
    past_24_temp_high = db.Column(db.Float)  # Temp high (past 24 hours)
    past_24_temp_low = db.Column(db.Float)  # Temp low (past 24 hours)
    #Future
    future_precip_rate = db.Column(db.String)   # Precipitation rate (future)
    future_temp_high = db.Column(db.Float)  # Temp high (future)
    future_temp_low = db.Column(db.Float)  # Temp low (future)
    future_wind_mph = db.Column(db.String)  # Wind mph (future)
    future_wind_direction = db.Column(db.String)  # Wind direction (future)
    pwl= db.Column(db.String)
    pwl_date= db.Column(db.Date)
    current_peak_gust_mph = db.Column(db.Float)  # Peak Gust MPH (current)
    current_peak_gust_direction = db.Column(db.String)  # Peak Gust Direction (current)
    current_peak_gust_time = db.Column(db.Time)  # Peak Gust Time (current)

    past_24_peak_gust_mph = db.Column(db.Float)  # Peak Gust MPH (past 24 hours)
    past_24_peak_gust_direction = db.Column(db.String)  # Peak Gust Direction (past 24 hours)
    past_24_peak_gust_time = db.Column(db.Time)  # Peak Gust Time (past 24 hours)

    future_peak_gust_mph = db.Column(db.Float)  # Peak Gust MPH (future)
    future_peak_gust_direction = db.Column(db.String)  # Peak Gust Direction (future)
    future_peak_gust_time = db.Column(db.Time)  # Peak Gust Time (future)
    #Avalanche
    avalanche_danger_resort = db.Column(db.String)
    avalanche_danger_backcountry = db.Column(db.String)
    #Other
    observation_notes=db.Column(db.String)
    critical_info = db.Column(db.String)
    weather_forecast = db.Column(db.String)
    avalanche_forecast_discussion=db.Column(db.String)
    summary_previous_day=db.Column(db.String)
    mitigation_plan=db.Column(db.String)
    pertinent_terrain_info=db.Column(db.String)
    #Avalanche Table Foreign Key
    children = relationship("Avalanche", back_populates="parent")





class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)


class Avalanche(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String)
    problem = db.Column(db.String)
    btl_aspect= db.Column(db.String)
    ntl_aspect= db.Column(db.String)
    atl_aspect= db.Column(db.String)
    size = db.Column(db.String)
    likelihood = db.Column(db.String)
    Snow_id = db.Column(db.Integer, ForeignKey('snow.id'))
    parent = relationship("Snow", back_populates="children")
