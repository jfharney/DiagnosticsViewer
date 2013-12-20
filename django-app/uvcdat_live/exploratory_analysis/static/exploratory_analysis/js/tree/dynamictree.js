
$(document).ready(function(){

	
	//removing thumbnail image from the pane
	$('body').on('click','button.btn-remove',function() {
		var id = $(this).attr('id');
		console.log('id: ' + id);
		var removedListId = id.split('_')[1];
		$('li#'+removedListId).remove();
	});
	
	
});


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

	  // Update the nodes�
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

  // Update the links�
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

//http://localhost:8081/static/exploratory_analysis/css/bootstrap/bootstrap.css
d3.json("../../../static/exploratory_analysis/css/tree/flare13.json", function(error, flare) {
///Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare13.json
//d3.json("{% static 'exploratory_analysis/css/tree/flare13.json' %}", function(error, flare) {
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
  alert('in if');
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
	  
	  var computedImg = "../../../static/exploratory_analysis/img/carousel/set6_turbf_Global.gif";
	  
	  //var staticImg = "{% static 'exploratory_analysis/img/carousel/set6_turbf_Global.gif' %}";
	  //"../../../static/exploratory_analysis/css/tree/flare13.json"
	  var staticImg = computedImg;
	  
	  $('#modal-title').empty();
	  $('.modal-body').empty();
	  $('#modal-title').append('<div>' + reversePath(fullpath) + '</div>');
	  $('.modal-body').append('<div>' + '<img src="' + staticImg + '" style="max-width:600px;max-height:500px;display: block;display: block;margin-left: auto;margin-right: auto" />' + '</div>')
	  
	  console.log('picname: ' + name);
	  var addedListing = ' <li style="padding:10px;border: 1px solid #000000;list-style-type: none;margin-bottom:10px" id="' + stripPipe(fullpath) + '">' +
	  	'<a class="thumbnail">' +
	  	'<img src="' + staticImg + '" style="max-width:150px;display: block;" />' +
	  	'</a>' +
	  	'<div style="font-size:10px;color:red;text-align: center;margin-top:5px">' + reversePath(fullpath) + '</div>' +
	  	'<div style="text-align: center;;padding:5px">' +
	  	'<button type="button" class="btn btn-default btn-remove" style="margin-right:10px;" id="remove_' + stripPipe(fullpath) + '">'+'Remove'+'</button>' +
	  	'<a data-toggle="modal" href="#myModal" class="btn btn-primary">View</a>' +
	  	'</div>' +
	  	'</li>';
	  	
	  	
	  
	  
	  //add an image
	  var appended = '<div class="row"><div class="col-md-12">'+ name + '</div></div>';
	  $('div#gallery').append(addedListing);
		
	  
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
