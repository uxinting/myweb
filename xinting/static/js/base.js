$(function() {
	setTimeout(function() {
		$('.breadcrumb').slideUp();
	}, 2000)
	
	$('#topNav').mouseover(function() {
		$('.breadcrumb').slideDown();
	});
	
	$('#topNav').mouseleave(function() {
		setTimeout(function() {
			$('.breadcrumb').slideUp();
		}, 2000)
	});
})