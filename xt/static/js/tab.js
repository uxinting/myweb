window.onload = function () {
	var tags = document.getElementById('tabmenu').children;
	var contents = document.getElementById('tabcontent').children
	contents[0].style.display = 'block';
	for (var i = 0; i < tags.length; i++) {
		tags[i].index = i;
		tags[i].onclick = function () {
			for (var j = 0; j < tags.length; j++) {
				contents[j].style.display = 'none';
				tags[j].className = '';
			}
			tags[this.index].className = 'act';
			contents[this.index].style.display = 'block';
		}
	}
}