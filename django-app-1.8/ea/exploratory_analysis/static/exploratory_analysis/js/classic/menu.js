$(document).ready(function() {
	
	var current_username = $('#username_posted').html();
	
	EA_MENU.functions.getGroups(current_username);

	EA_MENU.functions.getDatasets(current_username);
	
	EA_MENU.functions.getPackages(current_username);
	
	
	//Next button event
	//console.log('next button');
	$('button#dataset_selected').click(function() {
		$('#next_options').show();
		
		var dataset_chosen = $('#selectD').val();
		
		EA_MENU.functions.getVariables(dataset_chosen);
		
		EA_MENU.functions.getTimes(dataset_chosen);
		
	});
	
	
	/* Insert change calls here
	$('#selectP').change(function() {
		alert('changing P... issue call for ');
		
		
	});
	*/
});




var EA_MENU = EA_MENU || {};

EA_MENU.namespace = function(ns_string) {
	var parts = ns_string.split('.'),
		parent = EA_MENU,
		i;
	
	//strip redundant leading global
	if (parts[0] === 'EA_MENU') {
		parts = parts.slice(1);
	}
	
	for(i=0;i<parts.length;i++) {
		// create a property if it doesn't exist
		if (typeof parent[parts[i]] === 'undefined') {
			parent[parts[i]] = {};
		}
		parent = parent[parts[i]];
	}
	return parent;
	
};


EA_MENU.namespace('EA_MENU.functions');


EA_MENU.functions = (function() {
	
	return {
		//todo
		echo: function(word) {
			return word + ' echo';
		},
		
		makeMenuSelection: function(element,data_list,header,multiple) {
			$(element).multiselect({
				multiple : multiple,
				minWidth : 195,
				header : header
				//noneSelectedText : "tropics_warming_th_q_co2",
			});
			d3.select(element).selectAll("option").data(data_list).enter().append("option").attr("value", String).text(String);
			$(element).multiselect("refresh");

		},
		
		getGroups: function(username) {
			
			/*
			var dataList = ["ACME"];
			
			$("#select_Project").multiselect().multiselectfilter();

			$("#select_Project").multiselect({
				minWidth : 195,
				multiple : false,
				header : "Select a dataset",
				noneSelectedText : "tropics_warming_th_q_co2",
				selectedList : 1
			});
			*/
			
			
			var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/groups/' + username;
			
			
			//for now, use only ACME group, but this should be extended
			var data_list = EA.default_groups;//["ACME"];
			
			EA_MENU.functions.makeMenuSelection("#select_Project",data_list,'select a dataset',false);
			
			//disable other selections (for now)
			$("#select_Project").multiselect('disable');
			
			
		},
		
		

		
		getDatasets: function(username) {
			var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/dataset_access/' + 'ACME';//username;
			
			console.log('url get datasets-->' + url);
			  
			var data_list = EA.default_datasets;

			//need to get the data list from a service
			$.ajax({
				  type: "GET",
				  url: url,
				  success: function(response_data)
				  {
					  console.log('success ' + response_data);
					  
					  EA_MENU.functions.makeMenuSelection("#selectD",data_list,'select a dataset',false);
					
				  },
				  error: function() {
					  console.log('error');

					  //need to get the default data list 
					  
					  EA_MENU.functions.makeMenuSelection("#selectD",data_list,'select a dataset',false);
					  
					  
				  }
			});
		},
		
		getMenuItem: function(menu_item_id) {
			return $(menu_item_id).val();
		},
		
		
		getPackages: function(username) {
			var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/dataset_packages/' + 'ACME';//username;
			//http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$
			console.log('url get datasets-->' + url);
			  
			var data_list = EA.default_packages;
			EA_MENU.functions.makeMenuSelection("#selectP",data_list,'select a package',false);
			//need to get the data list from a service
			
			
		},
		
		
		getVariables: function(dataset_chosen) {
			
			var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/variables/' + dataset_chosen;//username;
			
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
					  
					  EA_MENU.functions.makeMenuSelection("#selectV",data_list,'select variables',true);
					
				  },
				  error: function() {
					  console.log('error');

					  //need to get the default data list 
					  
					  EA_MENU.functions.makeMenuSelection("#selectV",data_list,'select variables',true);
					  
					  
				  }
			});
			
		},
		
		getTimes: function(dataset_chosen) {

			
			//for now, just use the default list
			var data_list = EA.default_times;

			console.log('data_list: ' + data_list);
			EA_MENU.functions.makeMenuSelection("#selectT",data_list,'select times',true);
			
			
		}


		
		
	};
	
})();



/*
function getMenuItem(menu_item_id) {
	return $(menu_item_id).val();
}


function getGroups(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/groups/' + username;
	
	
	//for now, use only ACME group, but this should be extended
	var data_list = EA.default_groups;//["ACME"];
	
	makeMenuSelection("#select_Project",data_list,'select a dataset',false);
	
	//disable other selections (for now)
	$("#select_Project").multiselect('disable');
	
}



function getDatasets(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/dataset_access/' + 'ACME';//username;
	
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
	var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/dataset_packages/' + 'ACME';//username;
	//http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$
	console.log('url get datasets-->' + url);
	  
	var data_list = EA.default_packages;
	makeMenuSelection("#selectP",data_list,'select a package',false);
	//need to get the data list from a service
	
	
}


function getVariables(dataset_chosen) {
	
	var url = 'http://' + EA.host + ':' + EA.port + '/ea_services/variables/' + dataset_chosen;//username;
	
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

*/





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


