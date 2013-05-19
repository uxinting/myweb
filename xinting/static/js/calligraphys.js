$(function(){

	$(".thumbnail").find('img').click(function() {
		var s = '[src="' + $(this).attr('src') + '"]';
		$(".carousel-inner").find(s).parent().addClass('active');
		$('.fade').show();
	});
	
	$('.close').click(function() {
		$('.fade').hide();
		$(".carousel-inner").find('.active').removeClass('active');
	})
	
	$("[href='/calligraphy']").addClass('active');
});