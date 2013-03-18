var xHRObject = false

if (window.XMLHttpRequest) {
	xHRObject = new XMLHttpRequest();
} else if (window.ActiveXObject) {
	xHRObject = new ActiveXObject("Microsoft.XMLHTTP")
}

function getData() {
	if (xHRObject.readyState == 4) {
		var doc = xHRObject.responseText;
		var grid = document.getElementById('calligraphy-grids')
		alert(doc)
		if (grid != null) {
			var node = document.createElement('ul')
			node.className = 'grid-show'
		}
	}
}

function loadMore() {
	//Reset the function
	xHRObject.onreadystatechange = getData;
	
	xHRObject.open("GET", "/calligraphys/ajax", true);
	
	xHRObject.send(null);
}
