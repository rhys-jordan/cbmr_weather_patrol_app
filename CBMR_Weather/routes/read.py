from CBMR_Weather.routes import bp_read
from flask import render_template, request
from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow, Avalanche
from sqlalchemy import desc
from sqlalchemy import create_engine
#import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import json


@bp_read.route("/read", methods=['GET', 'POST'])
def read():
    seasons_db = db.session.query(Snow.season).distinct()
    seasons = []
    for s in seasons_db:
        seasons.append(s[0])

    if request.method == 'POST':
        data_request_1 = request.form.get("data_1")
        season_1 = request.form.get("season_1")
        title_1 = data_request_1 + " for " + season_1 + " season"
        if data_request_1 == "YTD Snow":
            dates_1, data_1 = get_hn24_ytd_snow(season_1)
            title_1="YTD Snow (inches)"

        elif data_request_1 == "YTD Swe":
            dates_1, data_1 = get_swe_ytd_swe(season_1)
            title_1 = "YTD Swe"

        elif data_request_1 == "hn24":
            dates_1, data_1 = get_hn24(season_1)
            title_1 = "hn24 (inches)"

        elif data_request_1 == "hs":
            dates_1, data_1 = get_hs(season_1)
            title_1 = "hs (inches)"

        elif data_request_1 == "temp":
            dates_1, data_1 = get_temp(season_1)
            title_1 = "Temperature (F)"
        else:
            dates_1=[]
            data_1=[]
            title_1=''
            y_label_1 = ''

        data_request_2 = request.form.get("data_2")
        season_2 = request.form.get("season_2")
        title_2 = data_request_2 + " for " + season_2 + " season"
        if data_request_2 == "YTD Snow":
            dates_2, data_2 = get_hn24_ytd_snow(season_2)
            title_2 = "YTD Snow (inches)"

        elif data_request_2 == "YTD Swe":
            dates_2, data_2 = get_swe_ytd_swe(season_2)
            title_2 = "YTD Swe"

        elif data_request_2 == "hn24":
            dates_2, data_2 = get_hn24(season_2)
            title_2 = "hn24 (inches)"

        elif data_request_2 == "hs":
            dates_2, data_2 = get_hs(season_2)
            title_2 = "hs (inches)"

        elif data_request_2 == "temp":
            dates_2, data_2 = get_temp(season_2)
            title_2 = "Temperature (F)"
        else:
            dates_2 = []
            data_2 = []
            title_2 = ''
            y_label_2 = ''
        data_request_3 = request.form.get("data_3")
        season_3 = request.form.get("season_3")
        title_3 = data_request_3 + " for " + season_3 + " season"
        if data_request_3 == "YTD Snow":
            dates_3, data_3 = get_hn24_ytd_snow(season_3)
            title_3 = "YTD Snow (inches)"

        elif data_request_3 == "YTD Swe":
            dates_3, data_3 = get_swe_ytd_swe(season_3)
            title_3 = "YTD Swe"

        elif data_request_3 == "hn24":
            dates_3, data_3 = get_hn24(season_3)
            title_3 = "hn24 (inches)"

        elif data_request_3 == "hs":
            dates_3, data_3 = get_hs(season_3)
            title_3 = "hs (inches)"

        elif data_request_3 == "temp":
            dates_3, data_3 = get_temp(season_3)
            title_3 = "Temperature (F)"
        else:
            dates_3 = []
            data_3 = []
            title_3 = ''
            y_label_3 = ''

        data_request_4 = request.form.get("data_4")
        season_4 = request.form.get("season_4")
        title_4 = data_request_4 + " for " + season_4 + " season"
        if data_request_4 == "YTD Snow":
            dates_4, data_4 = get_hn24_ytd_snow(season_4)
            title_4 = "YTD Snow (inches)"

        elif data_request_4 == "YTD Swe":
            dates_4, data_4 = get_swe_ytd_swe(season_4)
            title_4 = "YTD Swe"

        elif data_request_4 == "hn24":
            dates_4, data_4 = get_hn24(season_4)
            title_4 = "hn24 (inches)"

        elif data_request_4 == "hs":
            dates_4, data_4 = get_hs(season_4)
            title_4 = "hs (inches)"

        elif data_request_4 == "temp":
            dates_4, data_4 = get_temp(season_4)
            title_4 = "Temperature (F)"
        else:
            dates_4 = []
            data_4 = []
            title_4 = ''
            y_label_4 = ''
        return render_template('read.html', seasons=seasons,
                               dates_1=json.dumps(dates_1), data_1=data_1, title_1=json.dumps(title_1),
                               y_label_1=json.dumps(title_1),
                               dates_2=json.dumps(dates_2), data_2=data_2, title_2=json.dumps(title_2),
                               y_label_2=json.dumps(title_2),
                               dates_3=json.dumps(dates_3), data_3=data_3, title_3=json.dumps(title_3),
                               y_label_3=json.dumps(title_3),
                               dates_4=json.dumps(dates_4), data_4=data_4, title_4=json.dumps(title_4),
                               y_label_4=json.dumps(title_4))

    title_1 = "YTD Snow for 24-25 season"
    title_2 = title_1
    dates_1, data_1 = get_hn24_ytd_snow(seasons[0])
    dates_2 = dates_1
    data_2 = data_1

    title_3 = "YTD Snow for 24-25 season"
    title_4 = title_3
    dates_3=dates_2
    data_3=data_2
    dates_4 = dates_3
    data_4 = data_3
    return render_template('read.html', seasons=seasons,
                           dates_1=json.dumps(dates_1), data_1=data_1, title_1=json.dumps(title_1),
                           y_label_1=json.dumps(title_1),
                           dates_2=json.dumps(dates_2), data_2=data_2, title_2=json.dumps(title_2),
                           y_label_2=json.dumps(title_2),
                           dates_3=json.dumps(dates_3), data_3=data_3, title_3=json.dumps(title_3),
                           y_label_3=json.dumps(title_3),
                           dates_4=json.dumps(dates_4), data_4=data_4, title_4=json.dumps(title_4),
                           y_label_4=json.dumps(title_4))


def get_ytd_snow(start_date,end_date):
    ytd_snow = db.session.query(Snow.ytd_snow, Snow.date).filter(Snow.date.between(start_date,end_date)).order_by(Snow.date)
    dates = []
    snow = []
    for row in ytd_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')

        if (row[0] != None):
            dates.append(date_format)
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
            swe.append(row[0])
    return dates, swe

def get_hn24_ytd_snow(season):
    hn24_snow = db.session.query(Snow.hn24, Snow.date).filter(Snow.season == season).order_by(Snow.date)
    dates = []
    ytd_snow = []
    past_hn24 = 0
    for row in hn24_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        dates.append(date_format)
        if (row[0] != None ):
            try:
                hn24=float(row[0])
                ytd_snow.append(hn24 + past_hn24)
                past_hn24 = hn24 + past_hn24
            except:
                hn24=0
        else:

            ytd_snow.append(0 + past_hn24 )
    return dates, ytd_snow


def get_swe_ytd_swe(season):
    swe = db.session.query(Snow.swe, Snow.date).filter(Snow.season == season).order_by(Snow.date)
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

def get_temp(season):
    temps = db.session.query(Snow.temperature, Snow.date).filter(Snow.season == season).order_by(Snow.date)
    dates = []
    temperatures = []
    for row in temps:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        if (row[0] != None):
            dates.append(date_format)
            # dates.append(str(inct))
            temperatures.append(row[0])
    return dates, temperatures

def get_hn24(season):
    hn24_snow_results = db.session.query(Snow.hn24, Snow.date).filter(Snow.season == season).order_by(Snow.date)
    dates = []
    hn24_snow = []
    for row in hn24_snow_results:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        dates.append(date_format)
        if (row[0] != None):
            try:
                hn24 = float(row[0])
                hn24_snow.append(hn24)
            except:
                hn24=0
        else:
            hn24_snow.append(0)

    return dates, hn24_snow

def get_hs(season):
    hs_snow_results = db.session.query(Snow.hs, Snow.date).filter(Snow.season == season).order_by(Snow.date)
    dates = []
    hs_snow = []
    for row in hs_snow_results:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        dates.append(date_format)
        if (row[0] != None and type(row[0]) != str):
            hs_snow.append(row[0] )
        # else:
        #     hs_snow.append(0)
    return dates, hs_snow