from flask import Flask, render_template, request, redirect, send_file
from flask_json import FlaskJSON, json_response, as_json, JsonError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import foreign
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from datetime import datetime
from io import StringIO
from generate_pdf import generate_pdf

app = Flask(__name__, static_url_path='/static')
json= FlaskJSON(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db'
app.config['SECRET_KEY']="secretKey"

db= SQLAlchemy(app)
class Snow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    forecaster=db.Column(db.String)
    season = db.Column(db.String) #Season ie 24-25
    hs = db.Column(db.Float)  # Snow height (HS)
    hn24 = db.Column(db.Float)  # 24-hour new snow (HN24)
    hst = db.Column(db.Float)  # Total storm snow (HST)
    ytd = db.Column(db.Float)  # Year-to-date snow (YTD)
    sky = db.Column(db.String)  # Sky condition
    temperature = db.Column(db.Float)  # Temperature in degrees
    wind_mph = db.Column(db.String)  # Wind speed words
    wind_direction = db.Column(db.String)  # Wind direction
    critical_info= db.Column(db.String)
    weather_forecast=db.Column(db.String)
    avalanche_problems=db.Column(db.String)
    avalanche_forecast_discussion=db.Column(db.String)
    summary_previous_day=db.Column(db.String)
    mitigation_plan=db.Column(db.String)
    pertinent_terrain_info=db.Column(db.String)
    current_precip_rate = db.Column(db.Float)  # Precipitation rate (current)
    past_24_hn24_hst_date_cir = db.Column(db.Float)  # HN24 / HST date cir (past 24 hours)
    future_precip_rate = db.Column(db.Float)  # Precipitation rate (future)
    past_24_hn24_swe = db.Column(db.Float)  # HN24 SWE (past 24 hours)
    future_temp_high = db.Column(db.Float)  # Temp high (future)
    past_24_wind_mph_direction = db.Column(db.String)  # Wind mph/direction (past 24 hours)
    future_temp_low = db.Column(db.Float)  # Temp low (future)
    past_24_temp_high = db.Column(db.Float)  # Temp high (past 24 hours)
    future_wind_mph = db.Column(db.String)  # Wind mph (future)
    past_24_temp_low = db.Column(db.Float)  # Temp low (past 24 hours)
    future_wind_direction = db.Column(db.String)  # Wind direction (future)




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
    if current_user.is_authenticated:
        return render_template("home.html")
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
            return render_template("home.html")
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

@app.route("/search",methods=['GET', 'POST'])
def search():
    snow = Snow.query.all()
    print(snow)
    return render_template('search.html', snow=snow)

@login_required
@app.route('/am-form', methods=['GET', 'POST'])
def am_form():
    if request.method == 'POST':
        print(request.form)  # Debugging print statement
        datetime_str = request.form.get('datetime')
        print(datetime_str)
        date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        print('line 107')
        if date.month < 7:
            season = str(date.year - 1)[2:] + "-" + str(date.year)[2:]  # Example: "24-25"
        else:
            season = str(date.year)[2:] + "-" + str(date.year + 1)[2:]  # Example: "24-25"
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        hst = request.form.get('hst', None)
        ytd = request.form.get('ytd', None)
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        future_precip_rate = request.form.get('future_precip_rate', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        future_temp_high = request.form.get('future_temp_high', None)
        past_24_wind_mph_direction = request.form.get('past_24_wind_mph_direction', None)
        future_temp_low = request.form.get('future_temp_low', None)
        past_24_temp_high = request.form.get('past_24_temp_high', None)
        future_wind_mph = request.form.get('future_wind_mph', None)
        past_24_temp_low = request.form.get('past_24_temp_low', None)
        future_wind_direction = request.form.get('future_wind_direction', None)

        hs = float(hs) if hs else None
        pdf_file = generate_pdf('2/18/2025')
        #return render_template('am-form.html'),
        return send_file(pdf_file,as_attachment=True)
    else:
        return render_template('am-form.html')



app.run()