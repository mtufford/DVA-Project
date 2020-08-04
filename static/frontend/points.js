
var canvasRenderer = L.canvas({ padding: 0.5 });

















function addlegend(){

  const categories = Object.keys(window.colors)

  for (var i in categories){


    var category = categories[i]

      var legenditem = `<svg width="10" height="9">
    <rect width="10" height="9" style="fill:${colors[category]};stroke-width:1;stroke:rgb(0,0,0)" />
  </svg><label class="svglegendlabel"> ${category}</label><br/>`

    $("#pointlegend").append(legenditem)

  }
}

function nukecircles(){
      window.map.removeLayer(window.circlelayer);
      window.circlelayer.clearLayers();
}




function loadfires(query){
//query is a json object with keys "year" and/or "state"
nukecircles()

$.loading.start('Loading...')

$.ajax({
    url: "/api/fires",
    type: 'GET',
    data: query,
    dataType: 'json', // added data type
    success: function(res) {
         //wildfires = JSON.parse(res)
         wildfires = res
         console.log(wildfires)

         for (var i =0; i < wildfires.length; i++){


             const wildfirecause = wildfires[i]["STAT_CAUSE_DESCR"]

             const popupdata =  `<div >
               <ul class="list-group">
                 <li class="list-group-item list-group-item-small" id='wfID'><b>Name: </b>${wildfires[i]["FIRE_NAME"]}</li>
                 <li class="list-group-item list-group-item-small" id='wfCause'><b>Cause: </b>${wildfires[i]["STAT_CAUSE_DESCR"]}</li>
                 <li class="list-group-item list-group-item-small" id='wfSize'><b>Size Class: </b>${wildfires[i]["FIRE_SIZE_CLASS"]}</li>
                 <li class="list-group-item list-group-item-small" id='wfSize'><b>Size: </b>${wildfires[i]["FIRE_SIZE"]}</li>
                 <li class="list-group-item list-group-item-small" id='wfDisDate'><b>Discovery Date: </b>${wildfires[i]["DISCOVERY_DATE"]}</li>
               </ul>
               <center>
               <br/>

               <button class="btn btn-info btn-sm" hidden value = "${wildfires[i]["FOD_ID"]}"href='#' >Action</button></li>

             </div>`







             var circle = L.circle([wildfires[i]["LATITUDE"],wildfires[i]["LONGITUDE"]], {
             color: window.colors[wildfirecause] || 'yellow',
             renderer: canvasRenderer,
             fillColor: window.colors[wildfirecause] || 'yellow',
             fillOpacity: 0.5,
             radius: 500,//wildfires[i]["FIRE_SIZE"]
           }).bindPopup(popupdata).addTo(window.circlelayer);

          }
          window.circlelayer.addTo(window.map);
          $.loading.end()





        }
    });
  }
