$(function() {
	setTimeout(function() {
		$('.breadcrumbs').slideUp();
	}, 2000)
	
	$('#topNav').mouseover(function() {
		$('.breadcrumbs').slideDown();
	});
	
	$('#topNav').mouseleave(function() {
		setTimeout(function() {
			$('.breadcrumbs').slideUp();
		}, 2000)
	});
})