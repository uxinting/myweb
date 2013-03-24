var moveJobId = 0
function moveList(direct, targetId) {
	var target = document.getElementById(targetId)
	var w = target.offsetWidth
	var offset = target.offsetLeft
	target.style.marginLeft

	if (direct == 'hide') {
		if (parseInt(offset) + parseInt(w) <= 20)
			clearInterval(moveJobId)
		else 
			target.style.left = (parseInt(offset) - 10) + 'px'
			//target.style.marginLeft = (parseInt(offset) - 6) + 'px'
	} else {
		if (parseInt(offset) >= 0)
			clearInterval(moveJobId)
		else 
			target.style.left = (parseInt(offset) + 10) + 'px'
	}
}

function onLeft() {
	document.getElementById('icon-left').style.display = 'none'
	moveJobId = setInterval(moveList, 6, 'hide', 'about-info')
}

function onRight() {
	moveJobId = setInterval(moveList, 6, 'show', 'about-info')
	document.getElementById('icon-left').style.display = 'block'
}