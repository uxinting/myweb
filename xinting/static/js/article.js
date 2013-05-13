$(function() {
	$('#comments').click(function() {
		var offset = $('#article').height();
		var id = setInterval(moveTop, 10);
		$(document).scrollTop(10);
		
		function moveTop() {
			$(document).scrollTop($(document).scrollTop() * 1.1);
			if ($(document).scrollTop() > offset)
				clearInterval(id);
		}
	});
	
	$(document).scroll(function() {
		if ($(this).scrollTop() > 0) {
			$('.icon-backtop').show();
		} else {
			$('.icon-backtop').hide();
		}
	});
	
	$('.icon-backtop').click(function() {
		var id = setInterval(moveTop, 10);
		function moveTop() {
			$(document).scrollTop($(document).scrollTop() / 1.1);
			if ($(document).scrollTop() < 1)
				clearInterval(id);
		}
	});
	
	
})