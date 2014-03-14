
$(document).ready(function(){

	
	//removing thumbnail image from the pane
	$('body').on('click','button.btn-remove',function() {
		var id = $(this).attr('id');
		//alert('id: ' + id);
		console.log('id: ' + id);
		var removedListId = id.split('_')[1];
		//alert('removedListId: ' + removedListId);
		//$('li#'+removedListId).remove();
		$('li#'+id).remove();
	});
	
	
	

	//var cache_dir = '../../../static/cache/';
	
	//var fileName = "flare25.json";
	
	var treeFile = $('span#treeFile').html();
	console.log('treeFile: ' + treeFile);
	
	
	//EA.uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live';
	
	
	treeFile = treeFile.replace(EA.uvcdat_live_root + '/exploratory_analysis','../../..');
	console.log('treeFile: ' + treeFile);
	
	//treeFile = '../../../static/cache/temp.json';
	//alert('treeFile: ' + treeFile);
	//if(checkFile(cache_dir+fileName))
	
	//check to see if there was a tree loaded
	var treeloaded = $('span#treeloaded').html();
	console.log('treeloaded: ' + tree);
	console.log('chk: ' + checkFile(treeFile));
	if(treeloaded == 'true') {
		
		if(checkFile(treeFile))
		{
		
			//render the tree
			
			d3.json(treeFile, function(error, flare) {
			
			//d3.json(cache_dir + fileName, function(error, flare) {
			
			///Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare13.json
			root = flare;
			root.x0 = height / 2;
			root.y0 = 0;
		
			function collapse(d) {
			if (d.children) {
			  d._children = d.children;
			  d._children.forEach(collapse);
			  d.children = null;
			}
			}
		
			root.children.forEach(collapse);
			update(root);
			});
		
		} else {
			console.log('leave blank');
		}
		
		
	} else {
		//$('#bookmark_selection').show();
	}
	
	
	
	
	
	
	
	
});


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
    
    var data = {'csrfmiddlewaretoken': csrftoken};
	
    //alert('fileUrl: ' + fileUrl);
    
	var found = false;
	$.ajax({
		  type: "GET",
		  url: fileUrl,
		  data: data,
		  async: false,
		  success: function()
		  { 
			  found = true;
		  },
		  error: function(xhr, status, error) {
		    if(xhr.status==404)
		      { /** not found! **/}
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

function stripPipe(path) {
	console.log('path1: ' + path);
	path = path.replace(" ","");
	console.log('path2: ' + path);
	var replacedPath = path.replace(/|/g,""); 
	
	return replacedPath;
}

function replacePipe(path) {
	
	var replacedPath = path.replace(/|/g,";"); 
	
	return replacedPath;
	
}


function update(source) {
	// Compute the new tree layout.
	  var nodes = tree.nodes(root).reverse(),
	      links = tree.links(nodes);

	  // Normalize for fixed-depth.
	  nodes.forEach(function(d) { d.y = d.depth * 100; });

	  // Update the nodesÉ
	  var node = svg.selectAll("g.node")
	      .data(nodes, function(d) { return d.id || (d.id = ++i); });

	  
	  // Enter any new nodes at the parent's previous position.
	  var nodeEnter = node.enter().append("g")
	      .attr("class", "node")
	      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
	      .on("click", click)
	      .on("mouseover", hover);

	  nodeEnter.append("circle")
	      .attr("r", 1e-6)
	      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	  nodeEnter.append("text")
	      .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
	      .attr("dy", ".35em")
	      .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	      .text(function(d) { return d.name; })
	      .style("fill-opacity", 1e-6);

	  // Transition nodes to their new position.
	  var nodeUpdate = node.transition()
	      .duration(duration)
	      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

	  nodeUpdate.select("circle")
	      .attr("r", 4.5)
	      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	  
	  
	  
	  
	  nodeUpdate.select("text")
      .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExit.select("circle")
      .attr("r", 1e-6);

  nodeExit.select("text")
      .style("fill-opacity", 1e-6);

  // Update the linksÉ
  var link = svg.selectAll("path.link")
      .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}


var margin = {top: 20, right: 120, bottom: 20, left: 90},
width = 960 - margin.right - margin.left,
height = 800 - margin.top - margin.bottom;

var i = 0,
duration = 750,
root;

for (var key in d3.layout.tree()) {
console.log('key: ' + key + ' layout: ' + d3.layout[key]);
}

var tree = d3.layout.tree()
.size([height, width]);


tree.separation(function(a, b) { return (a.parent == b.parent ? 1 : 1.2); });

var diagonal = d3.svg.diagonal()
.projection(function(d) { return [d.y, d.x]; });

var svg = d3.select("#treeimg").append("svg")
.attr("width", width + margin.right + margin.left)
.attr("height", height + margin.top + margin.bottom)
.attr("style","overflow-x:visible")
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");







d3.select(self.frameElement).style("height", "800px");

var fullpath = '';

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


//Toggle children on click.
function click(d) {
if (d.children) {
  d._children = d.children;
  d.children = null;
} else {
  //alert('in else ');
  
  if(d['_children'] == undefined) {
	  var name = d['name'];
	  console.log('name: ' + name);
	  
	  for(var key in d) {
		  console.log('key: ' + key + ' val: ' + d[key]);
	  }
	  
	  
	  
	  
	  
	  
	  /*
	   * 
	   */
	  
	  var params = fullpath.split('9');
	  //9MAR9TLAI9set19tropics_warming_th_q_co29lmwg9jfharney
	  
	  var times = '';
	  var variables = '';
	  var sets = '';
	  var dataset = '';
	  var packages = '';
	  var realms = 'land';
	  var username = 'jfharney';
	  
	  for(var i=0;i<params.length;i++) {
		  console.log('param: ' + params[i]);
		  if(i == 1) {
			  times = params[i];
		  } else if(i == 2) {
			  variables = params[i];
		  } else if(i == 3) {
			  sets = params[i];
		  } else if(i == 4) {
			  dataset = params[i];
		  } else if(i == 5) {
			  packages = params[i];
		  } else if(i == 6) {
			  username = params[i];
		  }
		  
	  }
	  //alert('fullpath: ' + fullpath);
	  figure_generator(times,variables,sets,dataset,packages,realms,username,fullpath);
	  
  }
		d.children = d._children;
		d._children = null;
}
update(d);
}


function reversePath(path) {
	
	var reversedPath = '';
	
	var pathArr = path.split('|');
	for(var i=pathArr.length;i--;i>1) {
		
		if(i > 1) {
			console.log('i: ' + i + ' ' + pathArr[i]+'->');
			reversedPath += pathArr[i]+'->';
		}
			
		else {
			console.log('i: ' + i + ' ' + pathArr[i]);
			reversedPath += pathArr[i];
		}
			
	}
	
	return reversedPath;
	
}


function figure_generator(times,variables,sets,dataset,packages,realms,username,fullpath) {
	var csrftoken = getCookie('csrftoken');
	
	//var computedImg = "../../../static/exploratory_analysis/img/carousel/set6_turbf_Global.gif";
	  
	var img_prefix = '../../../static/exploratory_analysis/img/treeex/';
	//alert('computedIMG: ' + img_prefix + realms + '_' + packages + '_' + sets + '_' + times + '_' + variables + '.png');
	
	  var computedImg = '../../../static/exploratory_analysis/img/treeex/land_lmwg_set1_MAY_TG.png';
	  
	  //var staticImg = "{% static 'exploratory_analysis/img/carousel/set6_turbf_Global.gif' %}";
	  //"../../../static/exploratory_analysis/css/tree/flare13.json"
	var staticImg = img_prefix + realms + '_' + packages + '_' + sets + '_' + times + '_' + variables + '.png';//computedImg;
	  

	$body = $("body");
	
    var data = {
    			'csrfmiddlewaretoken': csrftoken,
    			'variables': variables,
    			'times':times,
    			'sets':sets,
    			'packages':packages,
    			'realms':realms
    };

	$body.addClass("loading");  
    
    
	//var get_image_url = 'http://localhost:8081/exploratory_analysis/figure_generator/';
	
	var get_image_url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/figure_generator/';
	
	
	$.ajax({
		url: get_image_url,
		//global: false,
		type: 'POST',
		data: data,
		success: function(data) {
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
			  //alert('strip pipe: ' + stripPipe(fullpath))
			  //alert('figTitle: ' + figTitle);
			  var addedListing = ' <li style="padding:10px;border: 1px solid #000000;list-style-type: none;margin-bottom:10px" id="' + stripPeriod(figTitle) + '">' +
			  	'<a class="thumbnail">' +
			  	'<img src="' + staticImg + '" style="max-width:150px;display: block;" />' +
			  	'</a>' +
			  //'<div style="font-size:10px;color:red;text-align: center;margin-top:5px">' + reversePath(fullpath) + '</div>' +
			    '<div style="font-size:10px;color:red;text-align: center;margin-top:5px">' + figTitle + '</div>' +
			  	'<div style="text-align: center;;padding:5px">' +
			  	'<button type="button" class="btn btn-default btn-remove" style="margin-right:10px;" id="' + stripPeriod(figTitle) + '">'+'Remove'+'</button>' +
			  	
			  	//'<button type="button" class="btn btn-default btn-remove" style="margin-right:10px;" id="remove_' + stripPipe(fullpath) + '">'+'Remove'+'</button>' +
			  	'<a data-toggle="modal" href="#myModal" class="btn btn-primary">View</a>' +
			  	'</div>' +
			  	'</li>';
			  	
			  	
			  
			  
			  //add an image
			  var appended = '<div class="row"><div class="col-md-12">'+ name + '</div></div>';
			  $('div#gallery').append(addedListing);
			

			  $body.removeClass("loading");  
			
			
			
		},
		error: function( jqXHR, textStatus, errorThrown ) {
			//alert('datasetList textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
			alert('error in generating figure');
			
			$body.removeClass("loading"); 
			
		}
	  });
	  
}

function stripPeriod(word) {
	var newWord = '';
	newWord = word.replace('.','_');
	return newWord;
}

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
