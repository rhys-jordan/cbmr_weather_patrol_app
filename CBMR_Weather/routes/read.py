from CBMR_Weather.routes import bp_read
from flask import render_template
from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow, Avalanche
from sqlalchemy import desc
from sqlalchemy import create_engine
#import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import json


def get_ytd_snow():
    ytd_snow = db.session.query(Snow.ytd_snow, Snow.date).order_by(Snow.date)
    dates = []
    snow = []
    for row in ytd_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')

        if (row[0] != None):
            dates.append(date_format)
            # dates.append(str(inct))
            snow.append(row[0])
    return dates, snow

def get_swe_snow():
    ytd_snow = db.session.query(Snow.ytd_swe, Snow.date).order_by(Snow.date)
    dates = []
    swe = []
    for row in ytd_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')

        if (row[0] != None):
            dates.append(date_format)
            # dates.append(str(inct))
            swe.append(row[0])
    return dates, swe


@bp_read.route("/read", methods=['GET', 'POST'])
def read():
    dates_snow, snow = get_ytd_snow()
    dates_swe, swe = get_swe_snow()

    return render_template('read.html', dates_snow = json.dumps(dates_snow), ytd_snow = snow,
                            dates_swe = json.dumps(dates_swe), ytd_swe = swe)