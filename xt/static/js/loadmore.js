var xHRObject = false

function middleImg() {
	var imgnodes = document.getElementById('calligraphy-grids').getElementsByTagName('img')
	for (var j = 0; j < imgnodes.length; j++) {
		var img = imgnodes[j]
		if (img.width < 280) {
			img.style.left = (280 - img.width) / 2 + 'px'
		}
		if (img.height < 280) {
			img.style.top = (280 - img.height) /2 + 'px'
		}
	}
}

window.onload = middleImg

if (window.XMLHttpRequest) {
	xHRObject = new XMLHttpRequest();
} else if (window.ActiveXObject) {
	xHRObject = new ActiveXObject("Microsoft.XMLHTTP")
}

function getData() {
	if (xHRObject.readyState == 4 && xHRObject.status == 200) {
		var doc = xHRObject.responseText;
		
		if (doc == '') {
			alert("ц╩спак")
			return
		}
		
		var grid = document.getElementById('calligraphy-grids')

		if (grid != null) {
			var node = document.createElement('ul')
			node.className = 'grid-row'
			node.innerHTML = doc
			grid.appendChild(node)
		}
		
		var imgnodes = document.getElementById('calligraphy-grids').getElementsByTagName('img')
		for (var i = imgnodes.length-4; i < imgnodes.length; i++) {
			var img = imgnodes[i]
			
			if (img.width < 280 && img.width != 0) {
				img.style.left = (280 - img.width) / 2 + 'px'
			}
			
			if (img.height < 280 && img.width != 0) {
				img.style.top = (280 - img.height) /2 + 'px'
			}
		}
	}
}

function loadMore() {
	//Reset the function
	xHRObject.onreadystatechange = getData;
	var imgs = document.getElementsByTagName('img')
	
	xHRObject.open("GET", "/calligraphys/ajax?opt=loadmore&index=" + imgs.length, true);
	
	xHRObject.send(null);
}
