    $("#get_password").click(function(){
     var mail_mobile = $('#mailormobilenumber').val();
     data = JSON.stringify({
     'mail_mobile': mail_mobile,
    });
        $.ajax({
        type: 'POST',
        url: "/auth/forgot_password/",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'SUCCESS') {
                window.location = "/auth/verify_otp/"
                    }
            else{
                alert("User Does not exists")
                console.log("Error")
            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });
});

$("#re_send_otp").click(function(){
$.ajax({
        type: 'GET',
        url: "/auth/re_send_otp/",
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'SUCCESS') {
                window.location = "/auth/verify_otp/"
                    }
            if(response['message'] == 'Message sent is increased for this user'){
                alert("otp sent is increased for this user")
                console.log("message sent error")
            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });
});

$("#change_password").click(function(){
var one_time_password = $('#one_time_password').val();
var new_password = $('#new_password').val();
     data = JSON.stringify({
     'one_time_password': one_time_password,
     'new_password':new_password,
    });
$.ajax({
        type: 'POST',
        url: "/auth/re_send_otp/",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'success') {
                alert("User logged in")
                window.location = "/website/booking/"
                console.log("User logged in")
                    }
            else{
                alert("User Does not exists")
                console.log("Error")
            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });
});

$("#update_password").click(function(){
if($('#user-password-reset').valid()){
var epoch_time = $('#epoch_time').val();
var customer_email = $('#customer_email').val();
var new_password = $('#new_password').val();
     data = JSON.stringify({
     'epoch_time': epoch_time,
     'customer_email': customer_email,
     'new_password': new_password,
    });
$.ajax({
        type: 'POST',
        url: "/auth/set_password/",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'success') {
                $('#my-success-dialog').show();
                setTimeout(function(){
				$('.dialog-overlay').hide();
				window.location = "/website/booking/"
				},5000);

                    }
            else{
                 $('#my-error-dialog').show();
                setTimeout(function(){
				$('.dialog-overlay').hide();
				window.location = "/website/booking/"
				},5000);

            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$("#user-password-reset").validate({
		rules: {
			customer_email:{
                required:true,
             },
             new_password:{
                required:true,
             },

		},
        messages:{
            "customer_email":{
                required:"Please Enter Email Id"
                },
                "new_password":{
                required:"Please Enter New Password"
                },

        },
        errorPlacement: function(error, element) {
              if ( element.is(":radio") ){
                    error.appendTo( element.parent().parent() );
              }
              else if ( element.is(":checkbox") ){
                    error.appendTo ( element.next() );
              }
              else{
                    error.appendTo( element.parent() );
              }
         }
	});

	$('.dialog-confirm-button').click(function(){
	window.location = "/website/booking/";

	});