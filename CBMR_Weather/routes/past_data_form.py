from flask import render_template, request, send_file,redirect
from flask_login import login_required
from CBMR_Weather.generate_pdf_am import generate_pdf
from datetime import datetime, timedelta

from CBMR_Weather.routes import bp_past_form
from CBMR_Weather.extensions import db
from CBMR_Weather.models import Snow, Avalanche
from CBMR_Weather.forms_info import (get_time_info, get_top_of_page_info, get_past_info,
                                     get_future_info, get_current_info, get_pwl_info,
                                     get_avalanche_danger, get_avalanche_problem, get_textbox_info)


@bp_past_form.route('/past-data', methods=['GET', 'POST'])
@login_required
def past_data():
    if request.method == 'POST':
        # time functions
        dateTime, day, month, year, time, date, season = get_time_info()

        # Top of page
        forecaster, hs, hn24, hst, ytd_snow, swe, ytd_swe, critical_info = get_top_of_page_info()

        # current
        (current_temperature, current_precip_rate, sky, wind_mph, wind_direction, current_peak_gust_mph,
         current_peak_gust_direction, current_peak_gust_time) = get_current_info()

        # past
        (past_24_hn24_hst_date_cir, past_24_hst, past_24_date_cir, past_24_settlement,
         past_24_hn24, past_24_hn24_swe, past_24_hn24_percent, past_24_wind_mph,
         past_24_wind_direction, past_24_temp_high, past_24_temp_low, past_24_peak_gust_mph,
         past_24_peak_gust_direction, past_24_peak_gust_time) = get_past_info()

        # future
        (future_precip_rate, future_temp_high, future_temp_low, future_wind_mph, future_wind_direction,
         future_peak_gust_mph, future_peak_gust_direction, future_peak_gust_time) = get_future_info()

        # pwl
        pwl, pwl_date = get_pwl_info()

        # avalanche danger
        avalanche_danger_resort, avalanche_danger_backcountry = get_avalanche_danger()

        # Avalanche Problems
        avalanche_problem_1, btl_aspect_1, ntl_aspect_1, atl_aspect_1, size_1, likelihood_1, location_1 = get_avalanche_problem(
            1)
        avalanche_problem_2, btl_aspect_2, ntl_aspect_2, atl_aspect_2, size_2, likelihood_2, location_2 = get_avalanche_problem(
            2)
        avalanche_problem_3, btl_aspect_3, ntl_aspect_3, atl_aspect_3, size_3, likelihood_3, location_3 = get_avalanche_problem(
            3)
        avalanche_problem_4, btl_aspect_4, ntl_aspect_4, atl_aspect_4, size_4, likelihood_4, location_4 = get_avalanche_problem(
            4)

        # text box conversions
        (observation_notes, weather_forecast, avalanche_forecast_discussion,
         summary_previous_day, mitigation_plan, pertinent_terrain_info) = get_textbox_info()

        #checking if data input has already happened
        dateCheck = Snow.query.filter_by(date=date).first()
        if not dateCheck:
            print(avalanche_problem_1, avalanche_problem_2, avalanche_problem_3, avalanche_problem_4)
            snow = Snow(dateTime=dateTime, date=date, day=day, month=month, year=year, time=time, season=season,
                        forecaster=forecaster, hs=hs, hn24=hn24, swe=swe, hst=hst, ytd_snow=ytd_snow, ytd_swe=ytd_swe,
                        sky=sky, temperature=current_temperature, wind_mph=wind_mph, wind_direction=wind_direction,
                        observation_notes=observation_notes, critical_info=critical_info,
                        weather_forecast=weather_forecast, avalanche_forecast_discussion=avalanche_forecast_discussion,
                        summary_previous_day=summary_previous_day, mitigation_plan=mitigation_plan,
                        pertinent_terrain_info=pertinent_terrain_info, current_precip_rate=current_precip_rate,
                        past_24_hst=past_24_hst, past_24_settlement=past_24_settlement,
                        past_24_date_cir=past_24_date_cir, future_precip_rate=future_precip_rate,
                        past_24_hn24_swe=past_24_hn24_swe, past_24_hn24=past_24_hn24,
                        past_24_hn24_percent=past_24_hn24_percent, future_temp_high=future_temp_high,
                        past_24_wind_mph=past_24_wind_mph, past_24_wind_direction=past_24_wind_direction,
                        future_temp_low=future_temp_low, past_24_temp_high=past_24_temp_high,
                        future_wind_mph=future_wind_mph, past_24_temp_low=past_24_temp_low,
                        future_wind_direction=future_wind_direction, avalanche_danger_resort=avalanche_danger_resort,
                        avalanche_danger_backcountry=avalanche_danger_backcountry,pwl=pwl,pwl_date=pwl_date,
                        current_peak_gust_mph=current_peak_gust_mph,current_peak_gust_direction=current_peak_gust_direction,
                        current_peak_gust_time=current_peak_gust_time,past_24_peak_gust_mph=past_24_peak_gust_mph,
                        past_24_peak_gust_direction=past_24_peak_gust_direction,past_24_peak_gust_time=past_24_peak_gust_time,
                        future_peak_gust_mph=future_peak_gust_mph,future_peak_gust_direction=future_peak_gust_direction,
                        future_peak_gust_time=future_peak_gust_time)
            db.session.add(snow)

            id = Snow.query.filter_by(date=date).first().id
            print(id)

            if avalanche_problem_1:
                avy1 = Avalanche(problem=avalanche_problem_1, size=size_1, likelihood=likelihood_1,
                                 btl_aspect=btl_aspect_1, ntl_aspect=ntl_aspect_1, atl_aspect=atl_aspect_1,
                                 location=location_1, Snow_id=id)
                db.session.add(avy1)
            if avalanche_problem_2:
                avy2 = Avalanche(problem=avalanche_problem_2, size=size_2, likelihood=likelihood_2,
                                 btl_aspect=btl_aspect_2, ntl_aspect=ntl_aspect_2, atl_aspect=atl_aspect_2,
                                 location=location_2, Snow_id=id)
                db.session.add(avy2)
            if avalanche_problem_3:
                avy3 = Avalanche(problem=avalanche_problem_3, size=size_3, likelihood=likelihood_3,
                                 btl_aspect=btl_aspect_3, ntl_aspect=ntl_aspect_3, atl_aspect=atl_aspect_3,
                                 location=location_3, Snow_id=id)
                db.session.add(avy3)
            if avalanche_problem_4:
                avy4 = Avalanche(problem=avalanche_problem_4, size=size_4, likelihood=likelihood_4,
                                 btl_aspect=btl_aspect_4, ntl_aspect=ntl_aspect_4, atl_aspect=atl_aspect_4,
                                 location=location_4, Snow_id=id)
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
        return render_template('past-data.html')