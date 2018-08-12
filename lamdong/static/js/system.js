$("#login-btn").click(function() {
  $("#loginModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#signup-btn").click(function() {
  $("#sigupModal").modal("show");
  $(".navbar-collapse.in").collapse("hide");
  return false;
});
$('#login').validator().on('submit', function (e) {
  if (e.isDefaultPrevented()) {
    // handle the invalid form...
  } else {
	e.preventDefault();
	$.ajax({			
            url: '/v1/api/user/login',
            data: $('#login').serialize(),
            type: 'POST',
            success: function(response) {                
				window.location = "./";
				//console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
    });
	$("#loginModal").modal("hide");
  }
})

$('#signup').validator().on('submit', function (e) {
  if (e.isDefaultPrevented()) {
    // handle the invalid form...
  } else {
	e.preventDefault();
	$.ajax({
            url: '/v1/api/user/signup',
            data: $('#signup').serialize(),
            type: 'POST',
            success: function(response) {                
				console.log(response);								
            },
            error: function(error) {
                console.log(error);
            }
    });
	$("#sigupModal").modal("hide");
  }
})