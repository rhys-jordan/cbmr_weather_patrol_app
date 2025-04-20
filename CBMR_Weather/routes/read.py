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

def get_hn24_ytd_snow(start_date, end_date):
    hn24_snow = db.session.query(Snow.hn24, Snow.date).filter(Snow.date.between(start_date,end_date)).order_by(Snow.date)
    dates = []
    ytd_snow = []
    past_hn24 = 0
    for row in hn24_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        #day = datetime.strftime(row[1], '%d')
        #month = datetime.strftime(row[2], '%m')
        dates.append(date_format)
        #dates.append(str(row[2]) + '/' + str(row[1]))
        if (row[0] != None and type(row[0]) != str):
            #ytd_snow.append(row[0])
            ytd_snow.append(row[0] + past_hn24)
            past_hn24 = row[0] + past_hn24
        else:
            ytd_snow.append(0 + past_hn24 )
    return dates, ytd_snow


def get_swe_ytd_swe(start_date, end_date):
    swe = db.session.query(Snow.swe, Snow.date).filter(Snow.date.between(start_date,end_date)).order_by(Snow.date)
    dates = []
    ytd_swe = []
    past_hn24 = 0
    for row in swe:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        dates.append(date_format)
        if (row[0] != None and type(row[0]) != str):
            ytd_swe.append(row[0] + past_hn24)
            past_hn24 = row[0] + past_hn24
        else:
            ytd_swe.append(0 + past_hn24 )
    return dates, ytd_swe

def get_temp(start_date, end_date):
    temps = db.session.query(Snow.temperature, Snow.date).filter(Snow.date.between(start_date,end_date)).order_by(Snow.date)
    dates = []
    temperatures = []
    for row in temps:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        if (row[0] != None):
            dates.append(date_format)
            # dates.append(str(inct))
            temperatures.append(row[0])
    return dates, temperatures


@bp_read.route("/read", methods=['GET', 'POST'])
def read():
    dates_snow, snow = get_ytd_snow()
    dates_swe, swe = get_swe_snow()
    dates_ytd, hn24_ytd = get_hn24_ytd_snow('2024-10-01', '2025-05-01')
    dates_ytd_2, hn24_2 = get_hn24_ytd_snow('2024-10-01', '2025-05-01')
    dates_ytd_swe, ytd_swe = get_swe_ytd_swe('2024-10-01', '2025-05-01')
    #really struggling with comparing two seasons ytd snow
    #got to get the dates to line up correctly

    dates_temp, temperatures = get_temp('2024-10-01', '2025-05-01')

    return render_template('read.html', dates_snow = json.dumps(dates_ytd), ytd_snow = hn24_ytd,
                            dates_swe = json.dumps(dates_ytd_swe), ytd_swe = ytd_swe,
                           dates_temp =json.dumps(dates_temp), temps = temperatures)