function checkRole(userID) {

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/has_publish_role/' + userID;

	$.ajax({
		type : "GET",
		url : url,
		dataType : 'text',

		success : function(response_data) {

			if (response_data != "true") {
				//hide link
				$('#publish_link').hide();
			}

		},
		error : function(xhr, status, error) {
			console.log(error);
		}
	});

}

function get_publish_status() {
	var dataset = $('#selectD').val();
	console.log('dataset: ' + dataset);
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/dataset_published/' + dataset;
	$.ajax({
		type : "GET",
		url : url,
		async : false,
		contentType : "application/json",
		success : function(response_data) {
			var data = JSON.parse(response_data);
			if (data.published == "" || data.published == "unpublished")
				generate_publish_ui();
			else {
				document.getElementById("plotArea").style.visibility = 'visible';
				document.getElementById("plotArea").innerHTML = "";
				var innerHTML = '<font color=blue><h2>' + dataset + '</h2></font>';
				innerHTML += '<h5>Publising Process in Progress<h5><br>';
				innerHTML += '<h3>Status: <font color=blue>' + data.published + '</h3>';

				$('#plotArea').show();
				document.getElementById("plotArea").innerHTML = innerHTML;

			}

		},
		error : function() {
			alert('error');

		}
	});

}

function generate_publish_ui() {

	//these are all the options for the different facets
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/base_facets/jfharney';

	//set to default values here (just in case)
	var response_data = EA.default_facet_list;

	document.getElementById("plotArea").innerHTML = "";

	console.log('url: ' + url);
	$.ajax({
		type : "GET",
		url : url,
		//dataType : 'json',

		success : function(data) {

			data = JSON.parse(data);
			console.log('success in extracting facets');

			//set response data to the data returned by the service
			//response_data = data;

			//set the publish form to visible
			document.getElementById("plotArea").style.visibility = 'visible';

			//$inner = $('<div class="span8" id="info_pane">fff</div>');

			$inner = $('<div><div>');
			//$inner.append('<hr>');
			for (var i = 0; i < response_data.length; i++) {
				//for (var facet_key in response_data) {
				var facet = response_data[i];
				for (var key in facet) {
					//console.log('\t\tkey: ' + key + ' value: ' + facet[key] + ' length: ' + facet[key].length);
					$inner.append('<label for="selectF0" class="pull-left">' + key + ':</label>');
					$inner.append('<br>');
					var facet_value_arr = facet[key].split(',');
					$select = $('<select  id="selectF' + i + '" class = "pull-left"></select>');
					for (var facet_value in facet_value_arr) {
						//console.log('\t\t\t' + facet_value_arr[facet_value]);
						$select.append('<option value="' + facet_value_arr[facet_value] + '">' + facet_value_arr[facet_value] + '</option>');
					}
					$inner.append($select);
					$inner.append('<br>');

				}
			}

			$inner.append('<button type="button" class="btn btn-default" onclick="publish_button()">Publish</button>');

			$('#plotArea').show();
			//document.getElementById("plotArea").innerHTML = inner_html;

			$('#plotArea').append($inner);

			for (var i = 0; i < response_data.length; i++) {
				//console.log('\t\tkey: ' + key + ' value: ' + facet[key] + ' length: ' + facet[key].length);

				$('#selectF' + i).multiselect().multiselectfilter();

				$("#selectF" + i).multiselect({
					minWidth : 195,
					multiple : false,
					header : "Select an option",
					selectedList : 1
				});

				$("#selectF" + i).multiselect("refresh");

			}

		},
		error : function(xhr, err) {

			console.log("in error for generate publish ui")
			//set response data to the data returned by the service
			//response_data = data;

			//set the publish form to visible
			document.getElementById("plotArea").style.visibility = 'visible';

			//$inner = $('<div class="span8" id="info_pane">fff</div>');

			$inner = $('<div>');
			//$inner.append('<hr>');
			for (var i = 0; i < response_data.length; i++) {
				//for (var facet_key in response_data) {
				var facet = response_data[i];
				for (var key in facet) {
					//console.log('\t\tkey: ' + key + ' value: ' + facet[key] + ' length: ' + facet[key].length);
					$inner.append('<label for="selectF0" class="pull-left">' + key + ':</label>');
					$inner.append('<br><br>');
					var facet_value_arr = facet[key].split(',');
					$select = $('<select  id="selectF' + i + '" class = "pull-left"></select>');
					for (var facet_value in facet_value_arr) {
						//console.log('\t\t\t' + facet_value_arr[facet_value]);
						$select.append('<option value="' + facet_value_arr[facet_value] + '">' + facet_value_arr[facet_value] + '</option>');
					}
					$inner.append($select);
					$inner.append('<br><br>');

				}
			}

			$inner.append('<br><button type="button" class="btn btn-default pull-left" onclick="publish_button()">Publish</button><br>');

			$('#plotArea').show();
			//document.getElementById("plotArea").innerHTML = inner_html;

			$('#plotArea').append($inner);
			for (var i = 0; i < response_data.length; i++) {
				//console.log('\t\tkey: ' + key + ' value: ' + facet[key] + ' length: ' + facet[key].length);

				$('#selectF' + i).multiselect().multiselectfilter();

				$("#selectF" + i).multiselect({
					minWidth : 195,
					multiple : false,
					header : "Select an option",
					selectedList : 1
				});

				$("#selectF" + i).multiselect("refresh");
			}
		}
	});

}

function publish_button() {

	console.log('in publish button');

	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/publish/jfharney/';

	var project = $('#selectF0').val();
	var data_type = $('#selectF1').val();
	var experiment = $('#selectF2').val();
	var version = $('#selectF3').val();
	var range = $('#selectF4').val();
	var realm = $('#selectF5').val();
	var regridding = $('#selectF6').val();

	console.log('project: ' + project);
	console.log('data_type: ' + data_type);
	console.log('experiment: ' + experiment);

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
		async : false,
		contentType : "application/json",
		data : JSON.stringify(data),
		success : function(response_data) {
			//alert('success ' + response_data);
			console.log('success: ' + response_data);
			var current_username = $('#username_posted').html();
			//setTimeout(checkRole(current_username), 100);
			var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/dataset_published/' + $('#selectD').val() + '/';
			var status = {
				"published" : "pending"
			};
			$.ajax({
				type : "POST",
				url : url,
				async : false,
				contentType : "application/json",
				data : JSON.stringify(status),
				success : function(response_data) {
					//alert('success ' + response_data);
					console.log('success: ' + response_data);
					var current_username = $('#username_posted').html();
					get_publish_status();
				},
				error : function() {
					alert('error');

				}
			});
		},
		error : function() {
			alert('error');

		}
	});

}

function publish() {

	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/publish/jfharney/';

	var project = $('#selectF0').val();
	var data_type = $('#selectF1').val();
	var experiment = $('#selectF2').val();
	var version = $('#selectF3').val();
	var range = $('#selectF4').val();
	var realm = $('#selectF5').val();
	var regridding = $('#selectF6').val();

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
		async : false,
		data : data,
		success : function(data) {
			alert('success ' + data);

		},
		error : function() {
			alert('error');

		}
	});

}