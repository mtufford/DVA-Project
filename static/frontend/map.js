window.map = L.map('map')
            .setView([39.8283, -98.5795], 5)
            .on('mousemove',function(e){
              $("#latlong")[0].innerHTML = e.latlng.lat.toFixed(6)+ "N " +e.latlng.lng.toFixed(6)+"E";})
            .on('click',function(e){
              $("#LatitudeEntry").val(e.latlng.lat.toFixed(6))
              $('#LongitudeEntry').val(e.latlng.lng.toFixed(6))

            });
