$("#report-btn").click(function() {
  $("#reportModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});
$("#get-location-btn").click(function() {
	locateControl.start();
	if (navigator.geolocation) {       
		navigator.geolocation.getCurrentPosition(showPosition);		
    } else {
        //x.innerHTML = "Geolocation is not supported by this browser.";
    }					
});

function showPosition(position) {
	document.getElementById('reportLat').value = position.coords.latitude; 	
	document.getElementById('reporLng').value = position.coords.longitude;		    
}

$('#report').validator().on('submit', function (e) {
  if (e.isDefaultPrevented()) {
    // handle the invalid form...
  } else {
	e.preventDefault();
	var form_data = new FormData($('#report')[0]);
	$.ajax({			
            url: '/api/v1/reports',
            //data: $('#report').serialize(),
			data: form_data,
            type: 'POST',
			contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(response) {                
				//window.location = "./";
				//console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
    });
	$("#reportModal").modal("hide");
  }
})