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
    date = db.Column(db.Date, nullable=False)
    season = db.Column(db.String, nullable=False) #Season ie 24-25
    hs = db.Column(db.Float, nullable=True)  # Snow height (HS)
    hn24 = db.Column(db.Float, nullable=True)  # 24-hour new snow (HN24)
    hst = db.Column(db.Float, nullable=True)  # Total storm snow (HST)
    ytd = db.Column(db.Float, nullable=True)  # Year-to-date snow (YTD)
    sky = db.Column(db.String, nullable=True)  # Sky condition
    temperature = db.Column(db.Float, nullable=True)  # Temperature in degrees
    wind_mph = db.Column(db.String, nullable=True)  # Wind speed words
    wind_direction = db.Column(db.String, nullable=True)  # Wind direction



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

@app.route("/search",methods=['GET', 'POST'])
def search():
    snow = Snow.query.all()
    print(snow)
    return render_template('search.html', snow=snow)

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
            return redirect('/search')
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
            return redirect('/search')
        else:
            print('Error')
            #alert user that the date has already been inputted.
    else:
        return render_template('past-data.html')

app.run()