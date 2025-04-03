import datetime
from flask import Flask, render_template, request, redirect, jsonify
from flask import Flask, render_template, request, redirect, send_file, after_this_request, session, url_for
from flask_json import FlaskJSON, json_response, as_json, JsonError
from sqlalchemy import ForeignKey, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import foreign, relationship
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from datetime import datetime, timedelta
from CBMR_Weather.extensions import db, login_manager
from flask_apscheduler import APScheduler



def create_app():
    app = Flask(__name__, static_url_path='/static')
    #json = FlaskJSON(app)
    #"C:\Users\rhysj\OneDrive\Desktop\cbmr_weather_patrol_app\CBMR_Weather\instance\CBMR_Weather.db"
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db'  # Local
    #sqlite:///C:\Users\rhysj\OneDrive\Desktop\cbmr_weather_patrol_app\CBMR_Weather\instance\CBMR_Weather.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CBMR_Weather.db'  # Local
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/CBMRPatrolApp/database/CBMR_Weather.db' #pythonAnywhere
    app.config['SECRET_KEY'] = "secretKey"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

    db.init_app(app)


    from CBMR_Weather.routes import bp_home, bp_am_form, bp_forms, bp_read
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_am_form)
    app.register_blueprint(bp_forms)
    app.register_blueprint(bp_read)

    login_manager.login_view = "/"
    login_manager.init_app(app)

    return app



    '''
    #db.init_app(app)

    from CBMR_Weather.routes.home import home_bp

    #app.register_blueprint(am_form, url_prefix='/am-form')
    #app.register_blueprint(home_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = "/"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        user = User.query.get(uid)
        return user

    return app
    '''