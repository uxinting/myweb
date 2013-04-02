$(document).ready(function() {
	var article_width = $('#article').width();
	var trig_width = article_width * 0.03;
	var list_common_width = $('#article').offset().left;

	$('#article-list-trigger').css('width', trig_width + 'px');
	$('#article-list').css('width', list_common_width + 'px');
	
	$('#article-common-trigger').css('width', trig_width + 'px');
	$('#article-common').css('width', list_common_width + 'px');
	
	$('#article-list-trigger').click(function() {
		if ($('#article-left').css('left') == '0px') {
			$('#article-left').animate({left: '-' + list_common_width + 'px'});
		} else {
			$('#article-left').animate({left: '0px'});
		}
	});
	
	$('#article-common-trigger').click(function() {
		if ($('#article-right').css('right') == '0px') {
			$('#article-right').animate({right: '-' + list_common_width + 'px'});
		} else {
			$('#article-right').animate({right: '0px'});
		}
	});
});