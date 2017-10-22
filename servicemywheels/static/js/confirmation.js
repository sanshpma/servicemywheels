$(document).ready(function() {
    populateSelectedgenericproblem();
    if($('#customer_email').val().split('@')[1]=="dummyfbemail.com"){
        $('#customer_email').attr('readonly',false)
    }
    else{
        $('#customer_email').attr('readonly',true)
    }
});

function populateSelectedgenericproblem() {
    var lastSelectedGenericProblemsByUser = $('#selected_generic_problems_listed_by_user').val();
    var lastSelectedGenericProblemsByUser = JSON.parse(lastSelectedGenericProblemsByUser);

    for (var i = 0; i < lastSelectedGenericProblemsByUser.length; i++) {
        var genericProblem = '<li id="invest_LFT" class="emltd-doctor-cons-invest-list-active">' +
            '<span style="text-align:left;font-weight: normal; width: 160px" class="emltd-doctor-cons-invest-list-title">' + lastSelectedGenericProblemsByUser[i] + '</span>' +
            '<span class="service-my-wheels-vitals-level-tick" style="display: inline-block;"></span> ' +
            '<span class="clearfix"></span></li>';
        $('#invest-list').append(genericProblem);
    }
}
var count = 0;
$(document).on('click', '.morebuttonformobile', function() {
    count++;
    $('#count').val(count);
    $('.morebuttonformobile').hide();
    var customer_mobile_number = '<input type="text" name="customer_new_mobile_number">' +
        '<input type="button" value="Add More Mobile Number" class="morebuttonformobile" id="get_more_addresses_"+count><br>';
    $('.b').append(customer_mobile_number);
    '<br>'
});
$('#edit_order').on('click', function(e) {
    window.location = "/website/booking"
    if (isLoggedIn == "Loggedin") {}
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

$('.pickUpAddress').click(function(event) {
    if ($(this).attr('id') != 'add-addr') {
        var idStr = $(this).attr('id');
        var splitArry = idStr.split("_");
        $("#user_selected_address_id").val(splitArry[1]);
        $('.port-os-sel-addr').css('margin-top', '0px');
        $('#sel-' + splitArry[0] + '-' + splitArry[1]).css('margin-top', '-2px');
        $('.pickUpAddress').removeClass('port-os-green');
        $('.pickUpAddressSelected').removeClass('port-os-dk-green');
        $('.port-os-sel-addr').removeClass('port-os-dk-green');
        $('.port-os-sel-text').text('Select Address');
        var dropselectTextId= $("#user_drop_selected_address_id").val();
         if(typeof dropselectTextId!='undefined' && dropselectTextId.length>0){
             $('#sel-dropaddress-txt-' + dropselectTextId).text('Selected');
             $('#sel-dropaddress-'+dropselectTextId).addClass('port-os-dk-green');
             $('#sel-dropaddress-'+dropselectTextId).css('margin-top', '-2px');
        }
        $(this).addClass('port-os-green');
        $(this).find('.port-os-sel-addr').addClass('port-os-dk-green');

        //$(this).find('.port-os-sel-text').text('Selected');
        $('#sel-address-txt-' + splitArry[1]).text('Selected');
    }
});

$('.dropAddress').click(function(event) {
    if ($(this).attr('id') != 'add-addr') {
        var idStr = $(this).attr('id');
        var splitArry = idStr.split("_");
        $("#user_drop_selected_address_id").val(splitArry[1]);
        $('.port-os-sel-addr').css('margin-top', '0px');
        $('#sel-' + splitArry[0] + '-' + splitArry[1]).css('margin-top', '-2px');
        $('.dropAddress').removeClass('port-os-green');
        $('.dropAddressSelected').removeClass('port-os-dk-green');
        $('.port-os-sel-addr').removeClass('port-os-dk-green');
        $('.port-os-sel-text').text('Select Address');
        var pickupselectTextId= $("#user_selected_address_id").val();
        if(typeof pickupselectTextId!='undefined' && pickupselectTextId.length>0){
             $('#sel-address-txt-' + pickupselectTextId).text('Selected');
             $('#sel-address-'+pickupselectTextId).addClass('port-os-dk-green');
             $('#sel-address-'+pickupselectTextId).css('margin-top', '-2px');
        }
        $(this).addClass('port-os-green');
        $(this).find('.port-os-sel-addr').addClass('port-os-dk-green');
       // $(this).find('.port-os-sel-text').text('Selected');
        $('#sel-dropaddress-txt-' + splitArry[1]).text('Selected');
    }
});

$('#confirm-order').click(function() {
    $('#pick-up-address-id').val($("#user_selected_address_id").val());
    if ($("#user_drop_selected_address_id").val() > 0) {
        $('#drop-address-id').val($("#user_drop_selected_address_id").val());
    } else {
        if ($("#user_selected_address_id").val() > 0 && $('#add-pick-up-address').is(":checked") == false) {
            $('#drop-address-id').val($("#user_selected_address_id").val());
        }
    }
    var serviceType = $("input[type='radio'].service-type:checked").val();
    var mobile_number = $("#mobile_number").val();
    var pattern = /^(\+\d{1,3}[- ]?)?\d{10}$/
    if (pattern.test(mobile_number.value) == false) {
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Mobile number format not correct");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }
    $('#selected-service-type').val(serviceType);
    $('#user_mobile_number').val(mobile_number);

    if ($("#user_selected_address_id").val() == 0) {
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Please provide pickup address");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }
    if (typeof($("input[type='radio'].service-type:checked").val()) == "undefined") {
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Please Choose Service Type");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }

    if ($("#mobile_number").val().length == 0) {
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Please provide mobile number");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }
    if ($('#add-pick-up-address').is(":checked") == true && $('#drop-address-id').val() == "") {
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Please provide drop address or uncheck Drop Address different than Pickup Address Checkbox");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }
    if ($('#add-pick-up-address').is(":checked") == false) {
        $('#drop-address-id').val($('#pick-up-address-id').val());
    }
    if ($('#drop-address-id').val() == "0"){
        $("#errorMsgDivConfirmation").show();
        $("#errorMsgDivTextConfirmation").text("Please provide drop address or uncheck Drop Address different than Pickup Address Checkbox");
        $("#errorMsgDivTextConfirmation").addClass("error-message-style");
        return;
    }
    if($("#user_selected_address_id").val() > 0 && typeof($("input[type='radio'].service-type:checked").val()) != "undefined" && $("#mobile_number").val().length > 0)
    {
        $('#order-summary').submit();
    }
});

$('#edit-order').click(function() {
    window.location = "/website/booking";
});

var count=0;
$('.pickUpAddress').each(function(){
    count++;
});

if (count>1) {
    $('.morebuttonforaddress').css('margin-top','20px');
}
$(function(){
var passValidator =	$("#add-new-address").validate({
		rules: {
			address:{
                required:true,
             },
	  		pincode: {
	  		    required:true,
	  		},
		},
        messages:{
            "address":{
                required:"Please Enter Your new address"
                },
            "pincode": {
                required:"Please Enter Pin Code"
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