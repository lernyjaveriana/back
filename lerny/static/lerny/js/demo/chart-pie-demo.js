// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

$.ajax({
  method: 'GET',
  url: '/api_lerny/lernydetail/?lerny_id=-1&microlerny_id=-1',
  success: function(respuesta) {

    var data_pie = respuesta.approved; //Students approved
    var data_micro = respuesta.info_micro; //Array of microlernies
    var name_micro = respuesta.name_micro; //name of microlernies
    var cont_micro = respuesta.cont_micro; //number students of microlernies
    var progress_micro = respuesta.progress_micro; //progress of microlernies
    var average = respuesta.average_micro; //average of microlernies

    console.log(respuesta);
    console.log(lerny_id);
                
    // $( "#lerny_select" ).change(function() {
    //   $( "#lerny_name" ).text($( "#lerny_select" ).children("option:selected").text())
    //   $( "#microlerny_select" ).show()
    //   $('#microlerny_select').children().remove().end()
    //   .append('<option selected value="-1">Todos los Microlerny</option>') ;
    //   var lerny_id = $( "#lerny_select" ).children("option:selected").val();
    //   $.ajax({
    //       method: 'POST',
    //       url: '/api_lerny/microlernyapi/',
    //       data: { pk: lerny_id },
    //       success: function(data) {
    //           for(var i = 0; i < Object.keys(data).length; i++) {
    //               document.getElementById("microlerny_select").innerHTML += "<option value='"+data[i].pk+"'>"+data[i].name+"</option>";
    //           }
    //       },
    //       error: function() {
    //           console.log("No se ha podido obtener la información");
    //       }
    //   });
    // });

    $.ajax({
          url: '/api_lerny/lernyapi/',
          success: function(data) {
              for(var i = 0; i < Object.keys(data).length; i++) {
                  document.getElementById("lerny_select").innerHTML += "<option value='"+data[i].pk+"'>"+data[i].name+"</option>";
              }

              $( "#lerny_name" ).text(data[0].name)
          },
          error: function() {
              console.log("No se ha podido obtener la información");
          }
      });
  
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
              maxTicksLimit: 20
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
      type: 'pie',
      data: {
        labels: ["Aprobado", "No Aprobado"],
        datasets: [{
          label: "Porcentaje",
          data: data_pie,
          backgroundColor: ['#BB86FC', '#001844', ],
          borderColor: "#98E4FB",
          hoverOffset: 4
        }],
      },
    });

    var ctx = document.getElementById("myBarChartProgress");
    myBarChartProgress = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: name_micro,
        datasets: [{
          label: "Progreso",
          data: progress_micro,
          backgroundColor: ['#001844', '#0039A3', '#0047CC ', '#0056F5','#1F6DFF', '#4788FF','#70A2FF'],
          hoverOffset: 4,
          // hoverBackgroundColor: ['#001844', '#00A3EF','#7CDFF', '#BB86FC','#001844', '#001844','#001844','#001844', '#001844'],
          borderColor: "#000000",
        }],
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
              maxTicksLimit: 20
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