from flask import render_template, request, send_file
from flask_login import login_required
from CBMR_Weather.generate_pdf_pm import generate_pdf_pm
from datetime import datetime, timedelta

from CBMR_Weather.routes import bp_pm_form
from CBMR_Weather.models import Snow, Pm_form
from CBMR_Weather.extensions import db

@bp_pm_form.route('/pm-form', methods=['GET', 'POST'])
@login_required
def pm_form():
    if request.method == 'POST':
        date = request.form.get('datetime', None)
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        ytd_snow = request.form.get('ytd_snow', None)
        ytd_swe = request.form.get('ytd_swe', None)
        weather_fx = request.form.get('weather_fx', None)
        tonight_tomorrow = request.form.get('tonight_tomorrow', None)
        do_today = request.form.get('do_today', None)
        plan_to_do = request.form.get('plan_to_do', None)
        mitigation = request.form.get('mitigation', None)
        if request.form.get('uphill_access', None) == 'paradise':
            uphill_access = 'Open to top of Paradise'
        elif request.form.get('uphill_access', None) == 'peanut':
            uphill_access = 'Open to Peanut'
        else:
            uphill_access = 'Not Open'
        datetime_str = request.form.get('datetime')
        dateTime2 = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        date_converted = dateTime2.date()
        print(date_converted)
        dateCheck = Pm_form.query.filter_by(date=date_converted).first()
        print(dateCheck)
        if not dateCheck:
            hs = float(hs) if hs else None
            hn24 = float(hn24) if hn24 else None
            ytd_snow = float(ytd_snow) if ytd_snow else None
            ytd_swe = float(ytd_swe) if ytd_swe else None
            datetime_str = request.form.get('datetime')
            dateTime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            form= Pm_form(dateTime=dateTime,date=date_converted,forecaster=forecaster,hs=hs,hn24=hn24,ytd_snow=ytd_snow,ytd_swe=ytd_swe,weather_fx=weather_fx,tonight_tomorrow=tonight_tomorrow,do_today=do_today,plan_to_do=plan_to_do,mitigation=mitigation,uphill_access=uphill_access)
            db.session.add(form)
            db.session.commit()
            basic_stats = [hs, hn24, ytd_snow, ytd_swe, uphill_access]
            pdf_filename = generate_pdf_pm(date, forecaster, basic_stats, weather_fx, tonight_tomorrow, do_today,
                                           plan_to_do, mitigation)
            return send_file(pdf_filename, as_attachment=True)
        else:
            return render_template('confirm.html', flash_message=True)


    else:
        now = datetime.now()  #Local
        #now = datetime.now() - timedelta(hours=6) #pythonAnywhere
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        snow = Snow.query.filter_by(date=now.strftime("%Y-%m-%d")).first()
        return render_template('pm-form.html', now=formatted_now, snow=snow)
