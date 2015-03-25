$(document).ready(function() {
	$body = $("body");

	console.log('get the user name here ' + document.URL);
	//var current_username = getUsernameFromURL(document.URL)

	var current_username = $('#username_posted').html();
	//var current_username = 'jfhCSSEF';
	console.log('current_username: ' + current_username);

	getDatasets(current_username);

	getPackages(current_username);

	//getVariables(current_username);

	//getTimes(current_username);

	var treeloaded = $('#treeloaded').html();

	//for post requests, need to get the csrf token
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	if (treeloaded == 'false')
		$('#dataviewer').hide();

	$('#test').click(function() {

		console.log('csrftoken in test ' + csrftoken);

		var data = {
			'csrfmiddlewaretoken' : csrftoken
		};
		var fileUrl = 'http://localhost:8081/exploratory_analysis/test/';
		$.ajax({
			type : "POST",
			url : fileUrl,
			async : false,
			data : data,
			success : function() {
				console.log('success');
			},
			error : function(xhr, status, error) {
				console.log('error');
				if (xhr.status == 404) {

				}
			}
		});

	});

	//clear the page upon load
	//clear_page();

	//alert('loading classic.js');
	$('.classic_figure_sets').click(function() {

		var index = this.id.search('_');

		var set = this.id.substring(index + 1);

		toggle_vis(set);

	});

	$('.classic_toggle_sets').click(function() {

		var index = this.id.search('_');

		var set = this.id.substring(index + 1);

		//console.log('this.id: ' + this.id);

		toggle_vis(set);

	});

	$('#selectD').on('change', function() {

		var pckg = $('#selectP').val();

		//make amwg home button appear
		hide_land_home();
		$('#go_Atm_Home_Button').hide();

		//make lmwg home button disappear
		$('#go_Land_Home_Button').hide();
		hide_atm_home();

		hide_land_sets();
		hide_atm_sets();

		//hide variable and time selections and display next button
		hide_varSelect();

	});
	$('#save_tree').click(function() {
		var dataset = $('#selectD').val();
		var pckg = $('#selectP').val();

		var pckg = $('#selectP').val();

		//create_download_list();

		if (pckg == 'lmwg') {

			//make lmwg home button appear
			$('#go_Land_Home_Button').show();

			//make amwg home button disappear
			$('#go_Atm_Home_Button').hide();

			//make lmwg home appear

			go_Land_Home();

		} else {

			//make amwg home button appear
			$('#go_Atm_Home_Button').show();

			//make lmwg home button disappear
			$('#go_Land_Home_Button').hide();

			//make atm home appear
			toggle_set_list();
			go_Atm_Home();

		}
	});
	$('#selectP').on('change', function() {

		var pckg = $('#selectP').val();

		//make amwg home button appear
		hide_land_home();
		$('#go_Atm_Home_Button').hide();

		//make lmwg home button disappear
		$('#go_Land_Home_Button').hide();
		hide_atm_home();

		//hide variable and time selections and display next button
		hide_varSelect();

		hide_land_sets();
		hide_atm_sets();
	});
});

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

function go_publish() {
	
	
	//these are all the options for the different facets
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/base_facets/jfharney';
	
	var response_data = {};
	//default values here
	response_data['project'] = ['ACME']
	response_data['data_type'] = ['climo','dd','dt','dv','h','h0','h1','h2','h3','h4'];
	response_data['realm'] = ['atm','ice','lnd','ocn','all','ATM'];
	response_data['regridding'] = ['bilinear','downscaled,native','fv257x512','ne30_g16','T341_f02_t12'];
	response_data['range'] = ['all_dir','all','2-9','10-19','20-29','30-39','30-50','40-49','ALL'];
	response_data['versionnum'] = ['v0_0','v0_1','v01','HIGHRES','pre-v0'];
	response_data['experiment'] = ['B1850C5_ne30gx1_tuning','341f02.B1850dEdd','B1850C5e1_ne30'];
	
	$.ajax({
		type : "GET",
		url : url,
		dataType : 'text',
		async: false,
		//data: data,
		success : function(data) {
			alert('success in extracting facets');
			
		},
		error: function() {
			alert('error in extracting facets');
			
		}
	});
	
	for (var key in response_data) {
		console.log( 'key: ' + key + ' value: ' + response_data[key]);
	}
	
	document.getElementById("plotArea").style.visibility = 'visible';

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
	//$inner = $('<div class="span8" id="info_pane">fff</div>');
	//$inner = $('<select id="selectF0" multiple="multiple"></select>')
	
	var inner_html = "<hr>";

	inner_html += '<label for="selectF1">Project:</label>';
	inner_html += '<br>';
	
	inner_html += '<select id="selectF1" multiple="multiple">';
	for (var i=0;i<response_data['project'].length;i++) {
		inner_html += '<option value="' + response_data['project'][i] + '">' + response_data['project'][i] + '</option>'; 
	}
	inner_html += '</select>';
	
	inner_html += "<br>";
	
	inner_html += '<label for="selectF2">Data Type:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF2" multiple="multiple">';
	for (var i=0;i<response_data['data_type'].length;i++) {
		inner_html += '<option value="' + response_data['data_type'][i] + '">' + response_data['data_type'][i] + '</option>'; 
	}
	inner_html += '</select>';
	
	inner_html += "<br>";
	
	inner_html += '<label for="selectF3">Experiment:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF3" multiple="multiple">';
	for (var i=0;i<response_data['experiment'].length;i++) {
		inner_html += '<option value="' + response_data['experiment'][i] + '">' + response_data['experiment'][i] + '</option>'; 
	}
	inner_html += '</select>';
	
	inner_html += "<br>";
	
	inner_html += '<label for="selectF4">Version:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF4" multiple="multiple">';
	for (var i=0;i<response_data['versionnum'].length;i++) {
		inner_html += '<option value="' + response_data['versionnum'][i] + '">' + response_data['versionnum'][i] + '</option>'; 
	}
	inner_html += '</select>';
	
	
	inner_html += "<br>";
	
	inner_html += '<label for="selectF5">Range:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF5" multiple="multiple">';
	for (var i=0;i<response_data['range'].length;i++) {
		inner_html += '<option value="' + response_data['range'][i] + '">' + response_data['range'][i] + '</option>'; 
	}
	inner_html += '</select>';
	
	
	
	inner_html += "<br>";
	
	
	inner_html += '<label for="selectF6">Realm:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF6" multiple="multiple">';
	for (var i=0;i<response_data['realm'].length;i++) {
			inner_html += '<option value="' + response_data['realm'][i] + '">' + response_data['realm'][i] + '</option>'; 
	}		
	inner_html += '</select>';	
	
	inner_html += "<br>";
	inner_html += '<label for="selectF7">Regridding:</label>';
	inner_html += '<br>';
	inner_html += '<select id="selectF7" multiple="multiple" style="margin-bottom:20px;">';
	for (var i=0;i<response_data['regridding'].length;i++) {
		inner_html += '<option value="' + response_data['regridding'][i] + '">' + response_data['regridding'][i] + '</option>'; 
	}		
	inner_html += '</select>';	
	
	
	inner_html += '<button type="button" class="btn btn-default" id="dataset_selected" onclick="publish()">';
	inner_html + 'Publish';
	inner_html += '</button>';
	
	$('#plotArea').show();
	document.getElementById("plotArea").innerHTML = inner_html;
	
	
	
	
}


function publish() {
	
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/publish/jfharney/';

	var project = $('#selectF1').val();
	var data_type = $('#selectF2').val();
	var experiment = $('#selectF3').val();
	var version = $('#selectF4').val();
	var range = $('#selectF5').val();
	var realm = $('#selectF6').val();
	var regridding = $('#selectF7').val();

	
	
	var data = {
		'project' : project,
		'data_type' : data_type,
		'experiment' : experiment,
		'version' : version,
		'range' : range,
		'realm' : realm,
		'regridding' : regridding
	};
	
	
	$.ajax({
		type : "POST",
		url : url,
		//dataType : 'text',
		async: false,
		data: data,
		success : function(data) {
			alert('success ' + data);
			
		},
		error: function() {
			alert('error');
			
		}
	});
	
	
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

function downloadPlot() {
	html = '<div class="pull-left">';
	html += '<a href="#" onclick=\"displayImageClick(\'' + lastURL + '\')\"><< Back</a>';
	html += '<br><br>';
	html += '<iframe src=\"' + lastURL + '\" width=150px height=150px syle="overflow:none"><br></iframe>';
	html += '<span><h3>Downloads</h3></span><hr>';
	html += '<a href=\"' + lastURL + '\" download="" target="_blank">png (right-click save as)</a>';
	/*
	 html += '<br>';
	 html += '<a download="" target="_blank">xml</a>';
	 html += '<br>';
	 html += '<a download="" target="_blank">json</a>';
	 html += '<br>';
	 */

	document.getElementById("plotArea").innerHTML = html;
}

function expandPlot() {
	window.open(lastURL);
}

function nodisplayImage() {
	if (clicked != 1) {
		document.getElementById("plotArea").style.visibility = 'hidden';
	}
}

function toggle_varSelect() {
	var dataset = $('#selectD').val();

	$('#dataset_selected').hide();
	$('#variables_div').show();
	getVariables('ul');
}

function hide_varSelect() {
	var dataset = $('#selectD').val();

	$('#dataset_selected').show();
	$('#variables_div').hide();
	getVariables('ul');
}

function toggle_set_list() {

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();

	var pckg = $('#selectP').val();

	if (pckg == 'lmwg') {

		//make lmwg home button appear
		$('#go_Land_Home_Button').show();

		//make amwg home button disappear
		$('#go_Atm_Home_Button').hide();

		//make lmwg home appear
		go_Land_Home();

	} else {

		//make amwg home button appear
		$('#go_Atm_Home_Button').show();

		//make lmwg home button disappear
		$('#go_Land_Home_Button').hide();

		//make atm home appear
		go_Atm_Home();

	}

	//make some defaults for testing
	//TODO: replace or just dump this
	//if(dataset == null && pckg == 'lmwg') dataset = 'tropics_warming_th_q';
	//else if(dataset == null) dataset = 'f40_amip_cam5_c03_78b';

	//document.getElementById('landHome').style.display = 'none';
	hide_land_home();
	hide_atm_home();

	var variable_arr = $("#selectV").val();

	//it is possible that the variable_arr can be null (if none are selected)
	//in that case, let the default be ALL variables
	if (variable_arr == null) {
		variable_arr = new Array();
		//NOTE: come back and push all variables onto the array
		variable_arr.push('TLAI');
	}

	//it is possible that the season_arr can be null (if none are selected)
	//in that case, let the default be ALL variables
	var season_arr = $('#selectT').val();
	if (season_arr == null) {
		season_arr = new Array();
		season_arr.push('JAN');
	}

	var varsData = variable_arr;
	//["var1","var2"];
	var timesData = season_arr;
	//timesData;
	var packageData = pckg;
	//"package1";
	var datasetData = dataset;

	var data = {

		"vars" : varsData,
		"times" : timesData,
		"package" : packageData,
		"dataset" : datasetData

	};

	var url = '/exploratory_analysis/classic_set_list_html/' + '?_=' + Math.round(Math.random() * 10000);

	$.ajax({
		type : "POST",
		url : url,
		cache : false,
		data : JSON.stringify(data),
		//async : false,
		success : function(html) {
			console.log(html);
			$('#atmHome').append(html);
			$('.classic_toggle_sets').click(function() {

				var index = this.id.search('_');

				var set = this.id.substring(index + 1);

				//console.log('this.id: ' + this.id);

				toggle_vis(set);

			});

		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});

}

function toggle_vis(set) {

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();

	var pckg = $('#selectP').val();

	if (pckg == 'lmwg') {

		//make lmwg home button appear
		$('#go_Land_Home_Button').show();

		//make amwg home button disappear
		$('#go_Atm_Home_Button').hide();

		//make lmwg home appear
		go_Land_Home();

	} else {

		//make amwg home button appear
		$('#go_Atm_Home_Button').show();

		//make lmwg home button disappear
		$('#go_Land_Home_Button').hide();

		//make atm home appear
		go_Atm_Home();

	}

	//make some defaults for testing
	//TODO: replace or just dump this
	//if(dataset == null && pckg == 'lmwg') dataset = 'tropics_warming_th_q';
	//else if(dataset == null) dataset = 'f40_amip_cam5_c03_78b';

	//document.getElementById('landHome').style.display = 'none';
	hide_land_home();
	hide_atm_home();

	var variable_arr = $("#selectV").val();

	//it is possible that the variable_arr can be null (if none are selected)
	//in that case, let the default be ALL variables
	if (variable_arr == null) {
		variable_arr = new Array();
		//NOTE: come back and push all variables onto the array
		variable_arr.push('TLAI');
	}

	//it is possible that the season_arr can be null (if none are selected)
	//in that case, let the default be ALL variables
	var season_arr = $('#selectT').val();
	if (season_arr == null) {
		season_arr = new Array();
		season_arr.push('JAN');
	}

	var setData = set;
	var varsData = variable_arr;
	//["var1","var2"];
	var timesData = season_arr;
	//timesData;
	var packageData = pckg;
	//"package1";
	var datasetData = dataset;

	var data = {

		"set" : setData,
		"vars" : varsData,
		"times" : timesData,
		"package" : packageData,
		"dataset" : datasetData

	};

	var url = '/exploratory_analysis/classic_views_html/' + '?_=' + Math.round(Math.random() * 10000);

	$.ajax({
		type : "POST",
		url : url,
		cache : false,
		data : JSON.stringify(data),
		//async : false,
		success : function(html) {
			console.log(html);
			var html_elem_id = packageData + '_' + setData + '_html';

			$('#' + html_elem_id).empty();
			$('#' + html_elem_id).append(html);
			document.getElementById(html_elem_id).style.display = 'block';
			console.log(html_elem_id);
		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});

}

function go_Atm_Home() {
	document.getElementById('atmHome').style.display = 'block';

	hide_land_home();
	hide_land_sets();
	hide_atm_sets();

}

function go_Land_Home() {

	document.getElementById('landHome').style.display = 'block';

	hide_atm_home();
	hide_land_sets();
	hide_atm_sets();

}

function hide_land_sets() {

	document.getElementById('lmwg_set1_html').style.display = 'none';
	document.getElementById('lmwg_set2_html').style.display = 'none';
	document.getElementById('lmwg_set3_html').style.display = 'none';
	document.getElementById('lmwg_set5_html').style.display = 'none';
	document.getElementById('lmwg_set6_html').style.display = 'none';
	document.getElementById('lmwg_set7_html').style.display = 'none';
	document.getElementById('lmwg_set9_html').style.display = 'none';

}

function hide_atm_sets() {

	document.getElementById('amwg_topten_html').style.display = 'none';
	document.getElementById('amwg_set1_html').style.display = 'none';
	document.getElementById('amwg_set2_html').style.display = 'none';
	document.getElementById('amwg_set3_html').style.display = 'none';
	document.getElementById('amwg_set4_html').style.display = 'none';
	document.getElementById('amwg_set4a_html').style.display = 'none';
	document.getElementById('amwg_set5_html').style.display = 'none';
	document.getElementById('amwg_set6_html').style.display = 'none';
	document.getElementById('amwg_set7_html').style.display = 'none';
	document.getElementById('amwg_set8_html').style.display = 'none';
	document.getElementById('amwg_set9_html').style.display = 'none';
	document.getElementById('amwg_set10_html').style.display = 'none';
	document.getElementById('amwg_set11_html').style.display = 'none';
	document.getElementById('amwg_set12_html').style.display = 'none';
	document.getElementById('amwg_set13_html').style.display = 'none';
	document.getElementById('amwg_set14_html').style.display = 'none';
	document.getElementById('amwg_set15_html').style.display = 'none';
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

function hide_land_home() {
	document.getElementById('landHome').style.display = 'none';
}

function hide_atm_home() {
	document.getElementById('atmHome').style.display = 'none';
}
