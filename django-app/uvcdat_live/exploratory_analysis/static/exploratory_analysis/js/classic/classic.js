$(document).ready(function() {

	//alert('loading classic.js');
	$('.classic_figure_sets').click(function() {
	
		var index = this.id.search('_');
		
		var set = this.id.substring(index+1);
		
		
		toggle_vis(set);
		
		
		
	});
	
	$('.classic_toggle_sets').click(function() {
		
		
		var index = this.id.search('_');
		
		var set = this.id.substring(index+1);
		
		//alert('this.id: ' + this.id);
		
		toggle_vis(set);
		
		
	});
	
	$('#selectP').on('change',function() {
		
		var pckg = $('#selectP').val();
		
		if(pckg == 'lmwg') {
			
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
		
		
	});
});

var clicked=0;
function displayImageClick(imageURL)
{
	var imagePath = "<img src=\"" + imageURL + "\" \/>";
	document.getElementById("unglue").style.visibility='visible';
	document.getElementById("plotArea").style.visibility='visible';
	document.getElementById("plotArea").innerHTML=imagePath;
	clicked =1;
}


function displayImageHover(imageURL)
{
	if (clicked!=1){
		var imagePath = "<img src=\"" + imageURL + "\" \/>";
		document.getElementById("plotArea").style.visibility='visible';
		document.getElementById("plotArea").innerHTML=imagePath;
	}
}

function ungluePlot()
{
	clicked =0;
	document.getElementById("unglue").style.visibility='hidden';
	document.getElementById("plotArea").style.visibility='hidden';
}

function nodisplayImage()
{
	if (clicked!=1){
		document.getElementById("plotArea").style.visibility='hidden';
	}
}

function toggle_varSelect()
{
	var dataset = $('#selectD').val();
	$('#dataset_selected').hide();
	$('#variables_div').show();
	getVariables('ul');
}

function toggle_vis(set) {
	
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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
	var varsData = variable_arr;//["var1","var2"];
	var timesData = season_arr; //timesData;
	var packageData = pckg; //"package1";
	var datasetData = dataset;
	
	
	var data = {
			
			"set" : setData,
			"vars" : varsData,
			"times" : timesData,
			"package" : packageData,
			"dataset" : datasetData
			
	};
	
	
	if(packageData == 'amwg') {
		
		var url = '/exploratory_analysis/classic_views_html/' + '?_='+Math.round(Math.random()*10000);
		
		
		
		
		$.ajax({
			type : "POST",
			url : url,
			cache: false,
			data : JSON.stringify(data),
			//async : false,
			success : function(html) {
				
				var html_elem_id = packageData + '_' + setData + '_html';
				
				$('#' + html_elem_id).empty();
				$('#' + html_elem_id).append(html);
				document.getElementById(html_elem_id).style.display = 'block';
				
				
			},
			error : function(xhr, status, error) {
				
				console.log('error');
				if (xhr.status == 404) {
				}
			},
		});
		
				
	
	} else {
		
		var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/classic_views/' + '?_='+Math.round(Math.random()*10000);
		
		
		
		$.ajax({
			type : "POST",
			url : url,
			cache: false,
			data : JSON.stringify(data),
			//async : false,
			success : function(set_url) {
				
				console.log('setData: ' + setData);
				console.log('url: ' + set_url);
				
				//alert('set_url: ' + set_url);
				
				var html_elem_id = packageData + '_' + setData + '_html';
				console.log('html_elem_id: ' + html_elem_id);
				
				$('#' + html_elem_id).load(set_url);

				document.getElementById(html_elem_id).style.display = 'block';
				
			},
			error : function(xhr, status, error) {
				
				console.log('error');
				if (xhr.status == 404) {
				}
				
			}
		});
		
	}
	
	
	
	
	
}

function go_Atm_Home() {
	document.getElementById('atmHome').style.display = 'block';
	
	hide_land_home();
	hide_land_sets();
	hide_atm_sets();

}


function go_Land_Home()
{
	
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
	
	document.getElementById('amwg_set1_html').style.display = 'none';
	document.getElementById('amwg_set2_html').style.display = 'none';
	document.getElementById('amwg_set3_html').style.display = 'none';
	document.getElementById('amwg_set4_html').style.display = 'none';
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


