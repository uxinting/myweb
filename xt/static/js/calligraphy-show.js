$(document).ready(function() {
	var img = $('#pic');
	var offseth = (img.parent().height() - img.height()) / 2;
	var offsetw = (img.parent().width() - img.width()) / 2;
	img.css({'top': offseth + 'px', 'left': offsetw + 'px'});
});