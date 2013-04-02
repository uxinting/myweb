$(document).ready(function() {
	$('#icon-user').click(function() {
		$('#dialog').toggle();
		$('#fade').toggle();
		
		var offsetLeft = ($('#fade').width() - $('#dialog').width()) / 2;
		$('#dialog').css({marginLeft: offsetLeft + 'px'});
		
		$('#icon-close').click(function() {
			$('#dialog').toggle();
			$('#fade').toggle();
		});
		
		$('#fade').click(function() {
			$('#dialog').toggle();
			$('#fade').toggle();
		});
	});
});