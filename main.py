from idlelib.colorizer import DEBUG
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
from flask_apscheduler import APScheduler
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Image
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


from CBMR_Weather import create_app

app = create_app()
#NEED TO Make your own database. Copy from python anywhere and rename to CBMR_Weather.db and place in instance formula
#need dependencies. Import flask, json, sql stuff, report lab,.... Import all from app.py and generate_pdf files
if __name__ == '__main__':
    app.run()