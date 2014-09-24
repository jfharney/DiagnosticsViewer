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
}

function nodisplayImage()
{
	if (clicked!=1){
		document.getElementById("plotArea").style.visibility='hidden';
	}
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('setData: ' + setData);
			console.log('url: ' + set_url);
			
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
	document.getElementById('amwg_set5_html').style.display = 'none';
	document.getElementById('amwg_set6_html').style.display = 'none';
	document.getElementById('amwg_set7_html').style.display = 'none';
	document.getElementById('amwg_set9_html').style.display = 'none';
}

function hide_land_home() {
	document.getElementById('landHome').style.display = 'none';
}

function hide_atm_home() {
	document.getElementById('atmHome').style.display = 'none';
}


/*
document.getElementById('1energyBalance').style.display = 'none';
document.getElementById('2contourPlots').style.display = 'none';
document.getElementById('3monthlyClimatology').style.display = 'none';
document.getElementById('5tablesAnual').style.display = 'none';
document.getElementById('6anualTrends').style.display = 'none';
document.getElementById('7rtm').style.display = 'none';
document.getElementById('9econtourStats').style.display = 'none';
*/

/*
function toggle_vis1() 
{
	document.getElementById('landHome').style.display = 'none';
	
	

	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set1";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);
			
			$("#1energyBalance").load(set_url);   
			document.getElementById('1energyBalance').style.display = 'block';
			
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
}


function toggle_vis2() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set2";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);
			
			$("#2contourPlots").load(set_url);   
			document.getElementById('2contourPlots').style.display = 'block'; 		
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
						
}
function toggle_vis3() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set3";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);

			$("#3monthlyClimatology").load(set_url);   
			document.getElementById('3monthlyClimatology').style.display = 'block';
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
	
	
	
	
}
function toggle_vis5() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set5";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);

			$("#5tablesAnual").load(set_url); 
			document.getElementById('5tablesAnual').style.display = 'block';
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
	
	
	
	
}
function toggle_vis6() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set6";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);

			$("#6anualTrends").load(set_url); 
			document.getElementById('6anualTrends').style.display = 'block';
			
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
	
	
	
	
	
}
function toggle_vis7() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set7";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);

			$("#7rtm").load(set_url); 
			document.getElementById('7rtm').style.display = 'block';
			
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
	
}




function toggle_vis9() 
{
	document.getElementById('landHome').style.display = 'none';
	
	var dataset = $('#selectD').val();
	var pckg = $('#selectP').val();
	
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

	
	var url = 'http://localhost:8081/exploratory_analysis/classic_views/';
	
	var setData = "set9";
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
	
	
	$.ajax({
		type : "POST",
		url : url,
		data : JSON.stringify(data),
		//async : false,
		success : function(set_url) {
			
			console.log('url: ' + set_url);

			
			$("#9econtourStats").load(set_url); 
			document.getElementById('9econtourStats').style.display = 'block';
			
		},
		error : function(xhr, status, error) {
			
			console.log('error');
			if (xhr.status == 404) {
			}
			
		}
	});
	
	
	
	
	
}
*/

/*
function checkFile(fileUrl) {

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

	var data = {
		'csrfmiddlewaretoken' : csrftoken
	};

	//alert('fileUrl: ' + fileUrl);

	var found = false;
	$.ajax({
		type : "GET",
		url : fileUrl,
		data : data,
		async : false,
		success : function() {
			found = true;
		},
		error : function(xhr, status, error) {
			if (xhr.status == 404) {
			}
		}
	});

	return found;

	var xmlHttpReq = false;
	var self = this;
	// Mozilla/Safari
	if (window.XMLHttpRequest) {
		self.xmlHttpReq = new XMLHttpRequest();
	}
	// IE
	else if (window.ActiveXObject) {
		self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	self.xmlHttpReq.open('HEAD', fileUrl, true);
	self.xmlHttpReq.onreadystatechange = function() {
		if (self.xmlHttpReq.readyState == 4) {
			if (self.xmlHttpReq.status == 200) {
				alert('the file exists');
				return true;
			} else if (self.xmlHttpReq.status == 404) {
				alert('the file does not exist');
				return false;
			}
		}
	}
	self.xmlHttpReq.send();

}
*/

/*
function stripPipe(path) {
	console.log('path1: ' + path);
	path = path.replace(" ", "");
	console.log('path2: ' + path);
	var replacedPath = path.replace(/|/g, "");

	return replacedPath;
}
*/

/*
function replacePipe(path) {

	var replacedPath = path.replace(/|/g, ";");

	return replacedPath;

}
*/

/*
function update(source) {
        // Compute the new height, function counts total children of root node and sets tree height accordingly.
        // This prevents the layout looking squashed when new nodes are made visible or looking sparse when nodes are removed
        // This makes the layout more consistent.
        var levelWidth = [1];
        var childCount = function(level, n) {

            if (n.children && n.children.length > 0) {
                if (levelWidth.length <= level + 1) levelWidth.push(0);

                levelWidth[level + 1] += n.children.length;
                n.children.forEach(function(d) {
                    childCount(level + 1, d);
                });
            }
        };
        childCount(0, root);
        var newHeight = d3.max(levelWidth) * 25; // 25 pixels per line  
        tree = tree.size([newHeight, (width + margin.left + margin.right)]);	
	
	
	// Compute the new tree layout.
	var nodes = tree.nodes(root).reverse(), links = tree.links(nodes);
    var totalNodes = 0;
    var maxLabelLength = 0;
	console.log('--------updated tree state--------');

    function visit(parent, visitFn, childrenFn) {
        if (!parent) return;

        visitFn(parent);

        var children = childrenFn(parent);
        if (children) {
            var count = children.length;
            for (var i = 0; i < count; i++) {
                visit(children[i], visitFn, childrenFn);
            }
        }
    }

    // Call visit function to establish maxLabelLength
    visit(source, function(d) {
        totalNodes++;
        maxLabelLength = Math.max(d.name.length, maxLabelLength);

    }, function(d) {
        return d.children && d.children.length > 0 ? d.children : null;
    });
	// note this was commented out
	 for(var key in nodes) {
	 console.log('nodessss key: ' + key + ' node ' + nodes[key]);
	 var node = nodes[key];
	 for (var nodekey in node) {
	 console.log('  node key: ' + nodekey + ' value: ' + node[nodekey]);
	 }
	 }
	 for(var key in links) {
	 console.log('links key: ' + key + ' link: ' + links[key]);
	 }

	 //postStateExample

	 var url = 'http://' + 'localhost' + ':' + '8081' + '/exploratory_analysis/postStateExample/';

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

	 console.log('csrftoken ' + csrftoken);

	 var data = {
	 'csrfmiddlewaretoken': csrftoken,
	 'links': links

	 };

	 $.ajax({
	 url: url,
	 type: 'POST',
	 //dataType: 'json',
	 data: data,
	 success: function(data) {

	 console.log('post example success');

	 },
	 error: function( jqXHR, textStatus, errorThrown ) {
	 alert('timeseries textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);

	 }
	 });

	 //end note this was commented out

	console.log('--------end updated tree state--------');
	//console.log('****\n' + JSON.stringify(nodes) + '\n*******');

	//EA.tree_state = nodes;

	// Normalize for fixed-depth.
	nodes.forEach(function(d) {
		d.y = d.depth * EA.treeDepthFactor;
	});

	// Update the nodes�
	var node = svg.selectAll("g.node").data(nodes, function(d) {
		return d.id || (d.id = ++i);
	});

	// Enter any new nodes at the parent's previous position.
	var nodeEnter = node.enter().append("g").attr("class", "node").attr("transform", function(d) {
		return "translate(" + source.y0 + "," + source.x0 + ")";
	}).on("click", click).on("mouseover", hover);

	nodeEnter.append("circle").attr("r", 1e-6).style("fill", function(d) {
		return d._children ? "lightsteelblue" : "#fff";
	});

	nodeEnter.append("text").attr("x", function(d) {
		return d.children || d._children ? -10 : 10;
	}).attr("dy", ".35em").attr("text-anchor", function(d) {
		return d.children || d._children ? "end" : "start";
	}).text(function(d) {
		return d.name;
	}).style("fill-opacity", 1e-6);

	// Transition nodes to their new position.
	var nodeUpdate = node.transition().duration(duration).attr("transform", function(d) {
		return "translate(" + d.y + "," + d.x + ")";
	});

	nodeUpdate.select("circle").attr("r", 4.5).style("fill", function(d) {
		return d._children ? "lightsteelblue" : "#fff";
	});

	nodeUpdate.select("text").style("fill-opacity", 1);

	// Transition exiting nodes to the parent's new position.
	var nodeExit = node.exit().transition().duration(duration).attr("transform", function(d) {
		return "translate(" + source.y + "," + source.x + ")";
	}).remove();

	nodeExit.select("circle").attr("r", 1e-6);

	nodeExit.select("text").style("fill-opacity", 1e-6);

	// Update the links�
	var link = svg.selectAll("path.link").data(links, function(d) {
		return d.target.id;
	});

	// Enter any new links at the parent's previous position.
	link.enter().insert("path", "g").attr("class", "link").attr("d", function(d) {
		var o = {
			x : source.x0,
			y : source.y0
		};
		return diagonal({
			source : o,
			target : o
		});
	});

	// Transition links to their new position.
	link.transition().duration(duration).attr("d", diagonal);

	// Transition exiting nodes to the parent's new position.
	link.exit().transition().duration(duration).attr("d", function(d) {
		var o = {
			x : source.x,
			y : source.y
		};
		return diagonal({
			source : o,
			target : o
		});
	}).remove();

	// Stash the old positions for transition.
	nodes.forEach(function(d) {
		d.x0 = d.x;
		d.y0 = d.y;
	});
}
*/




/*
// Define the zoom function for the zoomable tree

function zoom() {
	svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}
*/


/*
// define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom", zoom);

    function centerNode(source) {
        scale = zoomListener.scale();
        x = -source.y0; 
        y = -source.x0;
        x = x * scale + viewerWidth / 2;
        y = y * scale + viewerHeight / 2;
        d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + x + "," + y + ")scale(" + scale + ")");
        zoomListener.scale(scale);
        zoomListener.translate([x, y]);
    }
//console.log('ea: ' + EA.tree_margin_right);

var margin = {
	top : EA.tree_margin_top,
	right : EA.tree_margin_right,
	bottom : EA.tree_margin_bottom,
	left : EA.tree_margin_left
}, width = EA.tree_width - margin.right - margin.left, height = EA.tree_height - margin.top - margin.bottom;

var i = 0, duration = 750, root;

for (var key in d3.layout.tree()) {
	console.log('key: ' + key + ' layout: ' + d3.layout[key]);
}

var tree = d3.layout.tree().size([height, width]);

tree.separation(function(a, b) {
	return (a.parent == b.parent ? 1 : 1.2);
});

var diagonal = d3.svg.diagonal().projection(function(d) {
	return [d.y, d.x];
});

var svg = d3.select("#treeimg").append("svg").attr("width", width + margin.right + margin.left).attr("height", height + margin.top + margin.bottom).call(zoomListener).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.select(self.frameElement).style("height", "800px");

var fullpath = '';


    // Function to center node when clicked/dropped so node doesn't get lost when collapsing/moving with large amount of children.

    function centerNode(source) {
        scale = zoomListener.scale();
        x = -source.y0;
        y = -source.x0;
        x = x * scale + (width + margin.right + margin.left) / 2;
        y = y * scale + (height + margin.top + margin.bottom) / 2;
        d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + x + "," + y + ")scale(" + scale + ")");
        zoomListener.scale(scale);
        zoomListener.translate([x, y]);
    }


function hover(d) {

	var name = d['name'];
	//console.log(name + ' ' + d.parent.name);

	var path = '';

	var node = d;
	while (node.parent != undefined) {
		path = path + '9' + node.name;
		//console.log('path: ' + path);
		node = node.parent;
	}
	//console.log('root: ' + node.name);
	path = path + '9' + node.name;
	//console.log('final path: ' + path);
	fullpath = path
}

// TODO: Pan function, can be better implemented.

function pan(domNode, direction) {
	var speed = panSpeed;
	if (panTimer) {
		clearTimeout(panTimer);
		translateCoords = d3.transform(svgGroup.attr("transform"));
		if (direction == 'left' || direction == 'right') {
			translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
			translateY = translateCoords.translate[1];
		} else if (direction == 'up' || direction == 'down') {
			translateX = translateCoords.translate[0];
			translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
		}
		scaleX = translateCoords.scale[0];
		scaleY = translateCoords.scale[1];
		scale = zoomListener.scale();
		svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
		d3.select(domNode).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
		zoomListener.scale(zoomListener.scale());
		zoomListener.translate([translateX, translateY]);
		panTimer = setTimeout(function() {
			pan(domNode, speed, direction);
		}, 50);
	}
}
*/


/*
//Toggle children on click.
function click(d) {
    centerNode(d);
	if (d.children) {
		console.log('in if d.children ');
		d._children = d.children;
		d.children = null;
	} else {
		console.log('in else ');
		if (d['_children'] == undefined) {
			var name = d['name'];
			console.log('name: ' + name);

			
			 for(var key in d) {
			 console.log('key: ' + key + ' val: ' + d[key]);
			 }
			

			

			var params = fullpath.split('9');
			//9MAR9TLAI9set19tropics_warming_th_q_co29lmwg9jfharney

			var times = '';
			var variables = '';
			var sets = '';
			var dataset = '';
			var packages = '';
			var realms = 'land';
			var username = '';

			for (var i = 0; i < params.length; i++) {
				console.log('param: ' + params[i]);
				if (i == 1) {
					times = params[i];
				} else if (i == 2) {
					variables = params[i];
				} else if (i == 3) {
					sets = params[i];
				} else if (i == 4) {
					dataset = params[i];
				} else if (i == 5) {
					packages = params[i];
				} else if (i == 6) {
					username = params[i];
				}

			}

			figure_generator(times, variables, sets, dataset, packages, realms, username, fullpath);

		}
		d.children = d._children;
		d._children = null;
	}
	update(d);
}
*/


/*
function reversePath(path) {

	var reversedPath = '';

	var pathArr = path.split('|');
	for (var i = pathArr.length; i--; i > 1) {

		if (i > 1) {
			console.log('i: ' + i + ' ' + pathArr[i] + '->');
			reversedPath += pathArr[i] + '->';
		} else {
			console.log('i: ' + i + ' ' + pathArr[i]);
			reversedPath += pathArr[i];
		}

	}

	return reversedPath;

}
*/


/*
function figure_generator(times, variables, sets, dataset, packages, realms, username, fullpath) {
	var csrftoken = getCookie('csrftoken');

	console.log('*&^(^*%^*&^%*&^%*^%*^%*' + dataset);

	//var computedImg = "../../../static/exploratory_analysis/img/carousel/set6_turbf_Global.gif";

	//var img_prefix = '../../../static/exploratory_analysis/img/treeex/';

	var img_prefix = '../../../static/exploratory_analysis/img/tree/' + dataset + '/';
	//tropics_warming_th_q_co222/';

	//alert('computedIMG: ' + img_prefix + realms + '_' + packages + '_' + sets + '_' + times + '_' + variables + '.png');

	var computedImg = '../../../static/exploratory_analysis/img/treeex/land_lmwg_set1_MAY_TG.png';

	//var staticImg = "{% static 'exploratory_analysis/img/carousel/set6_turbf_Global.gif' %}";
	//"../../../static/exploratory_analysis/css/tree/flare13.json"
	var staticImg = img_prefix + realms + '_' + packages + '_' + sets + '_' + times + '_' + variables + '.png';
	//computedImg;

	$body = $("body");

	var data = {
		'csrfmiddlewaretoken' : csrftoken,
		'variables' : variables,
		'times' : times,
		'sets' : sets,
		'packages' : packages,
		'realms' : realms
	};

	$body.addClass("loading");

	//var get_image_url = 'http://localhost:8081/exploratory_analysis/figure_generator/';

	var get_image_url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/figure_generator/';

	$.ajax({
		url : get_image_url,
		//global: false,
		type : 'POST',
		data : data,
		success : function(data) {
			//alert('data: ' + data);
			//alert('fullpath ' + fullpath)
			//cachedFile = realms[0] + '_' + packages[0] + '_set' + sets[0] + '_' + times[0] + '_' + variables[0] + '.png'
			var figTitle = realms + '_' + packages + '_' + sets + '_' + times + '_' + variables + '.png';

			$('#modal-title').empty();
			$('.modal-body').empty();
			//$('#modal-title').append('<span>TITLE:</span> <div id="' + "figtitle" + '"> ' + reversePath(fullpath) + '</div>');
			//$('#modal-title').append('<span>TITLE:</span> <div id="' + "figtitle" + '"> ' + figTitle + '</div>');
			$('#modal-title').append('<div id="' + "figtitle" + '"> ' + figTitle + '</div>');

			//$('#modal-title').append('<span>URL:</span> <div id="' + "figurl" + '">' + staticImg + '</div>');
			$('.modal-body').append('<div>' + '<img src="' + staticImg + '" style="max-width:600px;max-height:500px;display: block;display: block;margin-left: auto;margin-right: auto" />' + '</div>')
			$('.modal-body').append('<div id="fig_url" style="display:none" >' + staticImg + '</div>');

			//$('#figure_bookmark_description').

			console.log('figTitle: ' + figTitle);

			var addedListing = ' <li style="padding:10px;border: 1px solid #000000;list-style-type: none;margin-bottom:10px" id="' + stripPeriod(figTitle) + '">' + '<a class="thumbnail">' + '<img src="' + staticImg + '" style="max-width:150px;display: block;" />' + '</a>' +
			//'<div style="font-size:10px;color:red;text-align: center;margin-top:5px">' + reversePath(fullpath) + '</div>' +
			'<div style="font-size:10px;color:red;text-align: center;margin-top:5px">' + figTitle + '</div>' + '<div style="text-align: center;;padding:5px">' + '<button type="button" class="btn btn-default btn-remove" style="margin-right:10px;" id="' + stripPeriod(figTitle) + '">' + 'Remove' + '</button>' +

			//'<button type="button" class="btn btn-default btn-remove" style="margin-right:10px;" id="remove_' + stripPipe(fullpath) + '">'+'Remove'+'</button>' +
			'<a data-toggle="modal" href="#myModal" class="btn btn-primary">View</a>' + '</div>' + '</li>';

			$('div#gallery').append(addedListing);

			//add an image
			var appended = '<div class="row"><div class="col-md-12">' + name + '</div></div>';

			$body.removeClass("loading");

		},
		error : function(jqXHR, textStatus, errorThrown) {
			//alert('datasetList textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
			alert('error in generating figure');

			$body.removeClass("loading");

		}
	});

}
*/

/*
function stripPeriod(word) {
	var newWord = '';
	newWord = word.replace('.', '_');
	return newWord;
}
*/

/*
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
*/