

var EA = EA || {};

EA.cache_location = '../../../static/exploratory_analysis/img/treeex/';


EA.host = 'localhost';

EA.port = document.location.port
//EA.port = '8081';

EA.spinnerFlag = true;

EA.uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live';



//---------Tree settings----------//
EA.treeDepthFactor = 150;

EA.tree_width = 960;
EA.tree_height = 800;

EA.tree_margin_right = 120;
EA.tree_margin_left = 120;
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