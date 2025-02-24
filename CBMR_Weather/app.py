from flask import Flask, render_template, request, redirect
from flask_json import FlaskJSON, json_response, as_json, JsonError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import foreign
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
json= FlaskJSON(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db'
app.config['SECRET_KEY']="secretKey"




db= SQLAlchemy(app)
class Snow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    day= db.Column(db.Integer)
    month=db.Column(db.Integer)
    year=db.Column(db.Integer)
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
    #Other
    critical_info= db.Column(db.String)
    weather_forecast=db.Column(db.String)
    avalanche_problems=db.Column(db.String)
    avalanche_forecast_discussion=db.Column(db.String)
    summary_previous_day=db.Column(db.String)
    mitigation_plan=db.Column(db.String)
    pertinent_terrain_info=db.Column(db.String)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def handle_post_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect("/")
        else:
            return render_template('login_error_user.html')
    return render_template('loginform_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_required
@app.route("/forms", methods=['GET', 'POST'])
def forms():
    return render_template('forms.html')

@app.route("/read", methods=['GET', 'POST'])
def read():
    return render_template('read.html')

@app.route("/view",methods=['GET', 'POST'])
def view():
    snow = Snow.query.all()
    print(snow)
    return render_template('view.html', snow=snow)

@login_required
@app.route('/am-form', methods=['GET', 'POST'])
def am_form():
    if request.method=='POST':
        print(request.form)
        day= request.form['day']
        month = request.form['month']
        year = request.form['year']
        date_str=year+'-'+month+'-'+day
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        season=int(year[2]+year[3])
        hs= int(request.form['hs'])
        hn24 = int(request.form['hn24'])
        hst = int(request.form['hst'])
        ytd = int(request.form['ytd'])
        sky = request.form['sky']
        temp = int(request.form['current_temp'])
        wind_mph= request.form['current_wind_mph']
        wind_direction = request.form['current_wind_direction']
        dateCheck = Snow.query.filter_by(date=date).first()
        if(not dateCheck):
            snow= Snow(date=date,season=season, hs=hs,hn24=hn24,hst=hst,ytd=ytd,sky=sky,temperature=temp,wind_mph=wind_mph,wind_direction=wind_direction)
            db.session.add(snow)
            db.session.commit()
            return redirect('/view')
        else:
            print('Error')
            #alert user that the date has already been inputted.
    else:
        return render_template('am-form.html')

@login_required
@app.route('/pm-form', methods=['GET', 'POST'])
def pm_form():
        return render_template('pm-form.html')

@login_required
@app.route('/past-data', methods=['GET', 'POST'])
def past_data():
        return render_template('past-data.html')

#app.run() #this is destructive when put into python anywhere // please do not include app.run()