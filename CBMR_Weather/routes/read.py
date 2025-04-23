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
            return render_template('read.html',seasons = seasons,  dates_1=json.dumps(dates_1), data_1=data_1,
                                   title_1 = json.dumps(title_1), y_label = json.dumps("YTD Snow (inches)"))
        elif data_request_1 == "YTD Swe":
            dates_1, data_1 = get_swe_ytd_swe(season_1)
            return render_template('read.html',seasons = seasons,  dates_1=json.dumps(dates_1), data_1=data_1,
                                   title_1 = json.dumps(title_1), y_label = json.dumps("YTD Swe"))
        elif data_request_1 == "hn24":
            dates_1, data_1 = get_hn24(season_1)
            return render_template('read.html',seasons = seasons,  dates_1=json.dumps(dates_1), data_1=data_1,
                                   title_1 = json.dumps(title_1), y_label = json.dumps("hn24 (inches)"))
        elif data_request_1 == "hs":
            dates_1, data_1 = get_hs(season_1)
            return render_template('read.html', seasons=seasons, dates_1=json.dumps(dates_1), data_1=data_1,
                                   title_1=json.dumps(title_1), y_label=json.dumps("hs (inches)"))
        elif data_request_1 == "temp":
            dates_1, data_1 = get_temp(season_1)
            return render_template('read.html', seasons=seasons, dates_1=json.dumps(dates_1), data_1=data_1,
                                   title_1=json.dumps(title_1), y_label=json.dumps("Temperature (F)"))
        else:
            return render_template('read.html', seasons = seasons, dates_1=json.dumps([]),
                                   data_1=[], title_1=json.dumps(""), y_label = json.dumps(""))


    title_1 = "YTD Snow for 24-25 season"
    dates_1, data_1 = get_hn24_ytd_snow(seasons[0])
    return render_template('read.html', seasons = seasons, dates_1 = json.dumps(dates_1),
                           data_1 = data_1, title_1 = json.dumps(title_1), y_label = json.dumps("YTD Snow (inches)"))


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