$('.open-signIn-link').magnificPopup({
    type: 'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});
$('.open-signUp-link').magnificPopup({
    type: 'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});

var redirectUrlAfterLogin = "home"

function onSignInCallback(resp) {
    //gapi.client.setApiKey('AIzaSyCkvbu3q3Kh9iE2BziV0TBYNqonOKX3ohM');
    gapi.client.load('plus', 'v1', apiClientLoaded);
}

function apiClientLoaded() {
    gapi.client.plus.people.get({
        userId: 'me'
    }).execute(handleEmailResponse);
}

function handleEmailResponse(resp) {
    var primaryEmail, name, etag, social_id;
    console.log(resp);
    if (resp.code == 403) {
        console.log("test2");
//        render();
        //                        $.ajax({
        //                              type: "GET",
        //                              url: "https://www.googleapis.com/plus/v1/people/me",
        //                              headers: {
        //                               "Authorization":"Bearer " + 'AIzaSyBvz_Cw9N6FMF4FsfCVt7z1YsheWMLYWHo',
        //                              }
        //                            });
//        render();
        /*$.ajax({
                 type: "GET",
                 url: "https://www.googleapis.com/plus/v1/people/me",
                 headers: {
                  "Authorization":"Bearer " + 'AIzaSyCDTk6_qhw14F2qlbG-_eWC5bbAhnCBX7E',
                 }
               });*/
        return false;
    }
    for (var i = 0; i < resp.emails.length; i++) {
        if (resp.emails[i].type === 'account') primaryEmail = resp.emails[i].value;
    }
    //document.getElementById('responseContainer').value = 'Primary email: ' +
    //    primaryEmail + '\n\nFull Response:\n' + JSON.stringify(resp);
    name = resp.displayName
    etag = resp.etag
    social_id = resp.id
    var data = {
        "email": primaryEmail,
        "name": name,
        "etag": etag,
        "social_id": social_id
    }
    $.ajax({
        url: "/auth/login_google/",
        type: "POST",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(resp) {
            msg = JSON.parse(resp)
            if (msg['status'] == "failed") {
                console.log('failed')
            }
            if (msg['status'] == "done") {

                if (redirectUrlAfterLogin == "processBooking") {
                    $submitBooking($("#bookingForm"))
                } else if (redirectUrlAfterLogin == "home") {
                    $(".mfp-close").click();
                    $('#login-status').load(location.href + ' #login-status');
                }
                console.log('success');
            }
        }
    });

}


//        function handleEmailResponse(resp) {
//        alert('handleEmailResponse');
//    var primaryEmail;
//    for (var i=0; i < resp.emails.length; i++) {
//      if (resp.emails[i].type === 'account') primaryEmail = resp.emails[i].value;
//      if (resp.emails.length == 1)
//      {
//        //first_name = resp.name.givenName;
//        //last_name = resp.name.familyName;
//        first_name = resp.displayName;
//        pic = resp.image.url;
//        //var data = 'email='+primaryEmail+'&first_name='+first_name+'&last_name='+last_name+'&password=qwerty'
//        var data = 'email='+primaryEmail+'&first_name='+first_name+'&pic='+pic+'&password=qwerty'
//        console.log(resp);
//
//
//        }
//      else
//      {
//      }
//    }
//  }

function render() {
        var ab=gapi.auth.authorize({ client_id: "463240297719-n8706442563rq904gioajptujaq4h346.apps.googleusercontent.com", scope: 'email', immediate: false, include_granted_scopes: false }, onSignInCallback);
}

function render_signup() {
    gapi.signin.render('social_buttons_google_signup', {
        'callback': 'onSignInCallback',
        //				      'clientid': '284988950964-apssq2cr5dj96mfr51soudedfr68sffd.apps.googleusercontent.com',
        'clientid': '284988950964-apssq2cr5dj96mfr51soudedfr68sffd.apps.googleusercontent.com',
        'cookiepolicy': 'single_host_origin',
        'scope': 'email'
    });
}



/*$(document).ready(function(){
    $(document).on("submit","form",function(e){
        if($(this).prop("name") == 'loginForm'){
            e.preventDefault()
            $loginUser($(this))
        }
        if($(this).prop("name") == 'registerForm'){
            e.preventDefault()
            $newUser($(this))
        }
        if($(this).prop("name") == 'booking_form'){
            e.preventDefault()
//            TODO: validate form

            if (isLoggedIn == "Loggedin"){
                $submitBooking($(this))
            }
            else if(isLoggedIn == "NotLoggedin"){

                 $saveBooking($(this))
                 redirectUrlAfterLogin = "processBooking";
                 loginPopUp();
            }

        }
    })




});*/
//function render(){
// alert('hi');
//gapi.signin.render('social_buttons_google_signin',{
//'data-scope':"email",
//          'data-clientid':"284988950964-apssq2cr5dj96mfr51soudedfr68sffd.apps.googleusercontent.com",
//          'data-callback':"onSignInCallback",
//          'data-theme':"dark",
//          'data-cookiepolicy':"single_host_origin"
//});
//}
/* $("#social_buttons_google_signin").on('click',function(){
         render();
  });*/

$("#social_buttons_google_signup").on('click', function() {
    render_signup();
});

$loginUser = function(form) {
    $.ajax({
        url: "/auth/login/",
        type: "POST",
        cache: false,
        data: form.serialize(),
        error: function() {
            alert('<p> An error has occured</p>');
        },
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(resp) {
            msg = JSON.parse(resp)
            if (msg['status'] == "failed") {
                console.log('failed');
                $('.errorMessage').show();
                $('.errorMessageText').html("user name or password is incorrect");
            }
            if (msg['status'] == "done") {

                if (redirectUrlAfterLogin == "processBooking") {
                    $submitBooking($("#bookingForm"))
                } else if (redirectUrlAfterLogin == "home") {
                    $(".mfp-close").click();
                    $('#login-status').load(location.href + ' #login-status');
                }
                console.log('success');
            }
        }
    });
}

$newUser = function(form) {
    $.ajax({
        url: "/auth/signup/",
        type: "POST",
        data: form.serialize(),
        success: function(resp) {
            msg = JSON.parse(resp)
            if (msg['status'] == "failed") {
                console.log('failed')
            }
            if (msg['status'] == "done") {
                if (redirectUrlAfterLogin == "processBooking") {
                    $submitBooking($("#bookingForm"))
                } else if (redirectUrlAfterLogin == "home") {
                    $(".mfp-close").click();
                    $('#login-status').load(location.href + ' #login-status');
                }
                console.log('success');
            }
            if (msg.status != "done") {
                console.log(msg.status.toString());
                $("#errorMsgDiv").show();
                $("#errorMsgDivText").text(msg.status.toString());
                $("#errorMsgDivText").addClass("error-message-style");
            }
        }
    });
}

$guestUser = function(form) {
    $.ajax({
        url: "/auth/guestUser/",
        type: "POST",
        data: form.serialize(),
        success: function(response) {
            response = JSON.parse(response)
            if (response['message'] == 'success') {
                window.location = "/website/booking/"
                console.log('user logged in successfully');
            }
            if (response['status'] != 'success') {
                console.log(response.status.toString());
                $("#errorMsgDiv").show();
                $("#errorMsgDivText").text(response.status.toString());
                $("#errorMsgDivText").addClass("error-message-style");
            }
        }
    });
    }


function logoutUser() {
    $.ajax({
        url: "/auth/logout/",
        type: "GET",
        data: {},
        success: function(resp) {
            msg = JSON.parse(resp)
            if (msg['status'] == "failed") {
                console.log('failed')
            }
            if (msg['status'] == "done") {
                ///                $("#login-status").load(location.href + "#login-status");
                window.location.href = "/"
                console.log('success');
            }
        }
    });
    return false;
}
$forgotPassword = function(form) {
    $.ajax({
        url: "/auth/forgot_password/",
        type: "POST",
        data: form.serialize(),
        success: function(response) {
            response = JSON.parse(response)
                if (response['status'] == 'success') {
               $.ajax({
                    url: "/auth/verify_otp/",
                    type: "GET",
                    data: form.serialize(),
                    success: function(response) {
                        response = JSON.parse(response)
                if (response['status'] == 'success') {
                    if(response['customer_registered_mobile_number'].length>0) {
                    $('.errorMessage').show();
                    $('#errorMsgDivText').html("Forgot password link has been sent to your registered Email and OTP is sent to your Registered Mobile");
                    $('#forgot_password_otp_form').show();
                    $('#forgot_password_form').hide();
                    $('#guest_form').hide();
                    $('#signup_form').hide();
                    $('#login_form').hide();
                    $.ajax({
                        url: "/auth/send_mail/",
                        type: "POST",
                    });
                    }else{
                        $('.errorMessage').show();
                        $('#errorMsgDivText').html("Forgot password link has been sent to your registered Email Id");
                        $('#forgot_password_form').hide();
                        $('#guest_form').hide();
                        $('#signup_form').hide();
                        $('#login_form').hide();
                        $('.modal-body-right').hide();
                        $('#center-line').hide();
                        $('.modal-register-btn').hide();
                        $.ajax({
                            url: "/auth/send_mail/",
                            type: "POST",
                        });
                    }
                    }
                    },
                    });
            }else{
                $('.errorMessage').show();
                $('#errorMsgDivText').html("This email id does not exists, give a valid email id");
                console.log("Error")
            }
            },
    });
}
$submitBooking = function(form) {
    formData = form.serializeArray();

    //fixing csrf-token issue
    for (var key in formData) {
        if (formData.hasOwnProperty(key)) {
            var obj = formData[key];
            if (obj.hasOwnProperty('name') && obj['name'] == "csrfmiddlewaretoken") {
                obj["value"] = getCookie('csrftoken');
            }

        }
    }

    $.ajax({
        url: "/website/booking/",
        type: "POST",
        data: formData,
        success: function(resp) {
            debugger;
            msg = JSON.parse(resp)
            if (msg['status'] == "failed") {
                console.log('failed')
            } else if (msg['status'] == "done") {
                window.location.href = "/website/confirmorder/"
            }
        }
    })
}

$saveBooking = function(form, source) {
    var vehicle_type = $("input[type='radio'].myvehicle:checked").val();
    var brand = $('#make').val();
    var service_center_address = $('#location').val();
    var specificProblems = $('#specificProblems').val();
    var selected_generic_problems = get_generic_problem()
    var pickup_time = $('#datetimepicker12').val();
    //var source = "book";
    data = JSON.stringify({
        'vehicle_type': vehicle_type,
        'brand': brand,
        'service_center_address': service_center_address,
        'specificProblems': specificProblems,
        'source': source,
        'pickup_time': pickup_time,
        'selected_generic_problems': selected_generic_problems,
    });

    $.ajax({
        type: 'POST',
        url: "/website/savebooking/",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("XCSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'SUCCESS') {

            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });

}

function get_generic_problem() {
    var generic_problem_length = $('#generic_problem_length').val();
    var generic_problems = [];
    if (vehicle_type == "Select Vehicle Type") {
        return generic_problems;
    } else {
        for (var i = 0; i < generic_problem_length; i++) {
            if ($('#' + i).hasClass('service-my-wheels-vitals-active')) {
                var selected_generic_problems = $('#' + i).children().text();
                if (selected_generic_problems.length > 0) {
                    generic_problems.push(selected_generic_problems);
                }
            }
        }
    }
    return generic_problems
}

var facebookAccessToken = '';

function login() {
    FB.login(function(response) {
        console.log(response);
        if (response.authResponse) {
            facebookAccessToken = response.authResponse.accessToken;
            testAPI();
        } else {
            // cancelled
        }
    }, {
        scope: 'email,publish_actions'
    });
}
window.fbAsyncInit = function() {
    FB.init({
        //appId : '317889798256950',
        appId: '539855112833964',
        status: true, // check login status
        cookie: true, // enable cookies to allow the server to access the session
        xfbml: true // parse XFBML
    });
    FB.Event.subscribe('auth.authResponseChange', function(response) {
        // Here we specify what we do with the response anytime this event occurs.
        if (response.status === 'connected') {

        } else if (response.status === 'not_authorized') {
            FB.login();
        } else {
            FB.login();
        }
    });
};

// Load the SDK asynchronously
(function(d) {
    var js, id = 'facebook-jssdk',
        ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement('script');
    js.id = id;
    js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));

function testAPI() {
    FB.api('/me?fields=first_name,last_name,email,gender', function(response) {
        console.log(response);
        var facebookEmail = response.email;
        var firstName = response.first_name;
        var lastName = response.last_name;
        var fullName = firstName + " " + lastName;
        var gender = response.gender;
        var social_id = "facebook" + response.id;
        if (facebookEmail != "") {
            $("#facebook_email_id").val(facebookEmail);
            $("#first_name").val(firstName);
            $("#last_name").val(lastName);
            $("#gender").val(gender);
            $("#facebook_login_id").val("facebook" + response.id);
            $("#social_login_type").val("facebook");
            var profileImgUrl = "https://graph.facebook.com/" + response.id + "/picture?type=large";
            $("#social_login_profile_img_url").val(profileImgUrl);
            var data = {
                "email": facebookEmail,
                "name": fullName,
                "etag": "none",
                "social_id": social_id
            }
            $.ajax({
                url: "/auth/login_fb/",
                type: "POST",
                data: data,
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSR*FToken", getCookie('csrftoken'));
                },
                success: function(resp) {
                    msg = JSON.parse(resp)
                    if (msg['status'] == "failed") {
                        console.log('failed')
                    }
                    if (msg['status'] == "done") {

                        if (redirectUrlAfterLogin == "processBooking") {
                            $submitBooking($("#bookingForm"))
                        } else if (redirectUrlAfterLogin == "home") {
                            $(".mfp-close").click();
                            $('#login-status').load(location.href + ' #login-status');
                        }
                        console.log('success');
                    }
                }
            });
        }
    });
}

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

