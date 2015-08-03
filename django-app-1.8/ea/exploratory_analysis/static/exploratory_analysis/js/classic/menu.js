$(document).ready(function() {
	
	var current_username = $('#username_posted').html();
	
	getGroups(current_username);
	
	console.log('getting datasets');

	getDatasets(current_username);
	
	getPackages(current_username);
	
	$('button#dataset_selected').click(function() {
		console.log('next button');
		$('#next_options').show();
		
		var dataset_chosen = $('#selectD').val();
		console.log('dataset_chosen: ' + dataset_chosen);
		
		getVariables(dataset_chosen);
		
		getTimes(dataset_chosen);
		
	});
	
	
});


function getMenuItem(menu_item_id) {
	return $(menu_item_id).val();
}


function getGroups(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/groups/' + username;
	
	
	//for now, use only ACME group, but this should be extended
	var data_list = EA.default_groups;//["ACME"];
	
	makeMenuSelection("#select_Project",data_list,'select a dataset',false);
	
	//disable other selections (for now)
	$("#select_Project").multiselect('disable');
	
}



function getDatasets(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/dataset_access/' + 'ACME';//username;
	
	console.log('url get datasets-->' + url);
	  
	var data_list = EA.default_datasets;

	//need to get the data list from a service
	$.ajax({
		  type: "GET",
		  url: url,
		  success: function(response_data)
		  {
			  console.log('success ' + response_data);
			  
			  makeMenuSelection("#selectD",data_list,'select a dataset',false);
			
		  },
		  error: function() {
			  console.log('error');

			  //need to get the default data list 
			  
			  makeMenuSelection("#selectD",data_list,'select a dataset',false);
			  
			  
		  }
	});
}


function getPackages(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/dataset_packages/' + 'ACME';//username;
	//http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$
	console.log('url get datasets-->' + url);
	  
	var data_list = EA.default_packages;
	makeMenuSelection("#selectP",data_list,'select a package',false);
	//need to get the data list from a service
	/*
	$.ajax({
		  type: "GET",
		  url: url,
		  success: function(response_data)
		  {
			  console.log('success ' + response_data);
			  
			  makeMenuSelection("#selectD",data_list,'select a dataset',false);
			
		  },
		  error: function() {
			  console.log('error');

			  //need to get the default data list 
			  
			  makeMenuSelection("#selectD",data_list,'select a dataset',false);
			  
			  
		  }
	});
	*/
	
}


function getVariables(dataset_chosen) {
	
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/variables/' + dataset_chosen;//username;
	
	console.log('url get datasets-->' + url);
	  
	var data_list = EA.default_variables;

	//need to get the data list from a service
	$.ajax({
		  type: "GET",
		  url: url,
		  success: function(response_data)
		  {
			  console.log('success ' + response_data);
			  
			  var response_data_json = JSON.parse(response_data)
			  
			  if(response_data_json['variables'] == '') {
				  data_list = EA.default_variables;
			  } else {
				  data_list = response_data_json['variables'];
			  }
			  
			  makeMenuSelection("#selectV",data_list,'select variables',true);
			
		  },
		  error: function() {
			  console.log('error');

			  //need to get the default data list 
			  
			  makeMenuSelection("#selectV",data_list,'select variables',true);
			  
			  
		  }
	});
	
}

function getTimes(dataset_chosen) {

	
	//for now, just use the default list
	var data_list = EA.default_times;

	console.log('data_list: ' + data_list);
	makeMenuSelection("#selectT",data_list,'select times',true);
	
	
}



function makeMenuSelection(element,data_list,header,multiple) {
	$(element).multiselect({
		multiple : multiple,
		minWidth : 195,
		header : header,
		//noneSelectedText : "tropics_warming_th_q_co2",
		selectedList : 1
	});
	d3.select(element).selectAll("option").data(data_list).enter().append("option").attr("value", String).text(String);
	$(element).multiselect("refresh");

}

var dataList = ["ACME"];
$("#select_Project").multiselect().multiselectfilter();

$("#select_Project").multiselect({
	minWidth : 195,
	multiple : false,
	header : "Select a dataset",
	//noneSelectedText : "tropics_warming_th_q_co2",
	selectedList : 1
});






/*
$("#select_Project").multiselect().multiselectfilter();

$("#select_Project").multiselect({
	minWidth : 195,
	multiple : false,
	header : "Select a group",
	//noneSelectedText : "",
	selectedList : 1
});

d3.select("#select_Project").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);

$("#select_Project").multiselect("refresh");
*/


/*
$("#selectD").multiselect().multiselectfilter();
	
$("#selectD").multiselect({
		multiple : false,
		header : "Select a dataset",
		//noneSelectedText : "tropics_warming_th_q_co2",
		selectedList : 1
});
d3.select("#selectD").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);
$("#selectD").multiselect("refresh");
 */


/*
$("#selectD").multiselect().multiselectfilter();
	
$("#selectD").multiselect({
		multiple : false,
		header : "Select a dataset",
		//noneSelectedText : "tropics_warming_th_q_co2",
		selectedList : 1
});
d3.select("#selectD").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);
$("#selectD").multiselect("refresh");
*/


