var car = $('#car_make_list').val();
var cars = JSON.parse(car)
var bike = $('#bike_make_list').val();
var bikes = JSON.parse(bike)
var service_center = $('#service_center_list').val();
var service_center_list = JSON.parse(service_center);
var generic_problem = $('#generic_problem_list').val();
var generic_problem_list = JSON.parse(generic_problem);

$(document).ready(function() {
    /*populateSelect();*/
    prePopulateForm();
});
var isLoggedIn = $('#checklogin').val()

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

/*$('#login').on('click',function(e){
         var vehicle_type = $('#vehicle').val();
         var brand = $('#make').val();
         var service_center_address = $('#location').val();
         var specificProblems = $('#specificProblems').val();
         var pickup_time = $('#datetimepicker12').val();
         var service_type = getRadioValue( document.getElementById('bookingForm'), 'serviceType' );
         var selected_generic_problems = get_generic_problem();
         var source = "login";
         data = JSON.stringify({
            'vehicle_type': vehicle_type,
            'brand': brand,
            'service_center_address': service_center_address,
            'specificProblems': specificProblems,
            'source': source,
            'pickup_time': pickup_time,
            'service_type': service_type,
            'selected_generic_problems': selected_generic_problems,
        });

        $.ajax({
        type: 'POST',
        url: "/website/savebooking/",
        data: data,
        success: function(response) {
                 if(response['message'] == 'SUCCESS'){
                    window.location = "/website/login"
                 }
        },
        dataType: 'json',
        contentType: 'application/json',
      });
});*/


$(function() {

    $("#vehicle").change(function() {
        /*populateSelect();*/
    });

});

$(function() {
    $("#make").change(function() {
        populateSelectLocation();
    });

});

function populateSelectLocation() {
    brand = $("#make").val();
    vehicle_type = $("input[type='radio'].myvehicle:checked").val();
    var service_center_location = brand + "_" + vehicle_type;
    $("#location").html('');
    /*$("#make").html('<option value="1">Select Brand</option>');*/
    if (brand == '') {
        $('#location').append('<option value="">' + 'Select Service Center' + '</option>');
    } else if( brand!=null){
        $('#location').append('<option value="">' + 'Select Service Center' + '</option>');
        service_center_list[service_center_location].forEach(function(t) {
            $('#location').append('<option>' + t + '</option>');
        });
    }
}

function populateGenericProblem() {
    $("#generic_problem").empty();
    vehicle_type = $("input[type='radio'].myvehicle:checked").val();
    var lastSelectedGenericProblemsAsString = $('#selected_generic_problems_listed').val();
    var lastSelectedGenericProblems = new Array();
    if (typeof lastSelectedGenericProblemsAsString != 'undefined') {
        if (lastSelectedGenericProblemsAsString.length > 0 && lastSelectedGenericProblemsAsString != "None") {
            lastSelectedGenericProblems = JSON.parse(lastSelectedGenericProblemsAsString);
        }
    }
    var problem = generic_problem_list[vehicle_type];
    var count = 0;
    count++
    if (typeof problem != 'undefined' && problem.length > 0) {
        $('#generic_problem_length').val(problem.length);
    }
    for (var i = 0; i < problem.length; i++) {
        var selected = 0
        lang = problem[i]
        var active = "";
        var tick = "none";
        for (var j = 0; j < lastSelectedGenericProblems.length; j++) {
            if (lang == lastSelectedGenericProblems[j]) {
                selected = 1
                    //         active="service-my-wheels-vitals-active";
                    //         tick="inline";
                break
            }
        }
        var abc = '<li id=' + i + ' class="generic_problem_list ' + active + '">' +
            '<div class="service-my-wheels-vitals-level-title">' + lang + '</div>' +
            '<div class="service-my-wheels-vitals-level-tick" style="display:' + tick + '"></div>' +
            '<input type="hidden" id="generic_problem_' + i + '" name="generic_problem_' + i + '" value="">' +
            '<span class="clearfix"></span>' +
            '</li>';
        /* append('<input type="checkbox" name ="generic_problem" id ="generic_problem_' + i +'" value="' + lang + '">').
         append(lang).
         appendTo('#generic_problem');*/
        $('#generic_problem').append(abc);
        if (selected == 1) {
            $("#" + i).click();
        }
    }
}

//populate brand

function populateSelect() {
    vehicle = $("input[type='radio'].myvehicle:checked").val();
    $("#make").html('');
    $('#make').append('<option value="">' + 'Select Brand' + '</option>');
        if (vehicle == 'Select Vehicle Type') {
        populateSelectLocation();
    }

    if (vehicle == 'Car') {
        cars.forEach(function(t) {
            $('#make').append('<option>' + t + '</option>');
        });
        populateSelectLocation();
        populateGenericProblem();

    }

    if (vehicle == 'Bike') {
        bikes.forEach(function(t) {
            $('#make').append('<option>' + t + '</option>');
        });
        populateSelectLocation();
        populateGenericProblem();

    }
}
$('.myvehicle').click(function() {
    populateSelect();
});
$('#resetForm').click(function() {
    $('#generic_problem').load(location.href + ' #generic_problem');
});
$('#chooseServiceCenter').click(function() {
    $('#chooseServiceCenter').prop('checked', false);
    $('#selectServiceCenter').hide();
    $('.serviceCenter').show();
    $('#serviceCenterforme').show();
    $('#chooseServiceCenteryDefault').prop('checked', true);
});
$('#chooseServiceCenteryDefault').click(function() {
    $('select option:contains("Select Service Center")').prop('selected',true);
    $('#chooseServiceCenteryDefault').prop('checked', false);
    $('.serviceCenter').hide();
    $('#serviceCenterforme').hide();
    $('#selectServiceCenter').show();
    $('#chooseServiceCenter').prop('checked', false);
});
function prePopulateForm() {
    var lastSelectedVehicle = $('#selected_vehicle_type').val();
    var lastSelectedBrand = $('#selected_brand').val();
    var lastSelectedSpecificProblems = $('#selected_specific_problems_listed').val();
    var lastSelectedServiceCenter = $('#selected_service_center_address').val();
    var lastSelectedGenericProblems = $('#selected_generic_problems_listed').val();
    var lastSelectedPickupTime = $('#selected_pickuptime').val();
    var lastSelectedServiceType = $('#selected_service_type').val();
    if (lastSelectedPickupTime == "None") lastSelectedPickupTime = "";
    if (lastSelectedSpecificProblems == "None") lastSelectedSpecificProblems = "";
    $('#vehicle').val(lastSelectedVehicle);
    if (typeof lastSelectedVehicle != 'undefined' && lastSelectedVehicle.length > 0) {
        $(':radio[value=' + lastSelectedVehicle + ']').attr('checked', 'checked');
    }
    populateSelect();
    if (lastSelectedBrand != "" && lastSelectedBrand != "None" && typeof(lastSelectedBrand) != undefined) {
        $('#make').val(lastSelectedBrand);
    }
    populateSelectLocation();
    if (lastSelectedServiceCenter != "" && lastSelectedServiceCenter != "None" && typeof(lastSelectedServiceCenter) != undefined) {
        $('#location').val(lastSelectedServiceCenter);
    }
    $('#specificProblems').val(lastSelectedSpecificProblems);
    $('#datetimepicker12').val(lastSelectedPickupTime);

    lastSelectedGenericProblems = lastSelectedGenericProblems.split(",");
    for (var i = 0; i < lastSelectedGenericProblems.length; i++) {
        checkCheckBoxWithValue(lastSelectedGenericProblems[i]);
    }
    //    $('#datetimepicker12').val(lastSelectedPickupTime);
    if (typeof lastSelectedServiceType != 'undefined' && lastSelectedServiceType.length > 0) {
        $(':radio[value=' + lastSelectedServiceType + ']').attr('checked', 'checked');
    }
}

function getRadioValue(form, name) {
    var val;
    var radios = form.elements[name];

    for (var i = 0, len = radios.length; i < len; i++) {
        if (radios[i].checked) {
            val = radios[i].value;
            break; // and break out of for loop
        }
    }
    return val;
}

function checkCheckBoxWithValue(val) {
    $(":checkbox").filter(function() {
        return this.value == val;
    }).prop("checked", "true");

}
$("#chooseservicecenterdiv").click(function() {
    var check = document.getElementById("chooseservicecenter").checked;
    if (check) {
        $("#chooseservicecenterdiv").css('display', 'none')
        $("#servicecenterloc").css('display', 'block')
        $("#defaultservicecenter").prop("checked", false);
    }

});

$("#defaultservicecenter").click(function() {
    var check = document.getElementById("defaultservicecenter").checked;
    if (check) {
        $("#servicecenterloc").css('display', 'none')
        $("#chooseservicecenterdiv").css('display', 'block')
        $("#chooseservicecenter").prop("checked", false);
    }
});

$('#generic_problem').on('click', '.generic_problem_list', function() {
    var genericNameId = $(this).attr('id');
    var genericName = $(this).text();
    $(this).toggleClass('service-my-wheels-vitals-active');
    if ($(this).hasClass('service-my-wheels-vitals-active')) {
        $(this).find('.service-my-wheels-vitals-level-tick').css('display', 'inline-block');
        $('#generic_problem_' + genericNameId).val(genericName);
    } else {
        $(this).find('.service-my-wheels-vitals-level-tick').hide();
        $('#generic_problem_' + genericNameId).val("");
    }

});


$('.register-btn').click(function() {
    //$('#login_form').attr('name', 'registerForm');
    $('.errorMessage').hide();
    $('#signup_form').show();
    $('#login_form').hide();
    $('#forgot_password_form').hide();
    $('#forgot_password_otp_form').hide();
    $('#guest_form').hide();
    $('.register-btn').hide();
    $('.already-account-btn').show();
    $('.continue_as_guest-btn').show();
    //$('.b').show();
});
$('.continue_as_guest-btn').click(function() {
$('.errorMessage').hide();
    /*$('#login_form').attr('name', 'registerForm');*/
    //$('.a').hide();
    $('#login_form').hide();
    $('#forgot_password_form').hide();
    $('#signup_form').hide();
    $('.already-account-btn').show();
    $('.register-btn').show();
    $('.continue_as_guest-btn').hide();
   // $('.c').show();
   $('#guest_form').show();
});
$('.already-account-btn').click(function() {
$('.errorMessage').hide();
   // $('.b').hide();
   $('#signup_form').hide();
    //$('.c').hide();
    $('#guest_form').hide();
    $('#forgot_password_form').hide();
    $('.login-link').show();
    $('.already-account-btn').hide();
    $('.register-btn').show();
    $('.continue_as_guest-btn').show();
   // $('.a').show();
   $('#login_form').show();
});
$('.forgot_password_btn').click(function() {
    $('.errorMessage').hide();
    $('#signup_form').hide();
    $('#guest_form').hide();
    $('#login_form').hide();
    $('#forgot_password_form').show();
});
$(function(){


$.validator.addMethod("mobile", function(value, element) {
    return this.optional(element) || /^[1-9][0-9]*(\[0-9]+)?|0+\[0-9]\d{10}$/.test(value);
    });
var passwordValidator =	$("#bookingForm").validate({
		rules: {
			vehicle_type:{
							required:true,
	  			         },
	  		brand: {
	  		    required:true,
	  		},
	  		location: {
	  		    required:true,
	  		},
	  		pickup_time: {
	  		     required:true,
	  		},
	  		terms_condition:{
	  		    required:true,
	  		}

		},
				messages:{
					"vehicle_type":{
						required:"Please select the Vehicle type"
						},
					"brand": {
					    required:"Please choose the Vehicle brand"
					},
					"pickup_time":{
					    required:"Please choose the pick up time"
					},
					"location": {
					    required:"Please choose the service center or uncheck to choose service center by default"
					},
					"terms_condition": {
					    required:"Please select the terms and conditions"
					},

                   },
					 errorPlacement: function(error, element) {
		                  if ( element.is(":radio") ){
		                        error.appendTo( element.parent().parent() );
		                  }
		                  else if ( element.is(":checkbox") ){
		                        error.appendTo ( element.parent().parent());
		                  }
		                  else{
		                        error.appendTo( element.parent() );
		                  }
					 }

			});
				});

$(function(){
var passValidator =	$("#login_form").validate({
		rules: {
			email:{
                required:true,
                 email:true,
	  		    emailId:true,
             },
	  		password: {
	  		    required:true,
	  		},
		},
        messages:{
            "email":{
                required:"Please Enter Email Id"
                },
            "password": {
                required:"Please Enter Password"
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
});
$(function(){
$.validator.addMethod("emailId", function(value, element) {
						return this.optional(element) || /^\b[A-Z0-9._-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i.test(value);
					});
var passValidator =	$("#signup_form").validate({
		rules: {
			customer_name:{
                required:true,
             },
	  		email: {
	  		    required:true,
	  		    email:true,
	  		    emailId:true,
	  		},
	  		password: {
	  		    required:true,
	  		},
		},
        messages:{
            "customer_name":{
                required:"Please Enter Customer Name"
                },
            "email": {
                required:"Please Enter Email Id"
            },
            "password": {
                required:"Please Enter Password"
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
});
$(function(){
var passValidator =	$("#guest_form").validate({
		rules: {
			email:{
                required:true,
                email:true,
	  		    emailId:true,
             },
	  		customer_name: {
	  		    required:true,
	  		},
		},
        messages:{
            "email":{
                required:"Please Enter Email Id"
                },
            "customer_name": {
                required:"Please Enter Your Name"
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
});
$("#forgot_password_form").validate({
		rules: {
			mail_mobile:{
                required:true,
             },

		},
        messages:{
            "mail_mobile":{
                required:"Please Enter Email Id or mobile no."
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
