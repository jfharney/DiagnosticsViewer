$(document).ready(function(){

		$("#example").popover({
			trigger : 'hover'
		});  
		
		var jsonData = '';
		var queryString = '';
		var url = 'http://localhost:8081/exploratory_analysis/datasets/' + 'jfharney';
		
		console.log('querying: ' + url);

		$.ajax({
			url: url,
			global: false,
			type: 'GET',
			dataType: 'json',
			data: queryString,
			success: function(data) {
				
				var datasetList = data['datasets'];
				$('#dataset_name').empty();
				for (var i=0;i<datasetList.length;i++) {
					var dataset = datasetList[i];
					$('.dropdown-dataset-menu').append('<li class="dataset_menu" id="' + dataset + '"><a href="#">' + dataset + '</a></li>');
				}
				
			},
			error: function( jqXHR, textStatus, errorThrown ) {
				alert('datasetList textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);

				
			}
		});
		
		
		
		
		

	});