// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var myBarChart = null
var myBarChartCant = null
$.ajax({
  method: 'GET',
  url: '/api_lerny/lernydetail/?lerny_id=-1&microlerny_id=-1',
  success: function(respuesta) {
    var data_pie = respuesta.approved;
    var data_micro = respuesta.info_micro;
    var name_micro = respuesta.name_micro;
    var cont_micro = respuesta.cont_micro;
    var progress_micro = respuesta.progress_micro;
    var average = respuesta.average_micro;

    var lerny_id = $( "#lerny_select" ).children("option:selected").val();
    var microlerny_id = $( "#microlerny_select" ).children("option:selected").val();

    function filter(){
      table.ajax.url( '/api_lerny/lernydetail/?lerny_id=' + lerny_id +'&microlerny_id=' + microlerny_id).load();
      myBarChartCant.destroy()
      myBarChart.destroy()
      myBarChartProgress.destroy()
      myBarChartAvg.destroy()
      
    }

    console.log("MICRO LERNYS", name_micro)

    var ctx = document.getElementById("myBarChartCant");
    myBarChartCant = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: name_micro,
        datasets: [{
          label: "# Estudiantes",
          data: cont_micro,
          backgroundColor: ['#001844', '#001844', '#001844', '#001844','#001844', '#001844','#001844','#001844', '#001844'],
          hoverBackgroundColor: ['#001844', '#001844','#001844', '#001844','#001844', '#001844','#001844','#001844', '#001844'],
          borderColor: "#4e73df",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: true,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 6
            },
            maxBarThickness: 25,
          }],
          y: {
            beginAtZero: true
          },
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10,
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      },
    });

    var ctx = document.getElementById("myBarChart");
    myBarChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["Aprobado", "No Aprobado"],
        datasets: [{
          label: "Porcentaje",
          data: data_pie,
          backgroundColor: ['#BB86FC', '#001844', ],
          hoverBackgroundColor: ['#BB86FC','#001844'],
          borderColor: "#4e73df",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: true,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 6
            },
            maxBarThickness: 25,
          }],
          y: {
            beginAtZero: true
          },
          yAxes: [{
            ticks: {
              min: 0,
              maxTicksLimit: 5,
              padding: 10,
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      },
    });

    var ctx = document.getElementById("myBarChartProgress");
    myBarChartProgress = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: name_micro,
        datasets: [{
          label: "Progreso",
          data: progress_micro,
          backgroundColor: ['#001844', '#001844', '#001844', '#001844','#001844', '#001844','#001844','#001844', '#001844'],
          hoverBackgroundColor: ['#001844', '#001844','#001844', '#001844','#001844', '#001844','#001844','#001844', '#001844'],
          borderColor: "#4e73df",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: true,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 6
            },
            maxBarThickness: 25,
          }],
          y: {
            beginAtZero: true
          },
          yAxes: [{
            ticks: {
              min:0,

              maxTicksLimit: 5,
              padding: 10,
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      },
    });

    var ctx = document.getElementById("myBarChartAvg");
    myBarChartAvg = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: name_micro,
        datasets: [{
          label: "Promedio",
          data: average,
          backgroundColor: ['#001844', '#001844', '#001844', '#001844','#001844', '#001844', '#001844','#001844', '#001844'],
          hoverBackgroundColor: ['#001844', '#001844','#001844', '#001844','#001844', '#001844','#001844','#001844', '#001844'],
          borderColor: "#4e73df",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: true,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 6
            },
            maxBarThickness: 25,
          }],
          y: {
            beginAtZero: true
          },
          yAxes: [{
            ticks: {
              min: 0,
              maxTicksLimit: 5,
              padding: 10,
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      },
    });
  },
  error: function() {
        console.log("No se ha podido obtener la información");
    }
});