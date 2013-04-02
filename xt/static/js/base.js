$(document).ready(function() {
	$('#icon-user').click(function() {
		var offsetLeft = ($('#fade').width() - $('#dialog').width()) / 2;
		$('#dialog').css({marginLeft: offsetLeft + 'px'});
		$('#fade').css({height: $('body').height() + 'px'});
		
		$('#fade').toggle();
		$('#dialog').toggle('fast');
		
		$('#icon-close').click(function() {
			$('#dialog').hide();
			$('#fade').hide();
		});
	});
	
	$('#icon-config').click(function() {
		var t = $(this).offset().top + 20;
		var l = $(this).offset().left;
		$('#bubble').css({top: t + 'px', left: l + 'px'});
		$('#bubble').slideToggle('fast');
	});
	
	$('#icon-msg').click(function() {
		var offsetLeft = ($('#fade').width() - $('#dialog').width()) / 2;
		$('#dialog').css({marginLeft: offsetLeft + 'px', marginTop: '0px'});
		$('#fade').css({height: $('body').height() + 'px'});
		
		$('#fade').toggle();
		$('#dialog').toggle('fast');
		
		$('#icon-close').click(function() {
			$('#dialog').hide();
			$('#fade').hide();
		});
	});
});