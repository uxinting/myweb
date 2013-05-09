$(function() {
	$('.icon-comments').click(function() {
		$($('body').children('div')[0])
		.removeClass('small-7');
		
		$('.article').addClass('small-7')
		
		$($('.article').next('div'))
		.removeClass('hide')
		.addClass('comment');
	});
})