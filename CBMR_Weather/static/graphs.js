
function graphs(x, y, element_id){

    const xValues = x;
    const yValues = y;
    const y_max = Math.max(...yValues)

    new Chart(document.getElementById(element_id).getContext('2d'), {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.1)",
          data: yValues
        }]
      },
      options: {
        legend: {display: false},
        scales: {
          yAxes: [{ticks: {min: 20, max:y_max+50}}]
        }
      }
    });
};


//(async function() {
//    const xValues = JSON.parse({{dates|tojson}});
//    const yValues = JSON.parse("{{ytd_snow}}");
//
//    snow_graph = new Chart( document.getElementById("ytd_snow_graph"), {
//      type: "line",
//      data: {
//        labels: xValues,
//        datasets: [{
//          fill: false,
//          lineTension: 0,
//          backgroundColor: "rgba(0,0,255,1.0)",
//          borderColor: "rgba(0,0,255,0.1)",
//          data: yValues
//        }]
//      },
//      options: {
//        legend: {display: false},
//        scales: {
//          yAxes: [{ticks: {min: 20, max:120}}]
//        }
//      }
//    })();

