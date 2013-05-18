$(function(){
	$(".thumbnail").find('img').click(function() {
		var s = '[src="' + $(this).attr('src') + '"]';
		$(".carousel-inner").find(s).parent().addClass('active');
	});
	
	$("[href='/calligraphy']").addClass('active');
});