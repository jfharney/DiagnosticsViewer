

var EA = EA || {};

EA.cache_location = '../../../static/exploratory_analysis/img/treeex/';


EA.host = 'acme-dev-2.ornl.gov';

EA.port = document.location.port;


var core_parameters_url = '/exploratory_analysis/core_parameters';

$.ajax({
	type : "GET",
	url : core_parameters_url,
	async : false,
	success : function(data) {
		
		var obj = JSON.parse(data);
		
		EA.host = obj['host'];
	},
	error: function() {
		
		alert('error in getting core parameters');
		
	}
});


EA.spinnerFlag = true;

//EA.uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live';
EA.uvcdat_live_root = '/usr/local/uvcdat/DiagnosticsViewer/django-app/uvcdat_live/';


//---------Tree settings----------//
EA.treeDepthFactor = 150;

EA.tree_width = 400;
EA.tree_height = 600;

EA.tree_margin_right = 20;
EA.tree_margin_left = 20;
EA.tree_margin_top = 30;
EA.tree_margin_bottom = 20;


//used in savetree.js
//EA.front_end_tree_cache_dir = '../../../static/cache/';
EA.front_end_tree_cache_dir = '../../../static/exploratory_analysis/cache/tree/';

EA.front_end_figure_cache_dir = '../../../static/exploratory_analysis/img/treeex/';



//--------Default Parameters------------//
EA.packList = ["lmwg"];
EA.timeList = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"];
EA.varList = ["GPP","NEE","HR","ER","NPP","QVEGT","QVEGE","QSOIL","GROSSNMIN"];


EA.tree_state = '';
