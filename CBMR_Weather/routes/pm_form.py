from flask import render_template, request, send_file
from flask_login import login_required
from CBMR_Weather.generate_pdf_pm import generate_pdf_pm
from datetime import datetime

from CBMR_Weather.routes import bp_pm_form
from CBMR_Weather.models import Snow

@bp_pm_form.route('/pm-form', methods=['GET', 'POST'])
@login_required
def pm_form():
    if request.method == 'POST':

        date = request.form.get('datetime', None)
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        ytd_snow = request.form.get('ytd_snow', None)
        weather_fx = request.form.get('weather_fx', None)
        tonight = request.form.get('tonight', None)
        tomorrow = request.form.get('tomorrow', None)
        tomorrow_night = request.form.get('tomorrow_night', None)
        mitigation = request.form.get('mitigation', None)

        if request.form.get('uphill_access', None) == 'paradise':
            uphill_access =  'Open to top of Paradise'
        elif request.form.get('uphill_access', None) == 'peanut':
            uphill_access = 'Open to Peanut'
        else:
            uphill_access = 'Not Open'
        basic_stats = [hs, hn24, ytd_snow, uphill_access]

        pdf_filename = generate_pdf_pm(date, forecaster, basic_stats, weather_fx, tonight, tomorrow, tomorrow_night, mitigation)
        return send_file(pdf_filename, as_attachment=True)  #


    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        snow = Snow.query.filter_by(date=now.strftime("%Y-%m-%d")).first()
        return render_template('pm-form.html', now=formatted_now, snow=snow) #, oldSnow=snow,avalanches=avalanche)