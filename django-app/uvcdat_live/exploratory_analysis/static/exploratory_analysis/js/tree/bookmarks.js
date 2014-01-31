function test2(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "POST",
		  url: fileUrl,
		  async: false,
		  data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test3(fileUrl,csrftoken,data) {

	$.ajax({
		  type: "DELETE",
		  url: fileUrl,
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test4(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "GET",
		  url: fileUrl,
		  dataType: 'json',
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  console.log(response_data);
			  
			  for (var key in response_data) {
				  console.log('key: ' + key + ' value: ' + response_data[key]);
			  }
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test12(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "POST",
		  url: fileUrl,
		  async: false,
		  data: data,
		  success: function(response_data)
		  { 
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test13(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "DELETE",
		  url: fileUrl,
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('delete success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test14(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "GET",
		  url: fileUrl,
		  dataType: 'json',
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  console.log(response_data);
			  
			  for (var key in response_data) {
				  console.log('key: ' + key + ' value: ' + response_data[key]);
			  }
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}


function getSampleDataTree(csrftoken) {
	var tree_bookmark_name = 'tree_bookmark_name1';
    var tree_bookmark_datasetname = 'tree_bookmark_datasetname1';
    var tree_bookmark_realm = 'tree_bookmark_realm1';
    var tree_bookmark_username = 'tree_bookmark_username1';
    var tree_bookmark_variables = 'tree_bookmark_variables1';
    var tree_bookmark_times = 'tree_bookmark_times1';
    var tree_bookmark_sets = 'tree_bookmark_sets1';
    var tree_bookmark_description = 'tree_bookmark_description1';
    var tree_cache_url = 'tree_cache_url1';
    
    var data = {
    			'csrfmiddlewaretoken': csrftoken,
    			'tree_bookmark_name': tree_bookmark_name,
    			'tree_bookmark_datasetname':tree_bookmark_datasetname,
    			'tree_bookmark_realm':tree_bookmark_realm,
    			'tree_bookmark_username':tree_bookmark_username,
    			'tree_bookmark_variables':tree_bookmark_variables,
    			'tree_bookmark_times':tree_bookmark_times,
    			'tree_bookmark_sets':tree_bookmark_sets,
    			'tree_bookmark_description':tree_bookmark_description,
    			'tree_cache_url':tree_cache_url
    };
    
    return data;
}

function getSampleQueryStringTree() {
	var tree_bookmark_name = 'tree_bookmark_name1';
    var tree_bookmark_datasetname = 'tree_bookmark_datasetname1';
    var tree_bookmark_realm = 'tree_bookmark_realm1';
    var tree_bookmark_username = 'tree_bookmark_username1';
    
    var querystring = '?tree_bookmark_name=' + tree_bookmark_name+
	'&tree_bookmark_datasetname=' + tree_bookmark_datasetname+
	'&tree_bookmark_realm=' + tree_bookmark_realm+
	'&tree_bookmark_username=' + tree_bookmark_username;

    
    return querystring;
}



function getSampleDataFigure(csrftoken) {
	
	var figure_bookmark_name = 'figure_bookmark_name1';
    var figure_bookmark_datasetname = 'figure_bookmark_datasetname1';
    var figure_bookmark_realm = 'figure_bookmark_realm1';
    var figure_bookmark_username = 'figure_bookmark_username1';
    var figure_bookmark_description = 'figure_bookmark_description1';
    var figure_cache_url = 'figure_cache_url1';
    
    var data = {
    			'csrfmiddlewaretoken': csrftoken,
    			'figure_bookmark_name': figure_bookmark_name,
    			'figure_bookmark_datasetname':figure_bookmark_datasetname,
    			'figure_bookmark_realm':figure_bookmark_realm,
    			'figure_bookmark_username':figure_bookmark_username,
    			'figure_bookmark_description':figure_bookmark_description,
    			'figure_cache_url':figure_cache_url
    };
	
	return data;
}

function getSampleQueryStringFigure() {
	
	var figure_bookmark_name = 'figure_bookmark_name1';
    var figure_bookmark_datasetname = 'figure_bookmark_datasetname1';
    var figure_bookmark_realm = 'figure_bookmark_realm1';
    var figure_bookmark_username = 'figure_bookmark_username1';
	
	var querystring = '?figure_bookmark_name=' + figure_bookmark_name+
						'&figure_bookmark_datasetname=' + figure_bookmark_datasetname+
						'&figure_bookmark_realm=' + figure_bookmark_realm+
						'&figure_bookmark_username=' + figure_bookmark_username;
	
	
	return querystring;
}

