$(document).ready(function() {

	var username = $('#username_posted').html();

	$('#heatmap_link').click(function() {
		location.href = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/heatmap/' + username;
	});

	$('#classic_link').click(function() {
		location.href = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/classic/' + username;
	});

	$('#login_link').click(function() {

		location.href = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/login";
	});

	$('#logout_link').click(function() {
		location.href = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/logout";
	});

	$('#home_link').click(function() {
		location.href = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis";
	});

	$('#geo_link').click(function() {

		location.href = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/maps/' + username;
	});

	$('#tree_link').click(function() {

		location.href = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/treeex/" + username;

	});

}); 