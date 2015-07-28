function populate_downloads() {

	document.getElementById("plotArea").style.visibility = 'visible';

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/downloadlist/' + dataset + '/' + pckg + '/null/null';

	$.ajax({
		type : "GET",
		url : url,
		dataType : 'text',
		//async: false,
		//data: data,
		success : function(response_data) {

			console.log('success in getting downloadlist');

			var download_list = response_data;
			$('#plotArea').show();
			document.getElementById("plotArea").innerHTML = download_list;

		},
		error : function(xhr, status, error) {
			console.log('error');
			if (EA.spinnerFlag) {
				$body.removeClass("loading");
			}
			if (xhr.status == 404) {

			}
		}
	});

}

function downloadPlot() {
	html = '<div class="pull-left">';
	html += '<a href="#" onclick=\"displayImageClick(\'' + lastURL + '\')\"><< Back</a>';
	html += '<br><br>';
	html += '<iframe src=\"' + lastURL + '\" width=150px height=150px syle="overflow:none"><br></iframe>';
	html += '<span><h3>Downloads</h3></span><hr>';
	html += '<a href=\"' + lastURL + '\" download="" target="_blank">png (right-click save as)</a>';
	html += '<br>';
	/*
	 html += '<br>';
	 html += '<a download="" target="_blank">xml</a>';
	 html += '<br>';
	 html += '<a download="" target="_blank">json</a>';
	 html += '<br>';
	 */

	var split = lastURL.split('/');

	split = split[split.length - 1];
	split = split.substring(0, split.length - 3);
	split = split + 'netcdf';
	console.log('split = ' + split);
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/cdflink/' + dataset + '/' + pckg + '/' + split + '/null';

	$.ajax({
		type : "GET",
		url : url,
		dataType : 'text',
		//async: false,
		//data: data,
		success : function(response_data) {

			console.log('success in getting downloadlist');

			var download_link = response_data;
			html += '<a href=\"' + download_link + '\">netcdf</a>';
			html += '<br>';
			document.getElementById("plotArea").innerHTML = html;
		},
		error : function(xhr, status, error) {
			console.log(error + xhr + status);
			if (EA.spinnerFlag) {
				$body.removeClass("loading");
			}
			if (xhr.status == 404) {

			}
		}
	});

	document.getElementById("plotArea").innerHTML = html;

}

function create_download_list() {
	var dataset = 'null';
	// $('#selectD').val();
	var pckg = $('#selectP').val();
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/downloadlist/' + dataset + '/' + pckg + '/null/null';

	$.ajax({
		type : "GET",
		url : url,
		dataType : 'json',
		//async: false,
		//data: data,
		success : function(response_data) {

			console.log('success in getting downloadlist');

			var download_list = response_data['file_list'];

		},
		error : function(xhr, status, error) {
			console.log('error');
			if (EA.spinnerFlag) {
				$body.removeClass("loading");
			}
			if (xhr.status == 404) {

			}
		}
	});
}
