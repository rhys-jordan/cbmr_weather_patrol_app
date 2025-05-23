from calendar import month

import datetime
from flask import Flask, render_template, request, redirect, jsonify
from flask import Flask, render_template, request, redirect, send_file, after_this_request, session, url_for
from flask_json import FlaskJSON, json_response, as_json, JsonError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import foreign, relationship
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from datetime import datetime, timedelta
from generate_pdf_am import generate_pdf
from generate_pdf_pm import generate_pdf_pm
from job_delete_pdf_files import delete_files
from flask_apscheduler import APScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db' #Local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/CBMRPatrolApp/database/CBMR_Weather.db' #pythonAnywhere
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

class Pm_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    forecaster = db.Column(db.String)
    hs = db.Column(db.Float)  # Snow height (HS)
    hn24 = db.Column(db.Float)  # 24-hour new snow (HN24)
    ytd_snow = db.Column(db.Float)  # Year-to-date snow (YTD)
    ytd_swe = db.Column(db.Float)
    weather_fx = db.Column(db.String)
    tonight_tomorrow = db.Column(db.String)
    do_today = db.Column(db.String)
    plan_to_do = db.Column(db.String)
    mitigation = db.Column(db.String)
    uphill_access= db.Column(db.String)

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

@app.route('/resetEmail', methods = ['POST'])
def reset_email():

    # snowsafetycb@gmail.com
    # CB email_key:

    sender_email = "clynckejje328@gmail.com"
    receiver_email = "clynckejje328@gmail.com"
    email_key = "rmzx qdnl ovtr psmu"

    subject = "CBMR Patrol App Reset Login"

    link = "http://127.0.0.1:5000/loginReset" #local
    #link = "https://cbmrpatrolapp.pythonanywhere.com/loginReset.html" #pythonAnywhere
    confirmation_key = "8493"

    user = User.query.filter_by(id=1).first()
    username = user.username
    password = user.password

    body = f"""
        Hello,
        
        Your current username is: {username}
        Your current password is: {password}
        
        If you want to change your username and password:
        Use the link and confirmation key below.

        Here is the password reset link: {link}
        Your confirmation key is: {confirmation_key}

        Please do not share this information.

        Hoping for snow,
        CBMR Ski Patrol
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_key)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

    return redirect("/login")

@app.route('/loginReset', methods = ['GET', 'POST'])
def login_reset():

    user = User.query.filter_by(id=1).first()
    username = user.username
    password = user.password

    if request.method == 'POST':
        resetCode = request.form.get('resetCode', None)
        new_username = request.form.get('new_username', None)
        confirm_username = request.form.get('confirm_username', None)
        new_password = request.form.get('new_password', None)
        confirm_password = request.form.get('confirm_password', None)
        user = User.query.filter_by(username=username).first()
        if(resetCode != '8493'):
            return render_template('login_reset.html', error_message="Invalid Reset Code")
        if (new_username != confirm_username):
            return render_template('login_reset.html', error_message="Usernames do not match")
        if(new_password == ""):
            return render_template('login_reset.html', error_message="Password must be at least 1 character")
        if(new_password != confirm_password):
            return render_template('login_reset.html', error_message="Passwords do not match")
        if user.password == new_password:
            return render_template('login_reset.html', error_message="Your new password can not be the same as your old password")

        print(user.username)

        user.username = new_username if new_username else user.username
        user.password = new_password
        db.session.commit()

        return render_template('loginform_user.html')

    return render_template('loginReset.html')

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
    snow = Snow.query.order_by(desc(Snow.date)).all()
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
        ytd_snow = request.form.get('ytd_snow', None)
        swe= request.form.get('swe', None) #this is new!! need to add to database
        ytd_swe=request.form.get('ytd_swe', None) #this is new!! need to add to database
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        #past
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        past_24_hst = request.form.get('past_24_hst', None)
        past_24_date_cir = request.form.get('past_24_date_cir', None)
        past_24_settlement = request.form.get('past_24_settlement', None)
        past_24_hn24 = request.form.get('past_24_hn24', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        past_24_hn24_percent= request.form.get('past_24_hn24_percent', None)
        past_24_wind_mph = request.form.get('past_24_wind_mph', None)
        past_24_wind_direction = request.form.get('past_24_wind_direction', None)
        past_24_temp_high = request.form.get('past_24_temp_high', None)
        past_24_temp_low = request.form.get('past_24_temp_low', None)
        #future
        future_precip_rate = request.form.get('future_precip_rate', None)
        future_temp_high = request.form.get('future_temp_high', None)
        future_temp_low = request.form.get('future_temp_low', None)
        future_wind_mph = request.form.get('future_wind_mph', None)
        future_wind_direction = request.form.get('future_wind_direction', None)


        pwl=request.form.get('pwl', None)
        pwl_date_raw = request.form.get('pwl_date')
        if pwl_date_raw:
            pwl_date = datetime.strptime(pwl_date_raw, '%Y-%m-%d')
        else:
            pwl_date = None

        current_peak_gust_mph = request.form.get('current_peak_gust_mph', None)
        current_peak_gust_mph = float(current_peak_gust_mph) if current_peak_gust_mph else None
        current_peak_gust_direction = request.form.get('current_peak_gust_direction', None)
        current_peak_gust_time_raw = request.form.get('current_peak_gust_time', None)
        if current_peak_gust_time_raw:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M').time()
        else:
            current_peak_gust_time = None

        past_24_peak_gust_mph = request.form.get('past_24_peak_gust_mph', None)
        past_24_peak_gust_mph = float(past_24_peak_gust_mph) if past_24_peak_gust_mph else None
        past_24_peak_gust_direction = request.form.get('past_24_peak_gust_direction', None)
        past_24_peak_gust_time_raw = request.form.get('past_24_peak_gust_time', None)
        if past_24_peak_gust_time_raw:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M').time()
        else:
            past_24_peak_gust_time = None

        future_peak_gust_mph = request.form.get('future_peak_gust_mph', None)
        future_peak_gust_mph = float(future_peak_gust_mph) if future_peak_gust_mph else None
        future_peak_gust_direction = request.form.get('future_peak_gust_direction', None)
        future_peak_gust_time_raw = request.form.get('future_peak_gust_time', None)
        if future_peak_gust_time_raw:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M').time()
        else:
            future_peak_gust_time = None

        # formatting to types to match database
        hs = float(hs) if hs else None
        hn24 = float(hn24) if hn24 else None
        hst = float(hst) if hst else None
        ytd_snow = float(ytd_snow) if ytd_snow else None
        ytd_swe = float(ytd_swe) if ytd_swe else None
        swe= float(swe) if swe else None

        #current
        sky = request.form.get('sky', None)
        current_precip_rate = str(current_precip_rate) if current_precip_rate else None
        temperature = float(temperature) if temperature else None
        wind_mph = request.form.get('current_wind_mph', None)
        wind_direction = request.form.get('current_wind_direction', None)
        #past conversions
        past_24_hst = float(past_24_hst) if past_24_hst else None

        past_24_date_cir_raw = request.form.get('past_24_date_cir', '').strip()
        if past_24_date_cir_raw:
            past_24_date_cir = datetime.strptime(past_24_date_cir, '%Y-%m-%d')
        else:
            past_24_date_cir = None
        past_24_settlement = float(past_24_settlement) if past_24_settlement else None
        past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
        past_24_hn24 = float(past_24_hn24) if past_24_hn24 else None
        past_24_hn24_percent = float(past_24_hn24_percent) if past_24_hn24_percent else None
        past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
        past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
        #future conversions
        future_precip_rate = str(future_precip_rate) if future_precip_rate else None
        future_temp_high = float(future_temp_high) if future_temp_high else None
        future_temp_low = float(future_temp_low) if future_temp_low else None
        #avalanche conversions

        avalanche_danger_resort = request.form.get('avalanche_danger_resort', None)
        avalanche_danger_backcountry = request.form.get('avalanche_danger_backcountry', None)
        # problem 1
        avalanche_problem_1 = request.form.get('avalanche_problem_1', None)
        btl_aspect_1 = request.form.getlist('btl_aspect_1[]')
        btl_aspect_1 = '-'.join(btl_aspect_1)
        ntl_aspect_1 = request.form.getlist('ntl_aspect_1[]')
        ntl_aspect_1 = '-'.join(ntl_aspect_1)
        atl_aspect_1 = request.form.getlist('atl_aspect_1[]')
        atl_aspect_1 = '-'.join(atl_aspect_1)

        size_1 = request.form.get('size_1', None)
        likelihood_1 = request.form.get('likelihood_1', None)
        location1=request.form.get('location1', None)
        # problem 2
        avalanche_problem_2 = request.form.get('avalanche_problem_2', None)
        btl_aspect_2 = request.form.getlist('btl_aspect_2[]')
        btl_aspect_2 = '-'.join(btl_aspect_2)
        ntl_aspect_2 = request.form.getlist('ntl_aspect_2[]')
        ntl_aspect_2 = '-'.join(ntl_aspect_2)
        atl_aspect_2 = request.form.getlist('atl_aspect_2[]')
        atl_aspect_2 = '-'.join(atl_aspect_2)
        size_2 = request.form.get('size_2', None)
        likelihood_2 = request.form.get('likelihood_2', None)
        location2 = request.form.get('location2', None)
        #problem 3
        avalanche_problem_3 = request.form.get('avalanche_problem_3', None)
        btl_aspect_3 = request.form.getlist('btl_aspect_3[]')
        btl_aspect_3 = '-'.join(btl_aspect_3)
        ntl_aspect_3 = request.form.getlist('ntl_aspect_3[]')
        ntl_aspect_3 = '-'.join(ntl_aspect_3)
        atl_aspect_3 = request.form.getlist('atl_aspect_3[]')
        atl_aspect_3 = '-'.join(atl_aspect_3)
        size_3 = request.form.get('size_3', None)
        likelihood_3 = request.form.get('likelihood_3', None)
        location3 = request.form.get('location3', None)
        # problem 4
        avalanche_problem_4 = request.form.get('avalanche_problem_4', None)
        btl_aspect_4 = request.form.getlist('btl_aspect_4[]')
        btl_aspect_4 = '-'.join(btl_aspect_4)
        ntl_aspect_4 = request.form.getlist('ntl_aspect_4[]')
        ntl_aspect_4 = '-'.join(ntl_aspect_4)
        atl_aspect_4 = request.form.getlist('atl_aspect_4[]')
        atl_aspect_4 = '-'.join(atl_aspect_4)
        size_4 = request.form.get('size_4', None)
        likelihood_4 = request.form.get('likelihood_4', None)
        location4 = request.form.get('location4', None)

        #text box conversions
        observation_notes=request.form.get('observation_notes', None) #this is new!! need to add to database
        critical_info = request.form.get('critical_information', None)
        weather_forecast = request.form.get('weather_forecast', None)
        avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
        summary_previous_day = request.form.get('summary_previous_day', None)
        mitigation_plan = request.form.get('mitigation_plan', None)
        pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if not dateCheck:
            print(avalanche_problem_1, avalanche_problem_2, avalanche_problem_3, avalanche_problem_4)
            snow = Snow(dateTime=dateTime,date=date, day=day, month=month, year=year, time=time, season=season, forecaster=forecaster, hs=hs, hn24=hn24,swe=swe, hst=hst, ytd_snow=ytd_snow, ytd_swe=ytd_swe, sky=sky, temperature=temperature, wind_mph=wind_mph, wind_direction=wind_direction, observation_notes=observation_notes, critical_info=critical_info, weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion, summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan, pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate, past_24_hst=past_24_hst, past_24_settlement=past_24_settlement,past_24_date_cir=past_24_date_cir, future_precip_rate=future_precip_rate, past_24_hn24_swe=past_24_hn24_swe, past_24_hn24=past_24_hn24, past_24_hn24_percent=past_24_hn24_percent, future_temp_high=future_temp_high, past_24_wind_mph=past_24_wind_mph, past_24_wind_direction=past_24_wind_direction, future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high, future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low, future_wind_direction=future_wind_direction, avalanche_danger_resort=avalanche_danger_resort, avalanche_danger_backcountry=avalanche_danger_backcountry,pwl=pwl,pwl_date=pwl_date,current_peak_gust_mph=current_peak_gust_mph,current_peak_gust_direction=current_peak_gust_direction,current_peak_gust_time=current_peak_gust_time,past_24_peak_gust_mph=past_24_peak_gust_mph,past_24_peak_gust_direction=past_24_peak_gust_direction,past_24_peak_gust_time=past_24_peak_gust_time,future_peak_gust_mph=future_peak_gust_mph,future_peak_gust_direction=future_peak_gust_direction,future_peak_gust_time=future_peak_gust_time)
            db.session.add(snow)

            id = Snow.query.filter_by(date=date).first().id

            if avalanche_problem_1:
                avy1 = Avalanche(problem=avalanche_problem_1, size = size_1, likelihood = likelihood_1, btl_aspect=btl_aspect_1,ntl_aspect=ntl_aspect_1,atl_aspect=atl_aspect_1, location=location1, Snow_id=id)
                db.session.add(avy1)
            if avalanche_problem_2:
                avy2 = Avalanche(problem=avalanche_problem_2, size = size_2, likelihood = likelihood_2, btl_aspect=btl_aspect_2,ntl_aspect=ntl_aspect_2,atl_aspect=atl_aspect_2, location=location2, Snow_id=id)
                db.session.add(avy2)
            if avalanche_problem_3:
                avy3 = Avalanche(problem=avalanche_problem_3, size = size_3,  likelihood= likelihood_3, btl_aspect=btl_aspect_3,ntl_aspect=ntl_aspect_3,atl_aspect=atl_aspect_3,  location=location3, Snow_id=id)
                db.session.add(avy3)
            if avalanche_problem_4:
                avy4 = Avalanche(problem=avalanche_problem_4, size = size_4,  likelihood= likelihood_4, btl_aspect=btl_aspect_4,ntl_aspect=ntl_aspect_4,atl_aspect=atl_aspect_4,  location=location4, Snow_id=id)
                db.session.add(avy4)

            db.session.commit()
            pdf_filename = generate_pdf(date)
            #return redirect('/view')
            return send_file(pdf_filename, as_attachment=True) #
        else:
            return render_template('confirm.html', flash_message=True)
    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        day_before = now - timedelta(days=1)
        dateBefore = day_before.strftime("%Y-%m-%d")
        snow = Snow.query.filter_by(date=dateBefore).first()
        if snow:
            if snow.ytd_snow == None:
                snow.ytd_snow=0
            if snow.ytd_swe == None:
                snow.ytd_swe=0
            return render_template('am-form.html', now=formatted_now, ytd_snowPre=snow.ytd_snow,ytd_swePre=snow.ytd_swe,critical_info=snow.critical_info,observation_notes=snow.observation_notes,weather_forecast=snow.weather_forecast,avalanche_forecast_discussion=snow.avalanche_forecast_discussion,summary_previous_day=snow.summary_previous_day,mitigation_plan=snow.mitigation_plan,pertinent_terrain_info=snow.pertinent_terrain_info)
        else:
            return render_template('am-form.html', now=formatted_now, ytd_snowPre=0,ytd_swePre=0, critical_info="",observation_notes="",weather_forecast="",avalanche_forecast_discussion="",summary_previous_day="",mitigation_plan="",pertinent_terrain_info="")


@app.route('/pm-form', methods=['GET', 'POST'])
@login_required
def pm_form():
    if request.method == 'POST':
        date = request.form.get('datetime', None)
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        ytd_snow = request.form.get('ytd_snow', None)
        ytd_swe= request.form.get('ytd_swe', None)
        weather_fx = request.form.get('weather_fx', None)
        tonight_tomorrow = request.form.get('tonight_tomorrow', None)
        do_today = request.form.get('do_today', None)
        plan_to_do = request.form.get('plan_to_do', None)
        mitigation = request.form.get('mitigation', None)
        if request.form.get('uphill_access', None) == 'paradise':
            uphill_access =  'Open to top of Paradise'
        elif request.form.get('uphill_access', None) == 'peanut':
            uphill_access = 'Open to Peanut'
        else:
            uphill_access = 'Not Open'
        basic_stats = [hs, hn24, ytd_snow, ytd_swe, uphill_access]
        pdf_filename = generate_pdf_pm(date, forecaster, basic_stats, weather_fx, tonight_tomorrow, do_today, plan_to_do, mitigation)
        return send_file(pdf_filename, as_attachment=True)  #

    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        snow = Snow.query.filter_by(date=now.strftime("%Y-%m-%d")).first()
        return render_template('pm-form.html', now=formatted_now, snow=snow) #, oldSnow=snow,avalanches=avalanche)


@app.route('/update-form/<inputDate>', methods=['GET', 'POST'])
@login_required
def update_form(inputDate):
    if request.method == 'POST':
        #time functions
        print('post')
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
        ytd_snow = request.form.get('ytd_snow', None)
        swe= request.form.get('swe', None) #this is new!! need to add to database
        ytd_swe=request.form.get('ytd_swe', None) #this is new!! need to add to database
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        #past
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        past_24_hst = request.form.get('past_24_hst', None)
        past_24_date_cir = request.form.get('past_24_date_cir', None)
        past_24_settlement = request.form.get('past_24_settlement', None)
        past_24_hn24 = request.form.get('past_24_hn24', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        past_24_hn24_percent= request.form.get('past_24_hn24_percent', None)
        past_24_wind_mph = request.form.get('past_24_wind_mph', None)
        past_24_wind_direction = request.form.get('past_24_wind_direction', None)
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
        ytd_snow = float(ytd_snow) if ytd_snow else None
        ytd_swe = float(ytd_swe) if ytd_swe else None
        swe= float(swe) if swe else None

        #current
        sky = request.form.get('sky', None)
        current_precip_rate = str(current_precip_rate) if current_precip_rate else None
        temperature = float(temperature) if temperature else None
        wind_mph = request.form.get('current_wind_mph', None)
        wind_direction = request.form.get('current_wind_direction', None)
        #past conversions
        past_24_hst = float(past_24_hst) if past_24_hst else None

        past_24_date_cir_raw = request.form.get('past_24_date_cir', '').strip()
        if past_24_date_cir_raw:
            past_24_date_cir = datetime.strptime(past_24_date_cir, '%Y-%m-%d')
        else:
            past_24_date_cir = None
        past_24_settlement = float(past_24_settlement) if past_24_settlement else None
        past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
        past_24_hn24 = float(past_24_hn24) if past_24_hn24 else None
        past_24_hn24_percent = float(past_24_hn24_percent) if past_24_hn24_percent else None
        past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
        past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
        #future conversions
        future_precip_rate = str(future_precip_rate) if future_precip_rate else None
        future_temp_high = float(future_temp_high) if future_temp_high else None
        future_temp_low = float(future_temp_low) if future_temp_low else None

        pwl = request.form.get('pwl', None)
        pwl_date_raw = request.form.get('pwl_date')
        if pwl_date_raw:
            pwl_date = datetime.strptime(pwl_date_raw, '%Y-%m-%d')
        else:
            pwl_date = None

        current_peak_gust_mph = request.form.get('current_peak_gust_mph', None)
        current_peak_gust_mph = float(current_peak_gust_mph) if current_peak_gust_mph else None
        current_peak_gust_direction = request.form.get('current_peak_gust_direction', None)
        current_peak_gust_time_raw = request.form.get('current_peak_gust_time', None)
        if current_peak_gust_time_raw:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M:%S').time()
        else:
            current_peak_gust_time = None

        past_24_peak_gust_mph = request.form.get('past_24_peak_gust_mph', None)
        past_24_peak_gust_mph = float(past_24_peak_gust_mph) if past_24_peak_gust_mph else None
        past_24_peak_gust_direction = request.form.get('past_24_peak_gust_direction', None)
        past_24_peak_gust_time_raw = request.form.get('past_24_peak_gust_time', None)
        if past_24_peak_gust_time_raw:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M:%S').time()
        else:
            past_24_peak_gust_time = None

        future_peak_gust_mph = request.form.get('future_peak_gust_mph', None)
        future_peak_gust_mph = float(future_peak_gust_mph) if future_peak_gust_mph else None
        future_peak_gust_direction = request.form.get('future_peak_gust_direction', None)
        future_peak_gust_time_raw = request.form.get('future_peak_gust_time', None)
        if future_peak_gust_time_raw:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M:%S').time()
        else:
            future_peak_gust_time = None

        #avalanche conversions

        avalanche_danger_resort = request.form.get('avalanche_danger_resort', None)
        avalanche_danger_backcountry = request.form.get('avalanche_danger_backcountry', None)
        # problem 1
        avalanche_problem_1 = request.form.get('avalanche_problem_1', None)
        btl_aspect_1 = request.form.getlist('btl_aspect_1[]')
        btl_aspect_1 = '-'.join(btl_aspect_1)
        ntl_aspect_1 = request.form.getlist('ntl_aspect_1[]')
        ntl_aspect_1 = '-'.join(ntl_aspect_1)
        atl_aspect_1 = request.form.getlist('atl_aspect_1[]')
        atl_aspect_1 = '-'.join(atl_aspect_1)

        size_1 = request.form.get('size_1', None)
        likelihood_1 = request.form.get('likelihood_1', None)
        location1 = request.form.get('location1', None)
        # problem 2
        avalanche_problem_2 = request.form.get('avalanche_problem_2', None)
        btl_aspect_2 = request.form.getlist('btl_aspect_2[]')
        btl_aspect_2 = '-'.join(btl_aspect_2)
        ntl_aspect_2 = request.form.getlist('ntl_aspect_2[]')
        ntl_aspect_2 = '-'.join(ntl_aspect_2)
        atl_aspect_2 = request.form.getlist('atl_aspect_2[]')
        atl_aspect_2 = '-'.join(atl_aspect_2)
        size_2 = request.form.get('size_2', None)
        likelihood_2 = request.form.get('likelihood_2', None)
        location2 = request.form.get('location2', None)
        #problem 3
        avalanche_problem_3 = request.form.get('avalanche_problem_3', None)
        btl_aspect_3 = request.form.getlist('btl_aspect_3[]')
        btl_aspect_3 = '-'.join(btl_aspect_3)
        ntl_aspect_3 = request.form.getlist('ntl_aspect_3[]')
        ntl_aspect_3 = '-'.join(ntl_aspect_3)
        atl_aspect_3 = request.form.getlist('atl_aspect_3[]')
        atl_aspect_3 = '-'.join(atl_aspect_3)
        size_3 = request.form.get('size_3', None)
        likelihood_3 = request.form.get('likelihood_3', None)
        location3 = request.form.get('location3', None)
        # problem 4
        avalanche_problem_4 = request.form.get('avalanche_problem_4', None)
        btl_aspect_4 = request.form.getlist('btl_aspect_4[]')
        btl_aspect_4 = '-'.join(btl_aspect_4)
        ntl_aspect_4 = request.form.getlist('ntl_aspect_4[]')
        ntl_aspect_4 = '-'.join(ntl_aspect_4)
        atl_aspect_4 = request.form.getlist('atl_aspect_4[]')
        atl_aspect_4 = '-'.join(atl_aspect_4)
        size_4 = request.form.get('size_4', None)
        likelihood_4 = request.form.get('likelihood_4', None)
        location4 = request.form.get('location4', None)

        #text box conversions
        observation_notes=request.form.get('observation_notes', None) #this is new!! need to add to database
        critical_info = request.form.get('critical_information', None)
        weather_forecast = request.form.get('weather_forecast', None)
        avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
        summary_previous_day = request.form.get('summary_previous_day', None)
        mitigation_plan = request.form.get('mitigation_plan', None)
        pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if dateCheck:
            Avalanche.query.filter_by(Snow_id=dateCheck.id).delete(synchronize_session=False)
            db.session.delete(dateCheck)
            db.session.commit()

        snow = Snow(dateTime=dateTime,date=date, day=day, month=month, year=year, time=time, season=season, forecaster=forecaster, hs=hs, hn24=hn24,swe=swe, hst=hst, ytd_snow=ytd_snow, ytd_swe=ytd_swe, sky=sky, temperature=temperature, wind_mph=wind_mph, wind_direction=wind_direction, observation_notes=observation_notes, critical_info=critical_info, weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion, summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan, pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate, past_24_hst=past_24_hst, past_24_settlement=past_24_settlement,past_24_date_cir=past_24_date_cir, future_precip_rate=future_precip_rate, past_24_hn24_swe=past_24_hn24_swe, past_24_hn24=past_24_hn24, past_24_hn24_percent=past_24_hn24_percent, future_temp_high=future_temp_high, past_24_wind_mph=past_24_wind_mph, past_24_wind_direction=past_24_wind_direction, future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high, future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low, future_wind_direction=future_wind_direction, avalanche_danger_resort=avalanche_danger_resort, avalanche_danger_backcountry=avalanche_danger_backcountry,pwl=pwl,pwl_date=pwl_date,current_peak_gust_mph=current_peak_gust_mph,current_peak_gust_direction=current_peak_gust_direction,current_peak_gust_time=current_peak_gust_time,past_24_peak_gust_mph=past_24_peak_gust_mph,past_24_peak_gust_direction=past_24_peak_gust_direction,past_24_peak_gust_time=past_24_peak_gust_time,future_peak_gust_mph=future_peak_gust_mph,future_peak_gust_direction=future_peak_gust_direction,future_peak_gust_time=future_peak_gust_time)
        db.session.add(snow)

        id = Snow.query.filter_by(date=date).first().id
        print(id)
        print("avy 1 aspects: "+btl_aspect_1+ " prob type "+avalanche_problem_1+"_ ")
        print("avalanceh 2 aspects: " + btl_aspect_2+ " prob type "+avalanche_problem_2+"_ ")
        print("avalanceh 3 aspects: " + btl_aspect_3+ " prob type "+avalanche_problem_3+"_ ")
        print("avalanceh 4 aspects: " + btl_aspect_4+ " prob type "+avalanche_problem_4+"_ ")
        if avalanche_problem_1:
            avy1 = Avalanche(problem=avalanche_problem_1, size=size_1, likelihood=likelihood_1, btl_aspect=btl_aspect_1,
                             ntl_aspect=ntl_aspect_1, atl_aspect=atl_aspect_1, location=location1, Snow_id=id)
            db.session.add(avy1)
        if avalanche_problem_2:
            avy2 = Avalanche(problem=avalanche_problem_2, size=size_2, likelihood=likelihood_2, btl_aspect=btl_aspect_2,
                             ntl_aspect=ntl_aspect_2, atl_aspect=atl_aspect_2, location=location2, Snow_id=id)
            db.session.add(avy2)
        if avalanche_problem_3:
            avy3 = Avalanche(problem=avalanche_problem_3, size=size_3, likelihood=likelihood_3, btl_aspect=btl_aspect_3,
                             ntl_aspect=ntl_aspect_3, atl_aspect=atl_aspect_3, location=location3, Snow_id=id)
            db.session.add(avy3)
        if avalanche_problem_4:
            avy4 = Avalanche(problem=avalanche_problem_4, size=size_4, likelihood=likelihood_4, btl_aspect=btl_aspect_4,
                             ntl_aspect=ntl_aspect_4, atl_aspect=atl_aspect_4, location=location4, Snow_id=id)
            db.session.add(avy4)

        db.session.commit()
        pdf_filename = generate_pdf(date)
        #return redirect('/view')
        return send_file(pdf_filename, as_attachment=True) #
    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        snow=Snow.query.filter_by(date=inputDate).first()
        snowId=snow.id
        avalanche=Avalanche.query.filter_by(Snow_id=snowId).all()
        print(avalanche)
        return render_template('update-form.html', oldSnow=snow,avalanches=avalanche)


@app.route('/past-data', methods=['GET', 'POST'])
@login_required
def past_data():
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
        ytd_snow = request.form.get('ytd_snow', None)
        swe= request.form.get('swe', None) #this is new!! need to add to database
        ytd_swe=request.form.get('ytd_swe', None) #this is new!! need to add to database
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        #past
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        past_24_hst = request.form.get('past_24_hst', None)
        past_24_date_cir = request.form.get('past_24_date_cir', None)
        past_24_settlement = request.form.get('past_24_settlement', None)
        past_24_hn24 = request.form.get('past_24_hn24', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        past_24_hn24_percent= request.form.get('past_24_hn24_percent', None)
        past_24_wind_mph = request.form.get('past_24_wind_mph', None)
        past_24_wind_direction = request.form.get('past_24_wind_direction', None)
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
        ytd_snow = float(ytd_snow) if ytd_snow else None
        ytd_swe = float(ytd_swe) if ytd_swe else None
        swe= float(swe) if swe else None

        #current
        sky = request.form.get('sky', None)
        current_precip_rate = str(current_precip_rate) if current_precip_rate else None
        temperature = float(temperature) if temperature else None
        wind_mph = request.form.get('current_wind_mph', None)
        wind_direction = request.form.get('current_wind_direction', None)
        #past conversions
        past_24_hst = float(past_24_hst) if past_24_hst else None
        past_24_date_cir_raw = request.form.get('past_24_date_cir', '').strip()
        if past_24_date_cir_raw:
            past_24_date_cir = datetime.strptime(past_24_date_cir, '%Y-%m-%d')
        else:
            past_24_date_cir = None
        past_24_settlement = float(past_24_settlement) if past_24_settlement else None
        past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
        past_24_hn24 = float(past_24_hn24) if past_24_hn24 else None
        past_24_hn24_percent = float(past_24_hn24_percent) if past_24_hn24_percent else None
        past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
        past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
        #future conversions
        future_precip_rate = str(future_precip_rate) if future_precip_rate else None
        future_temp_high = float(future_temp_high) if future_temp_high else None
        future_temp_low = float(future_temp_low) if future_temp_low else None

        pwl = request.form.get('pwl', None)
        pwl_date_raw = request.form.get('pwl_date')
        if pwl_date_raw:
            pwl_date = datetime.strptime(pwl_date_raw, '%Y-%m-%d')
        else:
            pwl_date = None

        current_peak_gust_mph = request.form.get('current_peak_gust_mph', None)
        current_peak_gust_mph = float(current_peak_gust_mph) if current_peak_gust_mph else None
        current_peak_gust_direction = request.form.get('current_peak_gust_direction', None)
        current_peak_gust_time_raw = request.form.get('current_peak_gust_time', None)
        if current_peak_gust_time_raw:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M').time()
        else:
            current_peak_gust_time = None

        past_24_peak_gust_mph = request.form.get('past_24_peak_gust_mph', None)
        past_24_peak_gust_mph = float(past_24_peak_gust_mph) if past_24_peak_gust_mph else None
        past_24_peak_gust_direction = request.form.get('past_24_peak_gust_direction', None)
        past_24_peak_gust_time_raw = request.form.get('past_24_peak_gust_time', None)
        if past_24_peak_gust_time_raw:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M').time()
        else:
            past_24_peak_gust_time = None

        future_peak_gust_mph = request.form.get('future_peak_gust_mph', None)
        future_peak_gust_mph = float(future_peak_gust_mph) if future_peak_gust_mph else None
        future_peak_gust_direction = request.form.get('future_peak_gust_direction', None)
        future_peak_gust_time_raw = request.form.get('future_peak_gust_time', None)
        if future_peak_gust_time_raw:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M').time()
        else:
            future_peak_gust_time = None

        #avalanche conversions

        avalanche_danger_resort = request.form.get('avalanche_danger_resort', None)
        avalanche_danger_backcountry = request.form.get('avalanche_danger_backcountry', None)
        # problem 1
        avalanche_problem_1 = request.form.get('avalanche_problem_1', None)
        btl_aspect_1 = request.form.getlist('btl_aspect_1[]')
        btl_aspect_1 = '-'.join(btl_aspect_1)
        ntl_aspect_1 = request.form.getlist('ntl_aspect_1[]')
        ntl_aspect_1 = '-'.join(ntl_aspect_1)
        atl_aspect_1 = request.form.getlist('atl_aspect_1[]')
        atl_aspect_1 = '-'.join(atl_aspect_1)

        size_1 = request.form.get('size_1', None)
        likelihood_1 = request.form.get('likelihood_1', None)
        location1 = request.form.get('location1', None)
        # problem 2
        avalanche_problem_2 = request.form.get('avalanche_problem_2', None)
        btl_aspect_2 = request.form.getlist('btl_aspect_2[]')
        btl_aspect_2 = '-'.join(btl_aspect_2)
        ntl_aspect_2 = request.form.getlist('ntl_aspect_2[]')
        ntl_aspect_2 = '-'.join(ntl_aspect_2)
        atl_aspect_2 = request.form.getlist('atl_aspect_2[]')
        atl_aspect_2 = '-'.join(atl_aspect_2)
        size_2 = request.form.get('size_2', None)
        likelihood_2 = request.form.get('likelihood_2', None)
        location2 = request.form.get('location2', None)
        # problem 3
        avalanche_problem_3 = request.form.get('avalanche_problem_3', None)
        btl_aspect_3 = request.form.getlist('btl_aspect_3[]')
        btl_aspect_3 = '-'.join(btl_aspect_3)
        ntl_aspect_3 = request.form.getlist('ntl_aspect_3[]')
        ntl_aspect_3 = '-'.join(ntl_aspect_3)
        atl_aspect_3 = request.form.getlist('atl_aspect_3[]')
        atl_aspect_3 = '-'.join(atl_aspect_3)
        size_3 = request.form.get('size_3', None)
        likelihood_3 = request.form.get('likelihood_3', None)
        location3 = request.form.get('location3', None)
        # problem 4
        avalanche_problem_4 = request.form.get('avalanche_problem_4', None)
        btl_aspect_4 = request.form.getlist('btl_aspect_4[]')
        btl_aspect_4 = '-'.join(btl_aspect_4)
        ntl_aspect_4 = request.form.getlist('ntl_aspect_4[]')
        ntl_aspect_4 = '-'.join(ntl_aspect_4)
        atl_aspect_4 = request.form.getlist('atl_aspect_4[]')
        atl_aspect_4 = '-'.join(atl_aspect_4)
        size_4 = request.form.get('size_4', None)
        likelihood_4 = request.form.get('likelihood_4', None)
        location4 = request.form.get('location4', None)

        #text box conversions
        observation_notes=request.form.get('observation_notes', None) #this is new!! need to add to database
        critical_info = request.form.get('critical_information', None)
        weather_forecast = request.form.get('weather_forecast', None)
        avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
        summary_previous_day = request.form.get('summary_previous_day', None)
        mitigation_plan = request.form.get('mitigation_plan', None)
        pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if not dateCheck:
            print(avalanche_problem_1, avalanche_problem_2, avalanche_problem_3, avalanche_problem_4)
            snow = Snow(dateTime=dateTime, date=date, day=day, month=month, year=year, time=time, season=season,
                        forecaster=forecaster, hs=hs, hn24=hn24, swe=swe, hst=hst, ytd_snow=ytd_snow, ytd_swe=ytd_swe,
                        sky=sky, temperature=temperature, wind_mph=wind_mph, wind_direction=wind_direction,
                        observation_notes=observation_notes, critical_info=critical_info,
                        weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion,
                        summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan,
                        pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate,
                        past_24_hst=past_24_hst, past_24_settlement=past_24_settlement,
                        past_24_date_cir=past_24_date_cir, future_precip_rate=future_precip_rate,
                        past_24_hn24_swe=past_24_hn24_swe, past_24_hn24=past_24_hn24,
                        past_24_hn24_percent=past_24_hn24_percent, future_temp_high=future_temp_high,
                        past_24_wind_mph=past_24_wind_mph, past_24_wind_direction=past_24_wind_direction,
                        future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high,
                        future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low,
                        future_wind_direction=future_wind_direction, avalanche_danger_resort=avalanche_danger_resort,
                        avalanche_danger_backcountry=avalanche_danger_backcountry,pwl=pwl,pwl_date=pwl_date,current_peak_gust_mph=current_peak_gust_mph,current_peak_gust_direction=current_peak_gust_direction,current_peak_gust_time=current_peak_gust_time,past_24_peak_gust_mph=past_24_peak_gust_mph,past_24_peak_gust_direction=past_24_peak_gust_direction,past_24_peak_gust_time=past_24_peak_gust_time,future_peak_gust_mph=future_peak_gust_mph,future_peak_gust_direction=future_peak_gust_direction,future_peak_gust_time=future_peak_gust_time)
            db.session.add(snow)

            id = Snow.query.filter_by(date=date).first().id
            print(id)

            if avalanche_problem_1:
                avy1 = Avalanche(problem=avalanche_problem_1, size=size_1, likelihood=likelihood_1,
                                 btl_aspect=btl_aspect_1, ntl_aspect=ntl_aspect_1, atl_aspect=atl_aspect_1,
                                 location=location1, Snow_id=id)
                db.session.add(avy1)
            if avalanche_problem_2:
                avy2 = Avalanche(problem=avalanche_problem_2, size=size_2, likelihood=likelihood_2,
                                 btl_aspect=btl_aspect_2, ntl_aspect=ntl_aspect_2, atl_aspect=atl_aspect_2,
                                 location=location2, Snow_id=id)
                db.session.add(avy2)
            if avalanche_problem_3:
                avy3 = Avalanche(problem=avalanche_problem_3, size=size_3, likelihood=likelihood_3,
                                 btl_aspect=btl_aspect_3, ntl_aspect=ntl_aspect_3, atl_aspect=atl_aspect_3,
                                 location=location3, Snow_id=id)
                db.session.add(avy3)
            if avalanche_problem_4:
                avy4 = Avalanche(problem=avalanche_problem_4, size=size_4, likelihood=likelihood_4,
                                 btl_aspect=btl_aspect_4, ntl_aspect=ntl_aspect_4, atl_aspect=atl_aspect_4,
                                 location=location4, Snow_id=id)
                db.session.add(avy4)

            db.session.commit()
            pdf_filename = generate_pdf(date)
            #return redirect('/view')
            return send_file(pdf_filename, as_attachment=True) #
        else:
            return render_template('confirm.html', flash_message=True)
    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        return render_template('past-data.html')


scheduler.start()
app.run() #this is destructive when put into python anywhere // please do not include app.run()