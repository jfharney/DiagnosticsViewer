$(document).ready(function() {
	$body = $("body");

	console.log('get the user name here ' + document.URL);
	//var current_username = getUsernameFromURL(document.URL)

	var current_username = $('#username_posted').html();
	//var current_username = 'jfhCSSEF';
	console.log('current_username: ' + current_username);

	var dataList = ["ACME"];
	$("#select_Project").multiselect().multiselectfilter();

	$("#select_Project").multiselect({
		minWidth : 195,
		multiple : false,
		header : "Select a dataset",
		//noneSelectedText : "tropics_warming_th_q_co2",
		selectedList : 1
	});

	d3.select("#select_Project").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);

	$("#select_Project").multiselect("refresh");
	$("#select_Project").multiselect('disable');

	getDatasets(current_username);

	getPackages(current_username);

	checkRole(current_username);
	//getVariables(current_username);

	//getTimes(current_username);

	//var treeloaded = $('#treeloaded').html();

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

	$('#publish_button').on('click', function() {
		console.log('publishing...');
	});

});

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

			$('#atmHome').empty();
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
	document.getElementById('atmHome').innerHTML = "";
	document.getElementById('landHome').innerHTML = "";
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
	document.getElementById('amwg_tier1b_html').style.display = 'none';
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

function hide_land_home() {
	document.getElementById('landHome').style.display = 'none';
}

function hide_atm_home() {
	document.getElementById('atmHome').style.display = 'none';
}

