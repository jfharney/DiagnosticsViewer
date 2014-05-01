$(document).ready(function(){

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
    
	console.log('csrftoken ' + csrftoken);
	


	$('#signin').click(function(){
			
			var username = $('#username').val();
	        var password = $('#password').val();
	        var email = $('#email').val();
			
			
			var input_data = {
					'csrfmiddlewaretoken': csrftoken,
					'username':username,
					'password':password,
					'email':email
			}
			
			//var url = 'http://localhost:8081/exploratory_analysis/timeseries1/';
			//var url = 'http://localhost:8081/exploratory_analysis/auth/';
			var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/auth/';
			
			
			$.ajax({
				  type: "POST",
				  url: url,
				  data: input_data,
				  success: function(data)
				  { 
					  console.log(data);
					  if(data == 'Authenticated') {
						  console.log('Authenticated - go to the main page with the username');
						  //window.location = 'http://localhost:8081/exploratory_analysis/main/' + username;
						  window.location = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/main/' + username;
					  } else {
						  console.log('Not authenticated - stay on page');
					  }
					  
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