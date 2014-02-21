$(document).ready(function(){
	


$body = $("body");
	
	
	$('#save_plot').click(function() {
		
		
		console.log('csrftoken in test ' + csrftoken);
		

		//var figureUrl = '../../../static/exploratory_analysis/img/carousel/set6_turbf_Global.gif';
		var figureUrl = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/treeex/land_lmwg_set1_MAY_TG.png';
		console.log('title: ' + $('#modal-title').find('#figtitle').html());
		console.log('url: ' + $('#modal-title').find('#figurl').html());
		
		var figureName = $('#modal-title').find('#figtitle').html();
		
		console.log('need to push a figure url (e.g. ' + figureUrl +') with figure name: ' + figureName);
		
		
		var indexOf = figureName.indexOf('.png');
		
		console.log('substring: ' + figureName.substr(0,indexOf).trim() + ' length: ' + figureName.substr(0,indexOf).trim().length) ;
		
		figureName = figureName.substr(0,indexOf).trim();
		
		var fileUrl = $('#modal-body').find('#fig_url').html();

		fileUrl = '../../../static/exploratory_analysis/img/treeex/' + figureName;
		
		console.log('fileUrl:----------> ' + fileUrl);
		
		var description = $('textarea#figure_bookmark_description').val();
		
		
		
		var figure_bookmark_username = 'jfharney';
		var figure_bookmark_name = figureName;
		var figure_bookmark_location = figureUrl;
		var figure_bookmark_description = description;

		//var figure_bookmark_name = 'land_lmwg_set1_MAY_NPP';
		
		//console.log('trythis--->' + figure_bookmark_name + figureName );
		//console.log('fig name sent(length): ' + figure_bookmark_name.length + ' fig name replace(length): ' + figureName.length);
		
		var figure_bookmark_realm = 'land';
		var figure_bookmark_datasetname = 'tropics_warming_th_q_co2';
		var figure_cache_url = fileUrl;

		//console.log('figure_bookmark_name: ' + figure_bookmark_name);
		
		var data = {
				'csrfmiddlewaretoken': csrftoken,
				'figure_bookmark_name' : figure_bookmark_name,
				'figure_bookmark_realm' : figure_bookmark_realm,
				'figure_bookmark_datasetname' : figure_bookmark_datasetname,
				'figure_bookmark_username' : figure_bookmark_username,
				'figure_bookmark_description' : figure_bookmark_description,
				'figure_cache_url' : figure_cache_url
		}


		//$body.addClass("loading");  
		
		//var url = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var url = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/figure_bookmarks/";
		
		
		$.ajax({
			  type: "POST",
			  url: url,
			  //async: false,
			  data: data,
			  success: function()
			  { 
				  console.log('success');

				  //$body.removeClass("loading");  
				  
			  },
			  error: function(xhr, status, error) {
				  console.log('error'); 
			    if(xhr.status==404)
			    { 
			    	
			    }
			  }
			});
		
		
	});
	
	
	
	
});
	
	