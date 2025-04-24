function graph(x, y, element_id, chart_title, y_label){
    const xValues = x;
    const yValues = y;
//    console.log(xValues)
//    console.log(yValues)
    const y_max = Math.max(...yValues);
    const y_min = Math.min(...yValues);
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
        title: {
          display: true,
          text: chart_title,
          padding: 20,
          fontSize: 18
        },
        legend: {display: false},
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Date",
              fontSize: 14
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: y_label,
              fontSize: 14,
            }
          }]
        }
      }
    });
};



