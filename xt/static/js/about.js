$(document).ready(function(){
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
