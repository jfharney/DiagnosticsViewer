$(document).ready(function(){
	
		$('.dropdown-variable-menu').on('click','a',function() {
			//alert('issue an ajax call for variables for dataset ' + this.innerHTML);
			
			console.log('find times ' + this.innerHTML);
			
			var jsonData = '';
			var queryString = '';
			var url = 'http://localhost:8081/exploratory_analysis/times/' + this.innerHTML;
			
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
					
					var timeList = data['times'];
					$('.dropdown-time-menu').empty();
					
					console.log(timeList);
					for (var i=0;i<timeList.length;i++) {
						var time = timeList[i];
						console.log('time: ' + time);
						$('.dropdown-time-menu').append('<li class="time_menu" id="' + time + '"><a href="#">' + time + '</a></li>');
					}
					
					$('#dropdown-time-container').show();

					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('times textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});

			$('#variable_name').empty();
			$('#variable_name').append(this.innerHTML);
			
		});
});
		