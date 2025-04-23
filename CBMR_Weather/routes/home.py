from flask import render_template, request, redirect, session
from flask_login import  login_user,logout_user,current_user,login_required
from sqlalchemy import desc, asc

from CBMR_Weather.routes import bp_home
from CBMR_Weather import db
from CBMR_Weather.models import User, Snow, Avalanche, Pm_form

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
