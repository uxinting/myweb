var id = new Array();

$(document).ready(function() {
	$('#picture-filename').val($(this).val());
	$('#picture-file').find('input').change(function() {
		$('#picture-filename').val($(this).val());
	});
	
	//download button
	
	//picture submit
	id['picture'] = setInterval(checkDownload, 5000, 'picture');
});

function checkDownload(type) {
	$.get('/tools/ajax?type=' + type, function(data, status) {
		if (status == 'success') {
			if (data) {
				$('#' + type + '-download').css({'display': 'inline-block'});
				if (data == 'process') {
					$('#'+type+'-download').text('processing');
					return;
				}
			
				$('#'+type+'-download').attr('href', data)
					.attr('disabled', false)
					.css({'background': '#cccccc'})
					.text('Download');
				
				clearInterval(id[type]);
			}
		} else {
			alert("error");
		}
	});
}