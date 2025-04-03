
from flask import Flask, Blueprint, render_template, request, redirect, send_file, after_this_request, session, url_for
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required

from CBMR_Weather.routes import bp_home
from CBMR_Weather import db, login_manager
from CBMR_Weather.models import User

@bp_home.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('loginform_user.html')

@bp_home.route("/login", methods=['GET', 'POST'])
def handle_post_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(db)
        users = User.query.all()
        print(users)
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.password == password:
            login_user(user)
            session.permanent = True
            return redirect("/")
        else:
            return render_template('login_error_user.html')
    return render_template('loginform_user.html')

@bp_home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

'''
home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('loginform_user.html')


@home_bp.route("/login", methods=['GET', 'POST'])
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

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")'''