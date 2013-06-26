function showConfig() {
	var h = $(window).height();
	$('#config-container').css({'height': h}).show();
};

$(function() {
	//绑定ajax
	var options = {
		success: function(data, status) {
			alert(data + ' ' + status);
		}
	};
	$('#config-container form').ajaxForm(options);
	
	//默认
	$('#goDefault').click(function () {
		$('body').css({
			'background-color': 'rgb(204, 232, 207)',
			'color': 'rgb(71, 72, 74)',
			'font-family': '微软雅黑'
		});
			
		$('.article p').attr('style','font-size: 15px; word-spacing: 5px;letter-spacing: 1px; line-height: 25px; margin: 0;padding: 20px 8px;');
		
		$('#inputBackground').val('204, 232, 207');
		$('#inputFontColor').val('71, 72, 74');
		$('#selectFontFamily')[0].options[0].selected = true;
		$('#inputFontSize').val('15');
		$('#inputLetterSpace').val('1');
		$('#inputLineHeight').val('25');
		$('#inputParaPad').val('20');
	});
	//绑定input blur事件
	$('#inputBackground').blur(function (e) {
		var color = $(this).val().replace(/\s+/g, '')//去空格

		var re = /^\d+,\d+,\d+$/
		if (!re.test(color)) {
			$(this).val("");
			return;
		}
		$('body').css({'background-color': 'rgb(' +color+')'});
	});
	
	$('#inputFontColor').blur(function (e) {
		var color = $(this).val().replace(/\s+/g, '')//去空格

		var re = /^\d+,\d+,\d+$/
		if (!re.test(color)) {
			$(this).val("");
			return;
		}
		$('body').css({'color': 'rgb(' +color+')'});
	});
	
	$('#selectFontFamily').change(function () {
		var sff = $(this);
		$('body').css({'font-family': sff.val()});
	});
	
	$('#inputFontSize').blur(function () {
		var size = $(this).val();
		var re = /^\d+$/;
		if (!re.test(size)) {
			$(this).val('');
			return;
		}
		
		size = parseInt(size);
		if (size < 10) size = 10;
		if (size > 40) sizse = 40;

		$('.article p').css({'font-size': size + 'px'});
	});
	
	$('#inputLetterSpace').blur(function() {
		var space = $(this).val();
		var re = /^\d+$/;
		if (!re.test(space)) {
			$(this).val('');
			return;
		}
		
		space = parseInt(space);
		if (space > 5) space = 5;
		
		$('.article p').css({'letter-spacing': space+'px'});
	});
	
	$('#inputLineHeight').blur(function() {
		var lineh = $(this).val();
		var re = /^\d+$/;
		if (!re.test(lineh)) {
			$(this).val('');
			return;
		}
		
		lineh = parseInt(lineh);
		if (lineh < 20) lineh = 20;
		if (lineh > 35) lineh = 35;
		
		$('.article p').css({'line-height': lineh+'px'});
	});
	
	$('#inputParaPad').blur(function() {
		var pp = $(this).val();
		var re = /^\d+$/;
		if (!re.test(pp)) {
			$(this).val('');
			return;
		}
		
		pp = parseInt(pp);
		if (pp < 5) pp = 5;
		if (pp > 50) pp = 50;
		
		$('.article p').css({'padding': pp+'px 8px'});
	});
	
	$('#checkHLBg').change(function() {
		var article = $('.article')
		if (article.data('highlight') == '') return;
		
		var c = $(this)[0].checked;
		article.data('highlight', c);
	});
})
