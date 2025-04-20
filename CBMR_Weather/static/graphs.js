
function graphs(x, y, element_id){
    const graphData = {
      labels: x[0],
      datasets: []
    };

    for(let i = 0; i < x.length; i++){
        const dataset = {
          label: `Dataset ${i + 1}`,
          data: y[i],
          borderColor: `hsl(${i * 120}, 100%, 50%)`,
          fill: false
        };
        graphData.datasets.push(dataset);
    }

    const xValues = x[0];
    const yValues = y[0];
    console.log(xValues)
    console.log(yValues)
    const y_max = Math.max(...yValues)
    const y_min = Math.min(...yValues)

    new Chart(document.getElementById(element_id).getContext('2d'), {
      type: "line",
      data: graphData,
      options: {
        legend: {display: true},
        scales: {
          yAxes: [{ticks: {min:y_min, max:y_max + 10}}]
        }
      }
    });
};

function graphs2(x, y, element_id){
    const xValues = x;
    const yValues = y;
//    console.log(xValues)
//    console.log(yValues)
    const y_max = Math.max(...yValues)
    const y_min = Math.min(...yValues)

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
          text: 'YTD Snow',
          padding: 20,
          fontSize: 18
        },
        legend: {display: false},
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Date',
              fontSize: 14
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'YTD Snow (inches)',
              fontSize: 14
            }
          }]
        }
      }
    });
};


function graphs3(x, y, element_id, chart_title, x_label, y_label){
    const xValues = x;
    const yValues = y;
//    console.log(xValues)
//    console.log(yValues)
    const y_max = Math.max(...yValues)
    const y_min = Math.min(...yValues)

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
              labelString: x_label,
              fontSize: 14
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: y_label,
              fontSize: 14
            }
          }]
        }
      }
    });
};

