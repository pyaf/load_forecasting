$('#dddd').on('click', function() {
  var gap = {
    "fc": $("#fc").val(),
    // to: $("#to").val(),
  };
  // console.log("adsfadsfdff");
  // console.log(gap);
  // console.log(gap.fc);
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
  $.ajax({
    type: 'POST',
    url: '/show_forecasted_smavg_data/',
    data: gap,
    success: function(x){
      // console.log(x);
      console.log(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,");
      fun1(x);
    },
  });
});

const fun1  = function(data){
        // console.log('asdgf',data);
        // console.log("ooooooooooooooooooooooooooooooo");
        let load = data;
        console.log("zzzzzzzzzzzzzzz",load.rmseSMA);
        console.log(load.forecasted_Load);
        var a1 = document.getElementById('sma1');
        a1.innerHTML = load.rmseSMA;
        var b1 = document.getElementById('wma1');
        b1.innerHTML = load.rmseWMA;
        var c1 = document.getElementById('ses1');
        c1.innerHTML = load.rmseSES;
        var d1 = document.getElementById('arima1');
        d1.innerHTML = load.rmseARIMA;
        var e1 = document.getElementById('lstm1');
        e1.innerHTML = load.rmseLSTM;
        var f1 = document.getElementById('gru1');
        f1.innerHTML = load.rmseGRU;
        var g1 = document.getElementById('rnn1');
        g1.innerHTML = load.rmseRNN;

        var a1M = document.getElementById('sma1M');
        a1M.innerHTML = load.mapeSMA;
        var b1M = document.getElementById('wma1M');
        b1M.innerHTML = load.mapeWMA;
        var c1M = document.getElementById('ses1M');
        c1M.innerHTML = load.mapeSES;
        var d1M = document.getElementById('arima1M');
        d1M.innerHTML = load.mapeARIMA;
        var e1M = document.getElementById('lstm1M');
        e1M.innerHTML = load.mapeLSTM;
        var f1M = document.getElementById('gru1M');
        f1M.innerHTML = load.mapeGRU;
        var g1M = document.getElementById('rnn1M');
        g1M.innerHTML = load.mapeRNN;
        //   let datee = (parseInt(tarikh[8]+tarikh[9]) + i).toString() + '-' + tarikh[5]+tarikh[6] +'-'+tarikh[0]+tarikh[1]+tarikh[2]+tarikh[3];
        var chart = c3.generate({
          bindto: '#Forecasting',
          data: {
            x: 'x',
            xFormat:'%H:%M',
            columns: load.forecasted_Load,
          },
          axis: {
            y: {
              label:{
                text:'POWER IN MW',
                position: 'outer-middle',
              },
            },
            x: {
              label:{
                text: 'Time',
                position:'outer-right',
              },
              type: 'timeseries',
              tick:{
                format:'%H:%M'
              }
            }
          },
          point: {
            show: false
          },
          // zoom: {
          //   enabled:true,
          //   rescale:true,
          //   extent: [1, 100],
          // },
          grid: {
            x: {
              show: true,
            },
            y: {
              show: true,
            },
          },
      });
    };

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// $(document).ready(function(){
//     $('#kp').on('click', function(){
//         console.log("ooooooooooooooooooooooooooooooo");
//         let load = data;
//         //   let datee = (parseInt(tarikh[8]+tarikh[9]) + i).toString() + '-' + tarikh[5]+tarikh[6] +'-'+tarikh[0]+tarikh[1]+tarikh[2]+tarikh[3];
//         var chart = c3.generate({
//           bindto: '#d',
//           data: {
//             x: 'x',
//             xFormat:'%H:%M',
//             columns: load.Load,
//           },
//           axis: {
//             y: {
//               label:{
//                 text:'POWER IN MW',
//                 position: 'outer-middle',
//               },
//             },
//             x: {
//               label:{
//                 text: 'Time',
//                 position:'outer-center',
//               },
//               type: 'timeseries',
//               tick:{
//                 format:'%H:%M'
//               }
//             }
//           },
//           zoom: {
//             enabled:true,
//             rescale:true,
//             extent: [1, 100],
//           },
//           grid: {
//             x: {
//               show: true,
//             },
//             y: {
//               show: true,
//             },
//           },
//       });
//     });
//  });