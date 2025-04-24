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
        # Get form values and store them in previous_request
        previous_request = {
            'data_1': request.form['data_1'],
            'season_1': request.form['season_1'],
            'data_2': request.form['data_2'],
            'season_2': request.form['season_2'],
            'data_3': request.form['data_3'],
            'season_3': request.form['season_3'],
            'data_4': request.form['data_4'],
            'season_4': request.form['season_4']
        }

        # Process data for graph 1
        data_request_1 = previous_request['data_1']
        season_1 = previous_request['season_1']
        dates_1, data_1 = get_data_and_title(data_request_1, season_1)
        title_1 = data_request_1 + " for " + season_1 + " season"

        # Process data for graph 2
        data_request_2 = previous_request['data_2']
        season_2 = previous_request['season_2']
        dates_2, data_2 = get_data_and_title(data_request_2, season_2)
        title_2 = data_request_2 + " for " + season_2 + " season"

        # Process data for graph 3
        data_request_3 = previous_request['data_3']
        season_3 = previous_request['season_3']
        dates_3, data_3 = get_data_and_title(data_request_3, season_3)
        title_3 = data_request_3 + " for " + season_3 + " season"

        # Process data for graph 4
        data_request_4 = previous_request['data_4']
        season_4 = previous_request['season_4']
        dates_4, data_4 = get_data_and_title(data_request_4, season_4)
        title_4 = data_request_4 + " for " + season_4 + " season"

        # Render the template with the form data and graphs
        return render_template(
            'read.html',
            seasons=seasons,
            dates_1=json.dumps(dates_1), data_1=data_1, title_1=json.dumps(title_1),
            y_label_1=json.dumps(title_1),
            dates_2=json.dumps(dates_2), data_2=data_2, title_2=json.dumps(title_2),
            y_label_2=json.dumps(title_2),
            dates_3=json.dumps(dates_3), data_3=data_3, title_3=json.dumps(title_3),
            y_label_3=json.dumps(title_3),
            dates_4=json.dumps(dates_4), data_4=data_4, title_4=json.dumps(title_4),
            y_label_4=json.dumps(title_4),
            previous_request=previous_request  # Keep track of previous form data
        )

    # If the form has not been submitted, set default values for the graphs
    title_1 = "YTD Snow" + " for " + seasons[0] + " season"
    dates_1, data_1 = get_hn24_ytd_snow(seasons[0])
    title_2 = "YTD Swe" + " for " + seasons[0] + " season"
    dates_2, data_2 = get_swe_ytd_swe(seasons[0])
    title_3 = "HN24" + " for " + seasons[0] + " season"
    dates_3, data_3 = get_hn24(seasons[0])
    title_4 = "HS" + " for " + seasons[0] + " season"
    dates_4, data_4 = get_hs(seasons[0])
    previous_request = {
        'data_1': "YTD Snow",
        'season_1': seasons[0],
        'data_2': "YTD Swe",
        'season_2': seasons[0],
        'data_3': "hn24",
        'season_3': seasons[0],
        'data_4': "hs",
        'season_4': seasons[0],
    }

    # Render the template with default values
    return render_template(
        'read.html',
        seasons=seasons,
        dates_1=json.dumps(dates_1), data_1=data_1, title_1=json.dumps(title_1),
        y_label_1=json.dumps(title_1),
        dates_2=json.dumps(dates_2), data_2=data_2, title_2=json.dumps(title_2),
        y_label_2=json.dumps(title_2),
        dates_3=json.dumps(dates_3), data_3=data_3, title_3=json.dumps(title_3),
        y_label_3=json.dumps(title_3),
        dates_4=json.dumps(dates_4), data_4=data_4, title_4=json.dumps(title_4),
        y_label_4=json.dumps(title_4),
        previous_request=previous_request
    )

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
    ytd = db.session.query(Snow.ytd_snow, Snow.date).filter(Snow.season == season).order_by(Snow.date)
    dates = []
    ytd_snow = []
    past_hn24 = 0
    if season=='23-24' or season=='24-25':
        for row in hn24_snow:
            date_format = datetime.strftime(row[1], '%m-%d-%Y')
            dates.append(date_format)
            if (row[0] != None):
                try:
                    hn24 = float(row[0])
                    ytd_snow.append(hn24 + past_hn24)
                    past_hn24 = hn24 + past_hn24
                except:
                    hn24 = 0
            else:

                ytd_snow.append(0 + past_hn24)
    else:
        for row in ytd:
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
        if row[0] == 0:
            hs_snow.append(hs_snow[-1] if hs_snow else 0)
        if (row[0] != None and type(row[0]) != str):
            hs_snow.append(row[0])
        else:
            hs_snow.append(0)
    return dates, hs_snow

def get_data_and_title(data_request, season):
    if data_request == "YTD Snow":
        return get_hn24_ytd_snow(season)[0], get_hn24_ytd_snow(season)[1]
    elif data_request == "YTD Swe":
        return get_swe_ytd_swe(season)[0],  get_swe_ytd_swe(season)[1]
    elif data_request == "hn24":
        return get_hn24(season)[0],get_hn24(season)[1]
    elif data_request == "hs":
        return get_hs(season)[0], get_hs(season)[1]
    elif data_request == "temp":
        return get_temp(season)[0], get_temp(season)[1]
    else:
        return [], []