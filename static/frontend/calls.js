//Calls to the backend

function queryModel(e){



  query = {latitude : $("#LatitudeEntry").val(),
           longitude : $("#LongitudeEntry").val(),
           date : $("#DateEntry").val(),
           model :  $('#ModelEntry option:selected').val()
  }

  console.log({"query" : query})


  $.loading.start('Loading...')
  $.ajax({
      url: "/api/predict",
      contentType: "application/json; charset=utf-8",
      type: 'POST',
      data: JSON.stringify(query),
      dataType: 'json', // added data type
      success: function(res) {
           //wildfires = JSON.parse(res)




           console.log(res)


           var displayText = Object.keys(res).map((x) => `• ${x}:  ${res[x]}\n`)



            $.loading.end()
            alert(displayText.join(""))




          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
              $.loading.end()
              console.log(XMLHttpRequest.responseText)
              console.log(textStatus)
              console.log(errorThrown)
              alert(XMLHttpRequest.responseText);

          }
      });
}
