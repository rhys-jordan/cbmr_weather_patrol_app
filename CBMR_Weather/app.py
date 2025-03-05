from calendar import month

from flask import Flask, render_template, request, redirect, jsonify
from flask import Flask, render_template, request, redirect, send_file, after_this_request, session
from flask_json import FlaskJSON, json_response, as_json, JsonError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import foreign, relationship
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from datetime import datetime, timedelta
from generate_pdf import generate_pdf
from job_delete_pdf_files import delete_files
from flask_apscheduler import APScheduler


class Config_jobs:
    JOBS = [
        {
            "id": "job1",
            "func": delete_files,
            "trigger": "interval",
            "hours": 24,
        }
    ]

    SCHEDULER_API_ENABLED = True


app = Flask(__name__, static_url_path='/static')
json= FlaskJSON(app)
app.config.from_object(Config_jobs)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db'
app.config['SECRET_KEY']="secretKey"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

scheduler = APScheduler()
scheduler.init_app(app)

db= SQLAlchemy(app)

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
    hst = db.Column(db.Float)  # Total storm snow (HST)
    ytd = db.Column(db.Float)  # Year-to-date snow (YTD)
    #Current
    sky = db.Column(db.String)  # Sky condition
    current_precip_rate = db.Column(db.Float)  # Precipitation rate (current)
    temperature = db.Column(db.Float)  # Temperature in degrees
    wind_mph = db.Column(db.String)  # Wind speed words
    wind_direction = db.Column(db.String)  # Wind direction
    #past 24 hr column
    past_24_hn24_hst_date_cir = db.Column(db.Float)  # HN24 / HST date cir (past 24 hours)
    past_24_hn24_swe = db.Column(db.Float)  # HN24 SWE (past 24 hours)
    past_24_wind_mph_direction = db.Column(db.String)  # Wind mph/direction (past 24 hours)
    past_24_temp_high = db.Column(db.Float)  # Temp high (past 24 hours)
    past_24_temp_low = db.Column(db.Float)  # Temp low (past 24 hours)
    #Future
    future_precip_rate = db.Column(db.Float)  # Precipitation rate (future)
    future_temp_high = db.Column(db.Float)  # Temp high (future)
    future_temp_low = db.Column(db.Float)  # Temp low (future)
    future_wind_mph = db.Column(db.String)  # Wind mph (future)
    future_wind_direction = db.Column(db.String)  # Wind direction (future)
    #Avalanche
    avalanche_danger = db.Column(db.String)
    #Other
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
    problem = db.Column(db.String)
    size_likelihood = db.Column(db.String)
    aspect_elevation = db.Column(db.String)
    trend = db.Column(db.String)
    Snow_id = db.Column(db.Integer, ForeignKey('snow.id'))
    parent = relationship("Snow", back_populates="children")

with app.app_context():
    db.create_all()


login_manager = LoginManager(app)
login_manager.login_view = "/"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('loginform_user.html')


@app.route("/login", methods=['GET', 'POST'])
def handle_post_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            session.permanent = True
            return redirect("/")
        else:
            return render_template('login_error_user.html')
    return render_template('loginform_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/forms", methods=['GET', 'POST'])
@login_required
def forms():
    return render_template('forms.html')

@app.route("/read", methods=['GET', 'POST'])
def read():
    return render_template('read.html')

@app.route("/view",methods=['GET', 'POST'])
def view():
    snow = Snow.query.all()
    return render_template('view.html', snow=snow)


@app.route('/am-form', methods=['GET', 'POST'])
@login_required
def am_form():
    if request.method == 'POST':
        #time functions
        datetime_str = request.form.get('datetime')
        dateTime= datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        day= int(dateTime.day)
        month=int(dateTime.month)
        year=int(dateTime.year)
        time=dateTime.time()
        date = dateTime.date()
        if dateTime.month < 7:
            season = str(dateTime.year - 1)[2:] + "-" + str(dateTime.year)[2:]  # Example: "24-25"
        else:
            season = str(dateTime.year)[2:] + "-" + str(dateTime.year + 1)[2:]  # Example: "24-25"
        #Top of page
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        hst = request.form.get('hst', None)
        ytd = request.form.get('ytd', None)
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        #past
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        past_24_wind_mph_direction = request.form.get('past_24_wind_mph_direction', None)
        past_24_temp_high = request.form.get('past_24_temp_high', None)
        past_24_temp_low = request.form.get('past_24_temp_low', None)
        #future
        future_precip_rate = request.form.get('future_precip_rate', None)
        future_temp_high = request.form.get('future_temp_high', None)
        future_temp_low = request.form.get('future_temp_low', None)
        future_wind_mph = request.form.get('future_wind_mph', None)
        future_wind_direction = request.form.get('future_wind_direction', None)

        # formatting to types to match database
        hs = float(hs) if hs else None
        hn24 = float(hn24) if hn24 else None
        hst = float(hst) if hst else None
        ytd = float(ytd) if ytd else None

        #current
        sky = request.form.get('sky', None)
        current_precip_rate = float(current_precip_rate) if current_precip_rate else None
        temperature = float(temperature) if temperature else None
        wind_mph = request.form.get('current_wind_mph', None)
        wind_direction = request.form.get('current_wind_direction', None)
        #past conversions
        past_24_hn24_hst_date_cir = float(past_24_hn24_hst_date_cir) if past_24_hn24_hst_date_cir else None
        past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
        past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
        past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
        #future conversions
        future_precip_rate = float(future_precip_rate) if future_precip_rate else None
        future_temp_high = float(future_temp_high) if future_temp_high else None
        future_temp_low = float(future_temp_low) if future_temp_low else None
        #avalanche conversions
        avalanche_danger = request.form.get('avalanche_danger', None)
        # problem 1
        avalanche_problem_1 = request.form.get('avalanche_problem_1', None)
        aspect_elevation_1 = request.form.get('aspect_elevation_1', None)
        size_likelihood_1 = request.form.get('size_likelihood_1', None)
        trend_1 = request.form.get('trend_1', None)
        # problem 2
        avalanche_problem_2 = request.form.get('avalanche_problem_2', None)
        aspect_elevation_2 = request.form.get('aspect_elevation_2', None)
        size_likelihood_2 = request.form.get('size_likelihood_2', None)
        trend_2 = request.form.get('trend_2', None)
        #problem 3
        avalanche_problem_3 = request.form.get('avalanche_problem_3', None)
        aspect_elevation_3 = request.form.get('aspect_elevation_3', None)
        size_likelihood_3 = request.form.get('size_likelihood_3', None)
        trend_3 = request.form.get('trend_3', None)
        #text box conversions
        critical_info = request.form.get('critical_information', None)
        weather_forecast = request.form.get('weather_forecast', None)
        avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
        summary_previous_day = request.form.get('summary_previous_day', None)
        mitigation_plan = request.form.get('mitigation_plan', None)
        pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if not dateCheck:
            print(avalanche_problem_1, avalanche_problem_2, avalanche_problem_3)
            snow = Snow(dateTime=dateTime,date=date, day=day, month=month, year=year, time=time, season=season, forecaster=forecaster, hs=hs, hn24=hn24, hst=hst, ytd=ytd, sky=sky, temperature=temperature, wind_mph=wind_mph, wind_direction=wind_direction, critical_info=critical_info, weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion, summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan, pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate, past_24_hn24_hst_date_cir=past_24_hn24_hst_date_cir, future_precip_rate=future_precip_rate, past_24_hn24_swe=past_24_hn24_swe, future_temp_high=future_temp_high, past_24_wind_mph_direction=past_24_wind_mph_direction, future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high, future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low, future_wind_direction=future_wind_direction)
            db.session.add(snow)

            id = Snow.query.filter_by(date=date).first().id
            print(id)

            if avalanche_problem_1 != "":
                avy1 = Avalanche(problem=avalanche_problem_1, size_likelihood=size_likelihood_1, aspect_elevation=aspect_elevation_1, trend=trend_1, Snow_id=id)
                db.session.add(avy1)
            if avalanche_problem_2 != "":
                avy2 = Avalanche(problem=avalanche_problem_2, size_likelihood=size_likelihood_2, aspect_elevation=aspect_elevation_2, trend=trend_2, Snow_id=id)
                db.session.add(avy2)
            if avalanche_problem_3 != "":
                avy3 = Avalanche(problem=avalanche_problem_3, size_likelihood=size_likelihood_3, aspect_elevation=aspect_elevation_3, trend=trend_3, Snow_id=id)
                db.session.add(avy3)

            db.session.commit()
            pdf_filename = generate_pdf(date)
            #return redirect('/view'), send_file(pdf_filename, as_attachment=True)
            return send_file(pdf_filename, as_attachment=True)
        else:
            return render_template('confirm.html', flash_message=True)
    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        return render_template('am-form.html', now=formatted_now)


@app.route('/pm-form', methods=['GET', 'POST'])
@login_required
def pm_form():
        return render_template('pm-form.html')


@app.route('/past-data', methods=['GET', 'POST'])
@login_required
def past_data():
    return render_template('past-data.html')


scheduler.start()
app.run() #this is destructive when put into python anywhere // please do not include app.run()