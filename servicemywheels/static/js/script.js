/*

function hideRequired(start, end) {
	$('.date_toggle').hide();
	var i = start;
	var days = 0;
	$('#taskManagerHead .date_toggle').each(function(){
		days++;
	});
	var back_start, back_end, next_start, next_end;
	if(start - 7 <= 0){
		back_start = 1;
	} else {
		back_start = start - 7;
	}
	back_end = back_start + 6;
	if(end + 7 > days){
		next_end = days;
	} else {
		next_end = end + 7;
	}
	next_start = next_end - 6;
	$('.back_nav').attr('start', back_start);
	$('.back_nav').attr('end', back_end);
	$('.next_nav').attr('start', next_start);
	$('.next_nav').attr('end', next_end);
	while (i <= end) {
		if($('.date_' + ('0' + i).slice(-2)).length > 0){
			$('.date_' + ('0' + i).slice(-2)).show();
		}
		i++;
	}

}

//Setting current date for table.
function setTableCurrent() {
	var today = new Date();
	var today_date = today.getDate();
	var end_date = today_date + 6;
	hideRequired(today_date, end_date);
}

$('.back_nav, .next_nav').live('click', function() {
	hideRequired(parseInt($(this).attr('start')), parseInt($(this).attr('end')));
	return false;
});
*/
