/*window.colors  = { "Miscellaneous": "#a6cee3",
                 "Missing/Undefined" : "#a6cee3",
                 "Lightning": "#1f78b4",
                 "Debris Burning" :"#b2df8a",
                 "Campfire": "#33a02c",
                 "Equipment Use": "#fb9a99",
                 "Arson" : "#e31a1c",
                 "Children" : "#fdbf6f",
                 "Railroad": "#ff7f00",
                 "Smoking": "#cab2d6",
                 "Powerline" : "#6a3d9a",
                 "Structure" : "#ffff99",
                 "Fireworks" :"#b15928"}*/

window.colors = {"Human Accident" :"#fef0d9",
                  "Arson" : "#fdcc8a",
                  "Infrastructure Accident" : "#fc8d59",
                  "Natural" : "#e34a33",
                  "Other" : "#b30000",
                  }

window.circlelayer = L.layerGroup();




$( function() { $( "#yearselector" ).draggable();});
$( function() { $( "#chartdiv" ).draggable();});
$( function() { $( "#modeldiv" ).draggable();});
$( function() { $( "#pointlegend" ).draggable();});
$( function() { $( "#stateselector" ).draggable();});

$( "#timeslider" ).slider({
        value:2015,
        min: 1992,
        max: 2015,
        step: 1,
        slide: function( event, ui ) {
          $( "#amount" ).text( ui.value );

        },
        stop: function( event, ui) {


          loadfires({"year" : ui.value, "state" : $('#stateselector option:selected').val() })


        }
      });

$( "#amount" ).text( $( "#timeslider" ).slider( "value" ) );

$.loading = {
    start: function (loadingTips='') {
        let _LoadingHtml = '<div class="spin spin-lg spin-spinning">' +
                                '<span class="spin-dot spin-dot-spin">' +
                                    '<i class="spin-dot-item"></i>' +
                                    '<i class="spin-dot-item"></i>' +
                                    '<i class="spin-dot-item"></i>' +
                                    '<i class="spin-dot-item"></i>' +
                                '</span>' +
                                '<span class="tips">'+loadingTips+'</span>'+
                           '</div>'

        $('body').append(_LoadingHtml);
        $('body').css("pointer-events", "none")
    },
    end: function () {
        $(".spin").remove();
        $('body').css("pointer-events", "auto")
    }
}

loadfires({"year" : 2015})
addlegend()
