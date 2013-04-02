$(document).ready(function(){
	$('.about-container').css({height: $('img').height() * 0.9 + 'px'});
	
	$('#icon-left').click(function() {
		//alert('icon-left');
		$('#icon-left').toggle();
		$('#about-info').animate({marginLeft: '-300px'});
	});
	
	$('#icon-right').click(function() {
		$('#icon-left').toggle();
		$('#about-info').animate({marginLeft: '0px'});
	});
});
