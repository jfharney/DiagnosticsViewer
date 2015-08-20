var EA = EA || {};

EA.host = 'localhost';
EA.port = '8081' //document.location.port;

EA.default_groups = ['ACME'];
EA.default_datasets = ['a','b','c'];
EA.default_packages = ['atm','lnd'];
EA.default_variables = ['v1','v2','v3'];
EA.default_times = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"];

EA.noImageSource = "/static/exploratory_analysis/img/classic/Noimage.png";

var EA_CLASSIC_VIEWER = EA_CLASSIC_VIEWER || {};

EA_CLASSIC_VIEWER.namespace = function(ns_string) {
	var parts = ns_string.split('.'),
		parent = EA_CLASSIC_VIEWER,
		i;
	
	//strip redundant leading global
	if (parts[0] === 'EA_CLASSIC_VIEWER') {
		parts = parts.slice(1);
	}
	
	for(i=0;i<parts.length;i++) {
		// create a property if it doesn't exist
		if (typeof parent[parts[i]] === 'undefined') {
			parent[parts[i]] = {};
		}
		parent = parent[parts[i]];
	}
	return parent;
	
};


EA_CLASSIC_VIEWER.namespace('EA_CLASSIC_VIEWER.functions');
