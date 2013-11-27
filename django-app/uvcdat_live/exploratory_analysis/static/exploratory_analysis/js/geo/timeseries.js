var parseDate = d3.time.format("%Y%m").parse;
var timedata;
$(document).ready(function(){
	
	$('#viz_button').click(function() {

			console.log('dataset id: ' + $('span#dataset_name').html());
			console.log('variable id: ' + $('span#variable_name').html());
			console.log('time id: ' + $('span#time_name').html());
			
			console.log('\n\n\n\npresent time series plot\n\n\n\n\n');
			
			var variable_id = $('span#variable_name').html();
			
			if(variable_id == '' || variable_id == ' ' || variable_id == 'undefined') {
				variable_id = 'AR';
			}
			
			var url = 'http://localhost:8081/exploratory_analysis/timeseries?variable=' + variable_id;
			
			
			
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				//dataType: 'json',
				data: queryString,
				success: function(data) {
					
					alert('success');
					
					var timedata = JSON.parse(data);
					
					for (var key in timedata) {
						//console.log('key: ' + key + ' ' + timedata[key]);
					}
					
					create_multiseries_time_plot(timedata, "map_plot_canvas1", 720, 150);
					
					/*
					var csvObj = d3.csv.parse(data);
					timedata = csvObj;
					for (var key in csvObj) {
						console.log('key: ' + csvObj[key]);
						for(var key2 in csvObj[key]) {
							console.log('  key2 value: ' + csvObj[key][key2]);
						}
					} 
					csvObj.forEach(function(d) {
			            d.date = parseDate(d.date);
			            console.log('d.date:' + d.date + ' ' + d.co2);
			            
			        });
					for (var key in csvObj) {
						console.log('key: ' + csvObj[key]);
						for(var key2 in csvObj[key]) {
							console.log('  key2 value: ' + csvObj[key][key2]);
						}
					} 
					create_multiseries_time_plot(csvObj, "map_plot_canvas1", 720, 150);
					*/
					
					/*
					d3.csv(data, function(error, csvdata) {
				        timedata = csvdata;
				        console.log('timedata: ' + timedata);
				        csvdata.forEach(function(d) {
				            d.date = parseDate(d.date);
				        });
				        create_multiseries_time_plot(timedata, "map_plot_canvas1", 720, 150);
				    });
				    */
					/*
					d3.csv("data/TLAI-avg.csv", function(error, data) {
				        timedata = data;
				        data.forEach(function(d) {
				            d.date = parseDate(d.date);
				        });
				        create_multiseries_time_plot(timedata, "map_plot_canvas1", 720, 150);
				    });
				    */
					/*
					mapdata = JSON.parse(data);
					
					$('.page-header').empty();
					$('.lead').empty();
					$('#map-canvas').empty();
					
					
					create_map_canvas(mapdata, "#map-canvas", 720, 360);
					
					$('.page-header').append('<h3>' + variable_id  + 'Average Map</h3>');
					$('#map-canvas').append('<div>Data for: ' + variable_id + '</div>');
					//$('#map-canvas').append('<div>' + data + '</div>');
					*/
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('timeseries textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});
			
			
		});

});