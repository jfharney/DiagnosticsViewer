var clicked = 0;
var lastURL = "";

function displayImageClick(imageURL) {
	$('.plot_btn').show();
	var imagePath = "<img src=\"" + imageURL + "\" \onerror=\"imgError(this);\"/>";
	document.getElementById("plotArea").style.visibility = 'visible';
	document.getElementById("plotArea").innerHTML = imagePath;
	lastURL = imageURL;
	clicked = 1;
}
function imgError(image) {
	image.onerror = "";
	image.src = "/static/exploratory_analysis/img/classic/Noimage.png";
	return true;
}

function displayTable(textTableURL) {
	$('.plot_btn').show();
	textTableURL = textTableURL;
	if (textTableURL.endsWith('.json')) {
		var tableHTML = '<table id="r22" width="100%" height="600" cellspacing="0"><thead><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th> </tr></thead><tfoot><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th></tr></tfoot></table>';
		document.getElementById("plotArea").style.visibility = 'visible';
		document.getElementById("plotArea").innerHTML = '' + tableHTML;

		//$(document).ready(function(){
		$('#r22').DataTable({
			"ajax" : {
				"url" : textTableURL,
				"dataSrc" : ""
			},
			"columns" : [{
				"data" : "name"
			}, {
				"data" : "position"
			}, {
				"data" : "office"
			}, {
				"data" : "extn"
			}, {
				"data" : "start_date"
			}, {
				"data" : "salary"
			}]
			//} );
		});
	} else {
		document.getElementById("plotArea").style.visibility = 'visible';
		document.getElementById("plotArea").innerHTML = '<iframe src="' + textTableURL + '" width=100% height=800 frameborder=0 ></iframe>';
	}
	lastURL = textTableURL;
	clicked = 1;

}

String.prototype.endsWith = function(suffix) {
	return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

function displayTableHover(textTableURL) {
	if (clicked != 1) {
		textTableURL = textTableURL;
		if (textTableURL.endsWith('.json')) {
			var tableHTML = '<table id="r22" width="100%" height="600" cellspacing="0"><thead><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th> </tr></thead><tfoot><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th></tr></tfoot></table>';
			document.getElementById("plotArea").style.visibility = 'visible';
			document.getElementById("plotArea").innerHTML = '' + tableHTML;

			//$(document).ready(function(){
			$('#r22').DataTable({
				"ajax" : {
					"url" : textTableURL,
					"dataSrc" : ""
				},
				"columns" : [{
					"data" : "name"
				}, {
					"data" : "position"
				}, {
					"data" : "office"
				}, {
					"data" : "extn"
				}, {
					"data" : "start_date"
				}, {
					"data" : "salary"
				}]
				//} );
			});
		} else {
			document.getElementById("plotArea").style.visibility = 'visible';
			document.getElementById("plotArea").innerHTML = '<iframe src="' + textTableURL + '" width=100% height=800 frameborder=0 ></iframe>';
		}

	}

}

function displayImageHover(imageURL) {
	if (clicked != 1) {
		var imagePath = "<img src=\"" + imageURL + "\" \onerror=\"imgError(this);\"/>";
		document.getElementById("plotArea").style.visibility = 'visible';
		$('#plotArea').show();
		document.getElementById("plotArea").innerHTML = imagePath;
	}
}

function ungluePlot() {
	clicked = 0;
	$('.plot_btn').hide();
	document.getElementById("plotArea").style.visibility = 'hidden';
}
function expandPlot() {
	window.open(lastURL);
}

function nodisplayImage() {
	if (clicked != 1) {
		document.getElementById("plotArea").style.visibility = 'hidden';
	}
}