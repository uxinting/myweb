$(function() {
	//绑定ajax
	var options = {
		success: function(data, status) {
			alert(data);
		}
	};
	$('#config-container form').ajaxForm(options);
	
	var cp = new colorpicker('color-pick', function(color) {
		if ($('#inputBackground')[0].checked) {
			$('#testbody').css({'background-color': '#' +color});
			$('[name="background"]').val(color);
		} else {
			$('#testbody').css({'color': '#' + color});
			$('[name="fontColor"]').val(color);
		}
	});

	var bg;
	if ($('#inputBackground')[0].checked) {
		bg = $('#testbody').css('background-color');
	} else {
		bg = $('#testbody').css('color');
	}
	var rgbs = bg.substring(4, bg.length-1).split(',');
	cp.setColor(parseInt(rgbs[0]), parseInt(rgbs[1]), parseInt(rgbs[2]));
	
	$('#inputBackground, #inputFontColor').change(function() {
		var bg;
		if ($('#inputBackground')[0].checked) {
			bg = $('#testbody').css('background-color');
		} else {
			bg = $('#testbody').css('color');
		}
		var rgbs = bg.substring(4, bg.length-1).split(',');
		cp.setColor(parseInt(rgbs[0]), parseInt(rgbs[1]), parseInt(rgbs[2]));
	})
	
	//mousewheel of text
	$('[type="text"]').mousewheel(function(event, delta){
		var value = parseInt($(this).val());
		if (delta > 0) {
			value += 1;
		} else {
			value -= 1;
			if (value < 0) value = 0;
		}
		
		$(this).val(value);
		$(this).blur();
		$(this).focus();
	});
	
	//默认
	$('#goDefault').click(function () {
		$('body').css({
			'background-color': 'rgb(204, 232, 207)',
			'color': 'rgb(71, 72, 74)',
			'font-family': '微软雅黑'
		});
			
		$('.article p').attr('style','font-size: 15px; word-spacing: 5px;letter-spacing: 1px; line-height: 25px; margin: 0;padding: 20px 8px;');
		
		$('#inputBackground').val('cce8cf');
		$('#inputFontColor').val('47484a');
		if ($('#inputBackground')[0].checked) {
			cp.setColor(204, 232, 207);
		} else {
			cp.setColor(71, 72, 74);
		};
		
		$('#selectFontFamily')[0].options[0].selected = true;
		$('#inputFontSize').val('15');
		$('#inputLetterSpace').val('1');
		$('#inputLineHeight').val('25');
		$('#inputParaPad').val('20');
	});
	//绑定input blur事件
	$('#inputBackground').change(function (e) {
		var color = $(this).val().replace(/\s+/g, '')//去空格

		var re = /^[a-f0-9]{6}$/
		if (!re.test(color)) {
			$(this).val("");
			return;
		}
		$('#testbody').css({'background-color': '#' +color});
	});
	
	$('#inputFontColor').change(function (e) {
		var color = $(this).val().replace(/\s+/g, '')//去空格

		var re = /^[a-f0-9]{6}$/
		if (!re.test(color)) {
			$(this).val("");
			return;
		}
		$('#testbody').css({'color': '#' +color});
	});
	
	$('#selectFontFamily').change(function () {
		var sff = $(this);
		$('#testbody').css({'font-family': sff.val()});
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
