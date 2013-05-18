$(function(){
	$('.fade-').hide();

	$(".thumbnail").find('img').click(function() {
		var s = '[src="' + $(this).attr('src') + '"]';
		$(".carousel-inner").find(s).parent().addClass('active');
		$('.fade-').show();
	});
	
	$('.close').click(function() {
		$('.fade-').hide();
	})
	
	$("[href='/calligraphy']").addClass('active');
});