!function($) {
	$(function() {
	
		//Back to top icon functions
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
				$(document).scrollTop($(document).scrollTop() / 1.2);
				if ($(document).scrollTop() < 1)
					clearInterval(id);
			}
		});
		
		//prev button
		$('.icon-prev').click(function() {
			
		});
		
		//next button
		$('.icon-next').click(function() {
		
		});
		
		//data-toggle
		$('[data-toggle="tooltip"]').mouseover(function() {
			$(this).tooltip('show');
		});
		
		//highlight
		$(document).mousemove(function(e) {
			var yy = e.clientY;
			var y = e.pageY;
			if ($('.article').data('highlight') != true) return;
			
			var article = $('.article');
			var ot = article.offset().top;
			if (y > ot && y < ot + article.height()) {
				article.addClass('highlight').css('background-position', '0px ' + yy + 'px');
			} else {
				article.removeClass('highlight');
			}
		});
		
	});
}(window.jQuery);