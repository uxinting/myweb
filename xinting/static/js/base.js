$(function() {
	$('#space').css({'height': '20px', 'display': 'none'});
	setTimeout(function() {
		$('#topNav').slideUp();
		$('#space').slideDown();
	}, 2000)
})