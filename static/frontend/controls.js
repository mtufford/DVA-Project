var ImageryRoads =  L.layerGroup([L.esri.basemapLayer("Imagery"),L.esri.basemapLayer('ImageryLabels')]).addTo(window.map);

var Streetsbase = L.esri.basemapLayer("Streets")
var baseMaps = {
  	"Imagery and Streets" : ImageryRoads,
    "Streets": Streetsbase,};

var maplayers = L.control.layers(baseMaps).setPosition('topleft').addTo(window.map);


L.easyButton('fa-calendar fa-lg', function(btn){

    if (btn.button.style.backgroundColor == "gray"){
      $("#yearselector").css("visibility", "hidden");
      btn.button.style.backgroundColor = "white";
    }
    else{
      $("#yearselector").css("visibility", "visible");
      btn.button.style.backgroundColor = "gray";
    }


}, "Year Filter").addTo(window.map);

L.easyButton('fa-globe fa-lg', function(btn){

    if (btn.button.style.backgroundColor == "gray"){
      $("#stateselector").css("visibility", "hidden");
      btn.button.style.backgroundColor = "white";
    }
    else{
      $("#stateselector").css("visibility", "visible");
      btn.button.style.backgroundColor = "gray";
    }


}, "State Filter").addTo(window.map);

L.easyButton('fa-bar-chart fa-lg', function(btn){

    if (btn.button.style.backgroundColor == "gray"){
      $("#chartdiv").css("visibility", "hidden");
      btn.button.style.backgroundColor = "white";
    }
    else{
      $("#chartdiv").css("visibility", "visible");
      btn.button.style.backgroundColor = "gray";
      $("#causes-chart").click();
      $("#causes-chart").addClass("active");
    }


}, "Charts").addTo(window.map);

L.easyButton('fa-database fa-lg', function(btn){

    if (btn.button.style.backgroundColor == "gray"){
      $("#modeldiv").css("visibility", "hidden");
      btn.button.style.backgroundColor = "white";
    }
    else{
      $("#modeldiv").css("visibility", "visible");
      btn.button.style.backgroundColor = "gray";
    }


}, "Query Model").addTo(window.map);

$( "#stateselector" ).change(function(e) {
  console.log({"year" : $('#timeslider').val() })
  loadfires({"year" : $('#amount').text(), "state": e.target.value })
});

$(document).ready(function(){
      var date_input=$('input[name="date"]'); //our date input has the name "date"
      var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
      var options={
        format: 'mm-dd-yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
      };
      date_input.datepicker(options);
    })
