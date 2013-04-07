$(document).ready(function() {
	$('#filename').val('');
	$('#file').find('input').change(function() {
		$('#filename').val($(this).val());
	});
});