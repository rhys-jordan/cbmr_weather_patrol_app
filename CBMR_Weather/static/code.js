function submit_amForm() {
    day = document.getElementById("day").value;
    month = document.getElementById("month").value;
    year = document.getElementById("year").value;
    time = document.getElementById("time").value;
    forecaster = document.getElementById("forecaster").value;
    hs = document.getElementById("hs").value;
    hn24 = document.getElementById("hn24").value;
    hst = document.getElementById("hst").value;
    ytd = document.getElementById("ytd").value;
    critical_information = document.getElementById("critical_information").value;
    sky = document.getElementById("sky").value;
    past_24_hn24_hst_date_cir = document.getElementById("past_24_hn24/hst_date_cir").value;
    future_precip_rate = document.getElementById("future_precip/rate").value;
    current_precip_rate = document.getElementById("current_precip/rate").value;
    past_24_hn24_swe = document.getElementById("past_24_hn24_swe").value;
    future_temp_high = document.getElementById("future_temp_high").value;
    current_temp = document.getElementById("current_temp").value;
    past_24_wind_mph_direction = document.getElementById("past_24_wind_mph/direction").value;
    future_temp_low = document.getElementById("future_temp_low").value;
    current_wind_mph = document.getElementById("current_wind_mph").value;
    past_24_temp_high = document.getElementById("past_24_temp_high").value;
    future_wind_mph = document.getElementById("future_wind_mph").value;
    current_wind_direction = document.getElementById("current_wind_direction").value;
    past_24_temp_low = document.getElementById("past_24_temp_low").value;
    future_wind_direction = document.getElementById("future_wind_direction").value;
    weather_forecast = document.getElementById("weather_forecast").value;

    //need this to dynamically collect more based on the number of values used
    
    avalanche_danger = document.getElementById("avalanche_danger").value;
    avalanche_problem_1 = document.getElementById("avalanche_problem_1").value;
    aspect_elevation = document.getElementById("aspect_elevation").value;
    size_likelihood = document.getElementById("size_likelihood").value;
    trend = document.getElementById("trend").value;

    avalanche_forecast_discussion = document.getElementById("avalanche_forecast_discussion").value;
    summary_of_previous_work = document.getElementById("summary_of_previous_work").value;
    mitigation_plan = document.getElementById("mitigation_plan").value;
    pertinent_terrain_opening_closing = document.getElementById("pertinent_terrain_opening/closing").value;
}


function addProblem2() {

    document.getElementById("problem_2").hidden = false;
    document.getElementById("problem_2_button").hidden = true;
    document.getElementById("problem_3_button").hidden = false;


}


function addProblem3() {

    document.getElementById("problem_3").hidden = false;
    document.getElementById("problem_3_button").hidden = true;


}


function recheck() {
    alert("this date exists please input a valid date or go to the Past-Data Form.")
    window.location.href = "/view";
}

