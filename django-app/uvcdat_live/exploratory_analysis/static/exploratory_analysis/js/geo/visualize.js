
$(document).ready(function(){
	
	$('#viz_button').click(function() {

			console.log('dataset id: ' + $('span#dataset_name').html());
			console.log('variable id: ' + $('span#variable_name').html());
			console.log('time id: ' + $('span#time_name').html());
			
			var variable_id = $('span#variable_name').html();
			
			if(variable_id == '' || variable_id == ' ' || variable_id == 'undefined') {
				variable_id = 'AR';
			}
			
			var url = 'http://localhost:8081/exploratory_analysis/visualizations?variable=' + variable_id;
			var queryString = '';
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				dataType: 'json',
				data: queryString,
				success: function(data) {
					//console.log(data);
					mapdata = JSON.parse(data);
					
					$('.page-header').empty();
					$('.lead').empty();
					$('#map-canvas').empty();
					
					        var parseDate = d3.time.format("%Y%m").parse;

        d3.json("/static/exploratory_analysis/json_grid_data/TLAI-geogrid-0151-01.json", function(error, mapdata) {
            
            d3.json("http://localhost:8081/exploratory_analysis/timeseries/293/546/TLAI", function(error, timedata) {
                var current_year = +timedata.start_year;
                var current_month = +timedata.start_month;
                var timeseries_objects = [];
                timedata.timeseries_data.forEach(function(d) {
                    //d.date = parseDate(d.date);
                    var obj = {};
                    obj.date = new Date(current_year, (current_month-1), 1, 0, 0, 0, 0);
                    obj.value = d;
                    timeseries_objects.push(obj);
                    //console.log(obj);
                    if (current_month == 12) {
                        current_month = 1;
                        current_year++;
                    } else {
                        current_month++;
                    }
                });
                create_cyclone_plot(mapdata.geo_data, timeseries_objects, "#map-canvas");
            });
        });
					//create_map_canvas(mapdata, "#map-canvas", 720, 360);
					
					$('.page-header').append('<h3>' + variable_id  + 'Average Map</h3>');
					//$('#map-canvas').append('<div>Data for: ' + variable_id + '</div>');
					//$('#map-canvas').append('<div>' + data + '</div>');
					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('vizualizations textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});
			
			
		});

});