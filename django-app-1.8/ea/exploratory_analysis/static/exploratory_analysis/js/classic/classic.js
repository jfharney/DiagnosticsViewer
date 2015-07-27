$(document).ready(function() {

	$('#go_Land_Home_Button').click(function(){
		load_diags_homepage();
	});
	
	$('#go_Atm_Home_Button').click(function(){
		load_diags_homepage();
	});
	
	$('button#plots').click(function() {
		
		load_diags_homepage();
		
	});
	
	
});


function showButton(pckg) {
	if(pckg == 'lnd') {
		//hide atm button
		$('#go_Atm_Home_Button').hide();
		
		//show land button
		$('#go_Land_Home_Button').show();
	} else {
		//show atm button
		$('#go_Atm_Home_Button').show();
		
		//hide all other buttons
		$('#go_Land_Home_Button').hide();
	}
	
}



function load_diags_homepage() {
	
	//alert('run diags');
	
	var project = getMenuItem('#select_Project');
	var dataset = getMenuItem('#selectD');
	var pckg = getMenuItem('#selectP');
	var variables = getMenuItem('#selectV');
	var times = getMenuItem('#selectT');
	
	console.log('project: ' + project);
	console.log('dataset: ' + dataset);
	console.log('pckg: ' + pckg);
	console.log('variables: ' + variables);
	console.log('times: ' + times);
	/*
	var data = {
			"project" : project,
			"dataset" : dataset,
			"pckg" : pckg,
			"variables" : variables,
			"times" : times
		};
	*/
	
	showButton(pckg);
	
	if (pckg == null) {
		pckg = 'atm';
	}
	
	
	var url = '/exploratory_analysis/classic_set_list_html?package=' + pckg; // + '?_=' + Math.round(Math.random() * 10000);

	
	$.ajax({
		type : "GET",
		url : url,
		cache : false,
		success : function(html) {
			
			//console.log('appending ' + html);
			
			$('#landHome').empty();
			$('#atmHome').empty();
			if (pckg == 'lnd') {
				$('#landHome').append(html);
			} else {
				$('#atmHome').append(html);
			}
			
			
			//console.log('home: ' + $('#atmHome').html())
			
			$('.classic_toggle_sets').click(function() {

				
				
				console.log('id: ' + this.id);
				
				var set = transformClassicLinkNames(this.id);

				
				load_sets_homepage(pckg,set);
				
				
				
				/*
				var index = this.id.search('_');

				var set = this.id.substring(index + 1);
				

				//alert('classic toggle sets ' + set);
				
				load_sets_homepage(pckg,set);
				*/
				
				/*
				//console.log('this.id: ' + this.id);

				toggle_vis(set);
				*/
			});
			

		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});
	
}


//amwgmaster map is looking for:
//topten,so,1,2,3,4,4a,5,6,7,8,9,10,11,12,13,14,15

function transformClassicLinkNames(link_name) {
	
	if (link_name.search('15') > -1) {
		link_name = '15';
	} else if (link_name.search('14') > -1) {
		link_name = '14';
	} else if (link_name.search('13') > -1) {
		link_name = '13';
	} else if (link_name.search('12') > -1) {
		link_name = '12';
	} else if (link_name.search('11') > -1) {
		link_name = '11';
	} else if (link_name.search('10') > -1) {
		link_name = '10';
	} else if (link_name.search('topten') > -1) {
		link_name = 'topten';
	} else if (link_name.search('9') > -1) {
		link_name = '9';
	} else if (link_name.search('8') > -1) {
		link_name = '8';
	} else if (link_name.search('7') > -1) {
		link_name = '7';
	} else if (link_name.search('6') > -1) {
		link_name = '6';
	} else if (link_name.search('5') > -1) {
		link_name = '5';
	} else if (link_name.search('4') > -1) {
		link_name = '4';
	} else if (link_name.search('3') > -1) {
		link_name = '3';
	} else if (link_name.search('2') > -1) {
		link_name = '2';
	} else if (link_name.search('1') > -1) {
		link_name = '1';
	} 
	
	return link_name;
	
}

function load_sets_homepage(pckg,set) {
	var url = '/exploratory_analysis/classic_views_html?set=' + set; //+ '?_=' + Math.round(Math.random() * 10000);

	alert('set: ' + set);
	
	
	
	$.ajax({
		type : "GET",
		url : url,
		cache : false,
		//data : JSON.stringify(data),
		//async : false,
		success : function(html) {
			
			console.log('html: ' + html);

			$('#landHome').empty();
			$('#atmHome').empty();
			if (pckg == 'lnd') {
				$('#landHome').append(html);
			} else {
				$('#atmHome').append(html);
			}
			
			
			
			/*
			var html_elem_id = packageData + '_' + setData + '_html';

			$('#' + html_elem_id).empty();
			$('#' + html_elem_id).append(html);
			document.getElementById(html_elem_id).style.display = 'block';
			console.log(html_elem_id);
			*/
		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});
}
