from flask import request
from datetime import datetime

def get_time_info():
    datetime_str = request.form.get('datetime')
    dateTime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
    day = int(dateTime.day)
    month = int(dateTime.month)
    year = int(dateTime.year)
    time = dateTime.time()
    date = dateTime.date()
    if dateTime.month < 7:
        season = str(dateTime.year - 1)[2:] + "-" + str(dateTime.year)[2:]  # Example: "24-25"
    else:
        season = str(dateTime.year)[2:] + "-" + str(dateTime.year + 1)[2:]  # Example: "24-25"

    return dateTime, day, month, year, time, date, season

def get_top_of_page_info():
    forecaster = request.form.get('forecaster', None)
    hs = request.form.get('hs', None)
    hn24 = request.form.get('hn24', None)
    hst = request.form.get('hst', None)
    ytd_snow = request.form.get('ytd_snow', None)
    swe = request.form.get('swe', None)
    ytd_swe = request.form.get('ytd_swe', None)
    critical_info = request.form.get('critical_information', None)

    hs = float(hs) if hs else None
    hn24 = float(hn24) if hn24 else None
    hst = float(hst) if hst else None
    ytd_snow = float(ytd_snow) if ytd_snow else None
    ytd_swe = float(ytd_swe) if ytd_swe else None
    swe = float(swe) if swe else None

    return forecaster, hs, hn24, hst, ytd_snow, swe, ytd_swe, critical_info

def get_current_info():
    current_temperature = request.form.get('current_temp', None)
    current_precip_rate = request.form.get('current_precip_rate', None)
    sky = request.form.get('sky', None)
    current_precip_rate = str(current_precip_rate) if current_precip_rate else None
    current_temperature = float(current_temperature) if current_temperature else None
    wind_mph = request.form.get('current_wind_mph', None)
    wind_direction = request.form.get('current_wind_direction', None)
    current_peak_gust_mph = request.form.get('current_peak_gust_mph', None)
    current_peak_gust_mph = float(current_peak_gust_mph) if current_peak_gust_mph else None
    current_peak_gust_direction = request.form.get('current_peak_gust_direction', None)
    current_peak_gust_time_raw = request.form.get('current_peak_gust_time', None)
    if current_peak_gust_time_raw:
        try:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M:%S').time()
        except:
            current_peak_gust_time = datetime.strptime(current_peak_gust_time_raw, '%H:%M').time()
    else:
        current_peak_gust_time = None

    return (current_temperature, current_precip_rate, sky, wind_mph, wind_direction, current_peak_gust_mph,
            current_peak_gust_direction, current_peak_gust_time)

def get_past_info():
    past_24_hn24_hst_date_cir = request.form.get('past_24_hn24_hst_date_cir', None)
    past_24_hst = request.form.get('past_24_hst', None)
    past_24_date_cir = request.form.get('past_24_date_cir', None)
    past_24_settlement = request.form.get('past_24_settlement', None)
    past_24_hn24 = request.form.get('past_24_hn24', None)
    past_24_hn24_swe = request.form.get('past_24_hn24_swe', None)
    past_24_hn24_percent = request.form.get('past_24_hn24_percent', None)
    past_24_wind_mph = request.form.get('past_24_wind_mph', None)
    past_24_wind_direction = request.form.get('past_24_wind_direction', None)
    past_24_temp_high = request.form.get('past_24_temp_high', None)
    past_24_temp_low = request.form.get('past_24_temp_low', None)

    past_24_peak_gust_mph = request.form.get('past_24_peak_gust_mph', None)
    past_24_peak_gust_mph = float(past_24_peak_gust_mph) if past_24_peak_gust_mph else None
    past_24_peak_gust_direction = request.form.get('past_24_peak_gust_direction', None)
    past_24_peak_gust_time_raw = request.form.get('past_24_peak_gust_time', None)
    if past_24_peak_gust_time_raw:
        try:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M:%S').time()
        except:
            past_24_peak_gust_time = datetime.strptime(past_24_peak_gust_time_raw, '%H:%M').time()
    else:
        past_24_peak_gust_time = None

    past_24_settlement = float(past_24_settlement) if past_24_settlement else None
    past_24_hn24_swe = float(past_24_hn24_swe) if past_24_hn24_swe else None
    past_24_hn24 = float(past_24_hn24) if past_24_hn24 else None
    past_24_hn24_percent = float(past_24_hn24_percent) if past_24_hn24_percent else None
    past_24_temp_high = float(past_24_temp_high) if past_24_temp_high else None
    past_24_temp_low = float(past_24_temp_low) if past_24_temp_low else None
    past_24_hst = float(past_24_hst) if past_24_hst else None

    past_24_date_cir_raw = request.form.get('past_24_date_cir', '').strip()
    if past_24_date_cir_raw:
        past_24_date_cir = datetime.strptime(past_24_date_cir, '%Y-%m-%d')
    else:
        past_24_date_cir = None


    
    return (past_24_hn24_hst_date_cir, past_24_hst, past_24_date_cir, past_24_settlement,
            past_24_hn24, past_24_hn24_swe, past_24_hn24_percent, past_24_wind_mph,
            past_24_wind_direction, past_24_temp_high, past_24_temp_low, past_24_peak_gust_mph,
            past_24_peak_gust_direction, past_24_peak_gust_time)

def get_future_info():
    future_precip_rate = request.form.get('future_precip_rate', None)
    future_temp_high = request.form.get('future_temp_high', None)
    future_temp_low = request.form.get('future_temp_low', None)
    future_wind_mph = request.form.get('future_wind_mph', None)
    future_wind_direction = request.form.get('future_wind_direction', None)
    future_peak_gust_mph = request.form.get('future_peak_gust_mph', None)
    future_peak_gust_mph = float(future_peak_gust_mph) if future_peak_gust_mph else None
    future_peak_gust_direction = request.form.get('future_peak_gust_direction', None)
    future_peak_gust_time_raw = request.form.get('future_peak_gust_time', None)
    if future_peak_gust_time_raw:
        try:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M:%S').time()
        except:
            future_peak_gust_time = datetime.strptime(future_peak_gust_time_raw, '%H:%M').time()
    else:
        future_peak_gust_time = None
    # future conversions
    future_precip_rate = str(future_precip_rate) if future_precip_rate else None
    future_temp_high = float(future_temp_high) if future_temp_high else None
    future_temp_low = float(future_temp_low) if future_temp_low else None

    return (future_precip_rate, future_temp_high, future_temp_low, future_wind_mph, future_wind_direction,
            future_peak_gust_mph, future_peak_gust_direction,future_peak_gust_time)

def get_pwl_info():
    pwl = request.form.get('pwl', None)
    pwl_date_raw = request.form.get('pwl_date')
    if pwl_date_raw:
        pwl_date = datetime.strptime(pwl_date_raw, '%Y-%m-%d')
    else:
        pwl_date = None
    return pwl, pwl_date

def get_avalanche_danger():
    avalanche_danger_resort = request.form.get('avalanche_danger_resort', None)
    avalanche_danger_backcountry = request.form.get('avalanche_danger_backcountry', None)
    return avalanche_danger_resort, avalanche_danger_backcountry

def get_avalanche_problem(prob_num):
    avalanche_problem = request.form.get('avalanche_problem_'+str(prob_num), None)
    btl_aspect = request.form.getlist('btl_aspect_'+str(prob_num)+'[]')
    btl_aspect = '-'.join(btl_aspect)
    ntl_aspect = request.form.getlist('ntl_aspect_'+str(prob_num)+'[]')
    ntl_aspect = '-'.join(ntl_aspect)
    atl_aspect = request.form.getlist('atl_aspect_'+str(prob_num)+'[]')
    atl_aspect = '-'.join(atl_aspect)

    size = request.form.get('size_'+str(prob_num), None)
    likelihood = request.form.get('likelihood_'+str(prob_num), None)
    location = request.form.get('location'+str(prob_num), None)
    return avalanche_problem, btl_aspect, ntl_aspect, atl_aspect, size, likelihood, location

def get_textbox_info():
    observation_notes = request.form.get('observation_notes', None)
    weather_forecast = request.form.get('weather_forecast', None)
    avalanche_forecast_discussion = request.form.get('avalanche_forecast_discussion', None)
    summary_previous_day = request.form.get('summary_previous_day', None)
    mitigation_plan = request.form.get('mitigation_plan', None)
    pertinent_terrain_info = request.form.get('pertinent_terrain_info', None)
    return (observation_notes, weather_forecast, avalanche_forecast_discussion,
            summary_previous_day,mitigation_plan,pertinent_terrain_info)
