$(document).ready(function() {
    sendMail();
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

function sendMail() {
    var order_id = $('#current_order_id').val();
    data = JSON.stringify({
        'current_order_id': order_id,
    });
    $.ajax({
        type: 'POST',
        url: "/website/sendmail/",
        data: data,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response) {
            if (response['message'] == 'SUCCESS') {
                console.log("Success")
            }
        },
        dataType: 'json',
        contentType: 'application/json',
    });
}