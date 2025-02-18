
//This is from https://www.w3schools.com/howto/howto_js_sort_table.asp
//Will need to code our own version of this with a pre set up sort for things like sky cover, ->
//wind direction, wind speed since it is a word not a speed

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("snowTable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

//seems to be functioning. Accessing problem info I am unsure if the id names are dynamic..
problem_count=1;
function addProblem() {
            problem_count++;
            const newDiv = document.createElement('div');

            newDiv.innerHTML = `
                <label>Avalanche problem ${problem_count}</label> <input type="text" id="avalanche_problem_${problem_count}">
                <label>Aspect/elevation</label> <input type="text" id="aspect_elevation_${problem_count}">
                <label>Size/likelihood</label> <input type="text" id="size_likelihood_${problem_count}">
                <label>Trend</label> <input type="text" id="trend_${problem_count}">
            `;

            // Append the new div to the form or container
            document.getElementById('problemsContainer').appendChild(newDiv);
}

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
    avalanche_problem_1 = document.getElementById("avalanche_problem_1").value;
    aspect_elevation_1 = document.getElementById("aspect_elevation").value;
    size_likelihood_1 = document.getElementById("size_likelihood").value;
    trend_1 = document.getElementById("trend").value;

    avalanche_forecast_discussion = document.getElementById("avalanche_forecast_discussion").value;
    summary_of_previous_work = document.getElementById("summary_of_previous_work").value;
    mitigation_plan = document.getElementById("mitigation_plan").value;
    pertinent_terrain_opening_closing = document.getElementById("pertinent_terrain_opening/closing").value;
}
