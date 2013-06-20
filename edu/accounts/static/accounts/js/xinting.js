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
		
		$('form').submit(function() {
			//check empty input
			var inputs = $(this).find('input');
			for (var i = 0; i < inputs.length; i++) {
				var idata = $(inputs[i]);
				if (idata.data('request') && idata.val() == '') {
					idata.tooltip({'title': '不能为空'});
					idata.tooltip('show');
					return false;
				}
			}
			
			//check email format
			var email = $('[type="email"]');
			if (typeof(email) != 'undefined') {
				var re = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
				if (!re.test(email.val())) {
					email.tooltip({'title': '不是一个邮箱'}).tooltip('show');
					return false;
				}
			}
			return true;
		});
	});
}(window.jQuery);