$(document).ready(function(){
	

	$('.dropdown-dataset-menu').on('click','a',function() {
			//alert('issue an ajax call for variables for dataset ' + this.innerHTML);
			
			var jsonData = '';
			var queryString = '';
			var url = 'http://localhost:8081/exploratory_analysis/variables/' + this.innerHTML;
			
			console.log('querying: ' + url);
			
			
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				dataType: 'json',
				data: queryString,
				success: function(data) {
					
					for(var key in data) {
						console.log('key: ' + key + ' ' + data[key]);
					}
					
					var variableList = data['variables'];
					$('.dropdown-variable-menu').empty();
					
					console.log(variableList);
					for (var i=0;i<variableList.length;i++) {
						var variable = variableList[i];
						console.log('variable: ' + variable);
						$('.dropdown-variable-menu').append('<li class="variable_menu" id="' + variable + '"><a href="#">' + variable + '</a></li>');
					}
					
					$('#dropdown-variable-container').show();

					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('variables textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});

			$('#dataset_name').empty();
			$('#dataset_name').append(this.innerHTML);
			
		});
	
});