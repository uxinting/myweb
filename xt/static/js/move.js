window.onload = function init() {
	var article = document.getElementById('article')
	var article_list_trig = document.getElementById('article-list-trigger')
	var article_common_trig = document.getElementById('article-common-trigger')
	var article_list = document.getElementById('article-list')
	var article_common = document.getElementById('article-common')
	
	var aw = article.offsetWidth
	var ah = article.offsetHeight
	var lcw = article.offsetLeft
	
	article_list_trig.style.width = (parseInt(aw) * 0.03) + 'px'
	article_list.style.width = lcw + 'px'
	
	article_common_trig.style.width = (parseInt(aw) * 0.03) + 'px'
	article_common.style.width = lcw + 'px'
	
	article_list_trig.onclick = showList
	article_common_trig.onclick = showCommon
}

var moveJobId = 0

function moveList(direct) {
	var target = document.getElementById('article-left')
	var w = document.getElementById('article-list').offsetWidth
	var offset = target.offsetLeft
	
	target.style.position = 'absolute'
	if (direct == 'show') {
		if (parseInt(offset) + parseInt(w) <= 0)
			clearInterval(moveJobId)
		else 
			target.style.left = (parseInt(offset) - 6) + 'px'
	} else {
		if (parseInt(offset) >= 0)
			clearInterval(moveJobId)
		else 
			target.style.left = (parseInt(offset) + 6) + 'px'
	}
}

function showList() {
	var target = document.getElementById('article-left')
	var direct = ''
	if (parseInt(target.offsetLeft) >= 0) {
		direct = 'show'
	} else {
		direct = 'hide'
	}
	moveJobId = setInterval(moveList, 6, direct)
}

var commonright = 0
function moveCommon(direct) {
	var target = document.getElementById('article-right')
	var w = document.getElementById('article-common').offsetWidth
	
	target.style.position = 'absolute'
	if (direct == 'show') {
		if (commonright + parseInt(w) <= 0) {
			clearInterval(moveJobId)
		} else {
			commonright -= 6
			target.style.right = (commonright) + 'px'
		}
	} else {
		if (commonright >= 0)
			clearInterval(moveJobId)
		else {
			commonright += 6
			target.style.right = (commonright) + 'px'
		}
	}
}

function showCommon() {
	var target = document.getElementById('article-right')
	
	var direct = ''
	if (commonright >= 0) {
		direct = 'show'
	} else {
		direct = 'hide'
	}
	moveJobId = setInterval(moveCommon, 6, direct)
}