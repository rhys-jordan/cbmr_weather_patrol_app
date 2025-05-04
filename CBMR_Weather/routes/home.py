
import requests
import os
from flask import render_template, request, redirect, session
from flask_login import  login_user,logout_user,current_user,login_required
from sqlalchemy import desc, asc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


@bp_home.route('/resetEmail', methods=['POST'])
def reset_email():

    user = User.query.filter_by(id=1).first()
    username = user.username
    password = user.password
    confirmation_key = user.password

    # Mailgun credentials

    #PUT KEY HERE !!!!
    #key = ''

    DOMAIN = 'sandbox3dc3a9492c9e4cc38595dcfb7c65b4e0.mailgun.org'
    sender = f"CBMR Ski Patrol <mailgun@{DOMAIN}>"
    receiver = "snowsafetycb@gmail.com"

    # Compose the email content
    subject = "CBMR Patrol App Reset Login"
    text = f"""Hello,

    Your current username is: {username}
    Your current password is: {password}

    Use the link and confirmation key below.

    Reset link: https://cbmrpatrolapp.pythonanywhere.com/loginReset
    Confirmation key: {confirmation_key}

    Please do not share this information.

    Hoping for snow,
    CBMR Ski Patrol"""

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{DOMAIN}/messages",
            auth=("api", key),
            data={
                "from": sender,
                "to": receiver,
                "subject": subject,
                "text": text
            }
        )

        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Error sending email: {e}")

    return redirect("/login")


@bp_home.route('/loginReset', methods=['GET', 'POST'])
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
        if (resetCode != password):
            return render_template('loginReset.html', error_message="Invalid Reset Code")
        if (new_username != confirm_username):
            return render_template('loginReset.html', error_message="Usernames do not match")
        if (new_password == ""):
            return render_template('loginReset.html', error_message="Password must be at least 1 character")
        if (new_password != confirm_password):
            return render_template('loginReset.html', error_message="Passwords do not match")
        if user.password == new_password:
            return render_template('loginReset.html',
                                   error_message="Your new password can not be the same as your old password")

        print(user.username)

        user.username = new_username if new_username else user.username
        user.password = new_password
        db.session.commit()

        return render_template('loginform_user.html')

    return render_template('loginReset.html')


@bp_home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
