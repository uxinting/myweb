function imgCenter() {
	var img = document.getElementById('pic')
	var container = document.getElementById('pic-container')
	img.style.position = 'absolute'
	if (img.width < container.offsetWidth) {
		img.style.left = (container.offsetWidth - img.width) / 2 + 'px'
	}
	if (img.height < container.offsetHeight) {
		img.style.top = (container.offsetHeight - img.height) /2 + 'px'
	}
}
