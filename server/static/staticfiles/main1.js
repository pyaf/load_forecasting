$('#dddd').on('click', function() {
  var gap = {
    "fc": $("#fc").val(),
    // to: $("#to").val(),
  };
  console.log("adsfadsfdff");
  console.log(gap);
  console.log(gap.fc);
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
      console.log(x);
      fun1(x);
    },
  });
});

const fun1  = function(data){
        console.log('asdgf',data);
        console.log("ooooooooooooooooooooooooooooooo");
        let load = data;
        console.log(load.forecasted_Load);
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