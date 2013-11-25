
$(document).ready(function(){
	
	$('#viz_button').click(function() {

			console.log('dataset id: ' + $('span#dataset_name').html());
			console.log('variable id: ' + $('span#variable_name').html());
			console.log('time id: ' + $('span#time_name').html());
			
			var variable_id = $('span#variable_name').html();
			
			if(variable_id == '' || variable_id == ' ' || variable_id == 'undefined') {
				variable_id = 'AR';
			}
			
			var url = 'visualizations?variable=' + variable_id;
			
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				dataType: 'json',
				data: queryString,
				success: function(data) {
					
					//console.log('data: ' + data);
					$('.page-header').empty();
					$('.lead').empty();
					$('#map-canvas').empty();
					
					create_map_canvas(data, "#map-canvas", 720, 360);
					
					$('.page-header').append('<h3>' + variable_id  + 'Average Map</h3>');
					$('#map-canvas').append('<div>Data for: ' + variable_id + '</div>');
					//$('#map-canvas').append('<div>' + data + '</div>');
					
					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('vizualizations textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});
			
			
		});

});