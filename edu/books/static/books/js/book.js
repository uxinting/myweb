function showConfig() {
	var h = $(window).height();
	$('#config-container').css({'height': h}).show();
};

$(function() {
	$('form').submit(function(e) {
		e.preventDefault();//阻止默认
	});
})
