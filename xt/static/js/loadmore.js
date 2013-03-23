var xHRObject = false

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

function middleImg() {
	var imgnodes = document.getElementById('calligraphy-grids').getElementsByTagName('img')
	for (var j = 0; j < imgnodes.length; j++) {
		imgnodes[j].style.top = (140 - imgnodes[j].height / 2) + 'px'
		if (img.width < 280) {
			img.style.left = (container.offsetWidth - img.width) / 2 + 'px'
		}
		if (img.height < container.offsetHeight) {
			img.style.top = (container.offsetHeight - img.height) /2 + 'px'
		}
	}
}

//window.onload = middleImg

if (window.XMLHttpRequest) {
	xHRObject = new XMLHttpRequest();
} else if (window.ActiveXObject) {
	xHRObject = new ActiveXObject("Microsoft.XMLHTTP")
}

function getData() {
	if (xHRObject.readyState == 4 && xHRObject.status == 200) {
		var doc = xHRObject.responseText;
		
		if (doc == '') {
			alert('没有了')
			return
		}
		
		var grid = document.getElementById('calligraphy-grids')

		if (grid != null) {
			var node = document.createElement('ul')
			node.className = 'grid-row'
			node.innerHTML = doc
			grid.appendChild(node)
		}
		
/*		var imgnodes = document.getElementById('calligraphy-grids').getElementsByTagName('img')
		for (var i = imgnodes.length-4; i < imgnodes.length; i++) {
			imgnodes[i].style.top = (140 - imgnodes[i].height / 2) + 'px'
		}*/
	}
}

function loadMore() {
	//Reset the function
	xHRObject.onreadystatechange = getData;
	var imgs = document.getElementsByTagName('img')
	
	xHRObject.open("GET", "/calligraphys/ajax?opt=loadmore&index=" + imgs.length, true);
	
	xHRObject.send(null);
}
