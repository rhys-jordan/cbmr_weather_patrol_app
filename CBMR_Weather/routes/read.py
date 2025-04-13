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


@bp_read.route("/read", methods=['GET', 'POST'])
def read():
    #ytd_snow = Snow.query.get(Snow.ytd_snow)
    #ytd_snow = Snow.query(Snow.ytd_snow)
    ytd_snow = db.session.query(Snow.ytd_snow, Snow.date).order_by(Snow.date)
    #print(ytd_snow[1][0])
    dates = []
    snow = []
    inct = 0
    for row in ytd_snow:
        date_format = datetime.strftime(row[1], '%m-%d-%Y')
        dates.append(inct)
        inct = inct + 1
        snow.append(row[0])

    print(dates)
    #print(snow)
    #plt.plot(dates, snow)
    #plt.show()
    #st.write("My First App")
    #df = pd.DataFrame(SQL_Query, columns=['value1', 'value2'])
    #st.line_chart(df)


    return render_template('read.html', dates = json.dumps(dates), ytd_snow = snow)