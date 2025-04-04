from flask import render_template, request, send_file,redirect
from flask_login import login_required
from CBMR_Weather.generate_pdf_am import generate_pdf
from datetime import datetime, timedelta

from CBMR_Weather.routes import bp_am_form
from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow, Avalanche



@bp_am_form.route('/am-form', methods=['GET', 'POST'])
@login_required
def am_form():
    if request.method == 'POST':
        #time functions
        datetime_str = request.form.get('datetime')
        dateTime= datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        day= int(dateTime.day)
        month=int(dateTime.month)
        year=int(dateTime.year)
        time=dateTime.time()
        date = dateTime.date()
        if dateTime.month < 7:
            season = str(dateTime.year - 1)[2:] + "-" + str(dateTime.year)[2:]  # Example: "24-25"
        else:
            season = str(dateTime.year)[2:] + "-" + str(dateTime.year + 1)[2:]  # Example: "24-25"
        #Top of page
        forecaster = request.form.get('forecaster', None)
        hs = request.form.get('hs', None)
        hn24 = request.form.get('hn24', None)
        hst = request.form.get('hst', None)
        ytd_snow = request.form.get('ytd_snow', None)
        swe= request.form.get('swe', None) #this is new!! need to add to database
        ytd_swe=request.form.get('ytd_swe', None) #this is new!! need to add to database
        temperature = request.form.get('current_temp', None)
        current_precip_rate = request.form.get('current_precip_rate', None)
        #past
        past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
        past_24_hst = request.form.get('past_24_hst', None)
        past_24_date_cir = request.form.get('past_24_date_cir', None)
        past_24_settlement = request.form.get('past_24_settlement', None)
        past_24_hn24 = request.form.get('past_24_hn24', None)
        past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
        past_24_hn24_percent= request.form.get('past_24_hn24_percent', None)
        past_24_wind_mph = request.form.get('past_24_wind_mph', None)
        past_24_wind_direction = request.form.get('past_24_wind_direction', None)
        past_24_temp_high = request.form.get('past_24_temp_high', None)
        past_24_temp_low = request.form.get('past_24_temp_low', None)
        #future
        future_precip_rate = request.form.get('future_precip_rate', None)
        future_temp_high = request.form.get('future_temp_high', None)
        future_temp_low = request.form.get('future_temp_low', None)
        future_wind_mph = request.form.get('future_wind_mph', None)
        future_wind_direction = request.form.get('future_wind_direction', None)


        pwl=request.form.get('pwl', None)
        pwl_date_raw = request.form.get('pwl_date')
        if pwl_date_raw:
            pwl_date = datetime.strptime(pwl_date_raw, '%Y-%m-%d')
        else:
            pwl_date = None

        current_peak_gust_mph = request.form.get('current_peak_gust_mph', None)
        current_peak_gust_mph = float(current_peak_gust_mph) if current_peak_gust_mph else None
        current_peak_gust_direction = request.form.get('current_peak_gust_direction', None)
        current_peak_gust_time_raw = request.form.get('current_peak_gust_time', None)
        if current_peak_gust_time_raw:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M').time()
        else:
            current_peak_gust_time = None

        past_24_peak_gust_mph = request.form.get('past_24_peak_gust_mph', None)
        past_24_peak_gust_mph = float(past_24_peak_gust_mph) if past_24_peak_gust_mph else None
        past_24_peak_gust_direction = request.form.get('past_24_peak_gust_direction', None)
        past_24_peak_gust_time_raw = request.form.get('past_24_peak_gust_time', None)
        if past_24_peak_gust_time_raw:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M').time()
        else:
            past_24_peak_gust_time = None

        future_peak_gust_mph = request.form.get('future_peak_gust_mph', None)
        future_peak_gust_mph = float(future_peak_gust_mph) if future_peak_gust_mph else None
        future_peak_gust_direction = request.form.get('future_peak_gust_direction', None)
        future_peak_gust_time_raw = request.form.get('future_peak_gust_time', None)
        if future_peak_gust_time_raw:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M').time()
        else:
            future_peak_gust_time = None

        # formatting to types to match database
        hs = float(hs) if hs else None
        hn24 = float(hn24) if hn24 else None
        hst = float(hst) if hst else None
        ytd_snow = float(ytd_snow) if ytd_snow else None
        ytd_swe = float(ytd_swe) if ytd_swe else None
        swe= float(swe) if swe else None

        #current
        sky = request.form.get('sky', None)
        current_precip_rate = str(current_precip_rate) if current_precip_rate else None
        temperature = float(temperature) if temperature else None
        wind_mph = request.form.get('current_wind_mph', None)
        wind_direction = request.form.get('current_wind_direction', None)
        #past conversions
        past_24_hst = float(past_24_hst) if past_24_hst else None

        past_24_date_cir_raw = request.form.get('past_24_date_cir', '').strip()
        if past_24_date_cir_raw:
            past_24_date_cir = datetime.strptime(past_24_date_cir, '%Y-%m-%d')
        else:
            past_24_date_cir = None
        past_24_settlement = float(past_24_settlement) if past_24_settlement else None
        past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
        past_24_hn24 = float(past_24_hn24) if past_24_hn24 else None
        past_24_hn24_percent = float(past_24_hn24_percent) if past_24_hn24_percent else None
        past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
        past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
        #future conversions
        future_precip_rate = str(future_precip_rate) if future_precip_rate else None
        future_temp_high = float(future_temp_high) if future_temp_high else None
        future_temp_low = float(future_temp_low) if future_temp_low else None
        #avalanche conversions

        avalanche_danger_resort = request.form.get('avalanche_danger_resort', None)
        avalanche_danger_backcountry = request.form.get('avalanche_danger_backcountry', None)
        # problem 1
        avalanche_problem_1 = request.form.get('avalanche_problem_1', None)
        btl_aspect_1 = request.form.getlist('btl_aspect_1[]')
        btl_aspect_1 = '-'.join(btl_aspect_1)
        ntl_aspect_1 = request.form.getlist('ntl_aspect_1[]')
        ntl_aspect_1 = '-'.join(ntl_aspect_1)
        atl_aspect_1 = request.form.getlist('atl_aspect_1[]')
        atl_aspect_1 = '-'.join(atl_aspect_1)

        size_1 = request.form.get('size_1', None)
        likelihood_1 = request.form.get('likelihood_1', None)
        location1=request.form.get('location1', None)
        # problem 2
        avalanche_problem_2 = request.form.get('avalanche_problem_2', None)
        btl_aspect_2 = request.form.getlist('btl_aspect_2[]')
        btl_aspect_2 = '-'.join(btl_aspect_2)
        ntl_aspect_2 = request.form.getlist('ntl_aspect_2[]')
        ntl_aspect_2 = '-'.join(ntl_aspect_2)
        atl_aspect_2 = request.form.getlist('atl_aspect_2[]')
        atl_aspect_2 = '-'.join(atl_aspect_2)
        size_2 = request.form.get('size_2', None)
        likelihood_2 = request.form.get('likelihood_2', None)
        location2 = request.form.get('location2', None)
        #problem 3
        avalanche_problem_3 = request.form.get('avalanche_problem_3', None)
        btl_aspect_3 = request.form.getlist('btl_aspect_3[]')
        btl_aspect_3 = '-'.join(btl_aspect_3)
        ntl_aspect_3 = request.form.getlist('ntl_aspect_3[]')
        ntl_aspect_3 = '-'.join(ntl_aspect_3)
        atl_aspect_3 = request.form.getlist('atl_aspect_3[]')
        atl_aspect_3 = '-'.join(atl_aspect_3)
        size_3 = request.form.get('size_3', None)
        likelihood_3 = request.form.get('likelihood_3', None)
        location3 = request.form.get('location3', None)
        # problem 4
        avalanche_problem_4 = request.form.get('avalanche_problem_4', None)
        btl_aspect_4 = request.form.getlist('btl_aspect_4[]')
        btl_aspect_4 = '-'.join(btl_aspect_4)
        ntl_aspect_4 = request.form.getlist('ntl_aspect_4[]')
        ntl_aspect_4 = '-'.join(ntl_aspect_4)
        atl_aspect_4 = request.form.getlist('atl_aspect_4[]')
        atl_aspect_4 = '-'.join(atl_aspect_4)
        size_4 = request.form.get('size_4', None)
        likelihood_4 = request.form.get('likelihood_4', None)
        location4 = request.form.get('location4', None)

        #text box conversions
        observation_notes=request.form.get('observation_notes', None) #this is new!! need to add to database
        critical_info = request.form.get('critical_information', None)
        weather_forecast = request.form.get('weather_forecast', None)
        avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
        summary_previous_day = request.form.get('summary_previous_day', None)
        mitigation_plan = request.form.get('mitigation_plan', None)
        pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if not dateCheck:
            print(avalanche_problem_1, avalanche_problem_2, avalanche_problem_3, avalanche_problem_4)
            snow = Snow(dateTime=dateTime,date=date, day=day, month=month, year=year, time=time, season=season, forecaster=forecaster, hs=hs, hn24=hn24,swe=swe, hst=hst, ytd_snow=ytd_snow, ytd_swe=ytd_swe, sky=sky, temperature=temperature, wind_mph=wind_mph, wind_direction=wind_direction, observation_notes=observation_notes, critical_info=critical_info, weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion, summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan, pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate, past_24_hst=past_24_hst, past_24_settlement=past_24_settlement,past_24_date_cir=past_24_date_cir, future_precip_rate=future_precip_rate, past_24_hn24_swe=past_24_hn24_swe, past_24_hn24=past_24_hn24, past_24_hn24_percent=past_24_hn24_percent, future_temp_high=future_temp_high, past_24_wind_mph=past_24_wind_mph, past_24_wind_direction=past_24_wind_direction, future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high, future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low, future_wind_direction=future_wind_direction, avalanche_danger_resort=avalanche_danger_resort, avalanche_danger_backcountry=avalanche_danger_backcountry,pwl=pwl,pwl_date=pwl_date,current_peak_gust_mph=current_peak_gust_mph,current_peak_gust_direction=current_peak_gust_direction,current_peak_gust_time=current_peak_gust_time,past_24_peak_gust_mph=past_24_peak_gust_mph,past_24_peak_gust_direction=past_24_peak_gust_direction,past_24_peak_gust_time=past_24_peak_gust_time,future_peak_gust_mph=future_peak_gust_mph,future_peak_gust_direction=future_peak_gust_direction,future_peak_gust_time=future_peak_gust_time)
            db.session.add(snow)

            id = Snow.query.filter_by(date=date).first().id

            if avalanche_problem_1:
                avy1 = Avalanche(problem=avalanche_problem_1, size = size_1, likelihood = likelihood_1, btl_aspect=btl_aspect_1,ntl_aspect=ntl_aspect_1,atl_aspect=atl_aspect_1, location=location1, Snow_id=id)
                db.session.add(avy1)
            if avalanche_problem_2:
                avy2 = Avalanche(problem=avalanche_problem_2, size = size_2, likelihood = likelihood_2, btl_aspect=btl_aspect_2,ntl_aspect=ntl_aspect_2,atl_aspect=atl_aspect_2, location=location2, Snow_id=id)
                db.session.add(avy2)
            if avalanche_problem_3:
                avy3 = Avalanche(problem=avalanche_problem_3, size = size_3,  likelihood= likelihood_3, btl_aspect=btl_aspect_3,ntl_aspect=ntl_aspect_3,atl_aspect=atl_aspect_3,  location=location3, Snow_id=id)
                db.session.add(avy3)
            if avalanche_problem_4:
                avy4 = Avalanche(problem=avalanche_problem_4, size = size_4,  likelihood= likelihood_4, btl_aspect=btl_aspect_4,ntl_aspect=ntl_aspect_4,atl_aspect=atl_aspect_4,  location=location4, Snow_id=id)
                db.session.add(avy4)

            db.session.commit()
            pdf_filename = generate_pdf(date)
            #return redirect('/view')
            return send_file(pdf_filename, as_attachment=True) #
        else:
            return render_template('confirm.html', flash_message=True)
    else:
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M")
        day_before = now - timedelta(days=1)
        dateBefore = day_before.strftime("%Y-%m-%d")
        snow = Snow.query.filter_by(date=dateBefore).first()
        if snow:
            if snow.ytd_snow == None:
                snow.ytd_snow=0
            if snow.ytd_swe == None:
                snow.ytd_swe=0
            return render_template('am-form.html', now=formatted_now, ytd_snowPre=snow.ytd_snow,ytd_swePre=snow.ytd_swe,critical_info=snow.critical_info,observation_notes=snow.observation_notes,weather_forecast=snow.weather_forecast,avalanche_forecast_discussion=snow.avalanche_forecast_discussion,summary_previous_day=snow.summary_previous_day,mitigation_plan=snow.mitigation_plan,pertinent_terrain_info=snow.pertinent_terrain_info)
        else:
            return render_template('am-form.html', now=formatted_now, ytd_snowPre=0,ytd_swePre=0, critical_info="",observation_notes="",weather_forecast="",avalanche_forecast_discussion="",summary_previous_day="",mitigation_plan="",pertinent_terrain_info="")
