$(document).ready(function() {
	middle();
});

function middle() {
	$('img').each(function() {
		var height = $(this).parent().height();
		var offsetTop = (height - $(this).height()) / 2;
		$(this).css('marginTop', offsetTop + 'px');
	});
}

function loadMore() {
	$.get('/calligraphys/ajax?opt=loadmore&index=' + $('img').size(), function(data, status) {
		if (status == 'success') {
			if (data.indexOf('<li>') < 0) {
				alert('none anymore');
				return;
			}
			
			$('#calligraphy-grids').append(data);
		} else {
			alert('Sorry, Service Error');
		}
		
		middle();
	});
}