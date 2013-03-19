var xHRObject = false

if (window.XMLHttpRequest) {
	xHRObject = new XMLHttpRequest();
} else if (window.ActiveXObject) {
	xHRObject = new ActiveXObject("Microsoft.XMLHTTP")
}

function getData() {
	if (xHRObject.readyState == 4 && xHRObject.status == 200) {
		var doc = xHRObject.responseText;
		alert(doc)
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
	}
}

function loadMore() {
	//Reset the function
	xHRObject.onreadystatechange = getData;
	var imgs = document.getElementsByTagName('img')
	alert(imgs.length)
	xHRObject.open("GET", "/calligraphys/ajax?opt=loadmore&index=" + imgs.length, true);
	
	xHRObject.send(null);
}
