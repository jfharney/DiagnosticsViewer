####related to settings.py####
#databases_name = '/Users/i7j/sqlite3/mydb.db'
databases_name = '/Users/8xo/sqlite3/11-3/mydb.db'




#location of the cloned project 
#${DiagnosticsViewer_home}/django-app/uvcdat-live
#uvcdat_live_root = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/' 
uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/' 

#directory holding netcdf datasets
#<<<<<<< HEAD
default_sample_data_dir = '/Users/8xo/sampledatalens/tropics_warming_th_q_co2'
#default_sample_data_dir = '/Users/i7j/climatedata/tropics_warming_th_q_co2/' 
#=======
#default_sample_data_dir = '/Users/8xo/sampledatalens/tropics_warming_th_q_co2'
#default_sample_data_dir = '/Users/i7j/climatedata/' 
#>>>>>>> 4fa58d76f5f248e6cc2fafa6ee472a001c786db2



#staticfiles_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis",
staticfiles_dirs = uvcdat_live_root + "exploratory_analysis/static/exploratory_analysis"
    

#template_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/templates/exploratory_analysis"
template_dirs = uvcdat_live_root + "exploratory_analysis/templates/exploratory_analysis"
####end related to settings.py####


###UVCMetrics paths (deprecated)

#path to uvcmetric python code
#syspath_append_uvcmetrics = '/Users/i7j/uvcmetrics/src/python'
syspath_append_uvcmetrics = '/Users/8xo/software/exploratory_analysis/DiagnosticsGen/uvcmetrics/src/python'

#path to cdscan (in uvcdat)
#syspath_append_cdscan = '/Users/i7j/build-uvcdat/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan'
syspath_append_cdscan = '/Users/8xo/software/exploratory_analysis/uvcdat_light/build-uvcdat/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan'

###End UVCMetrics paths


#path to "cache", i.e. place to store figures and json files for d3 renderings
#cache_dir = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/cache/'
#cache_dir = uvcdat_live_root + 'exploratory_analysis/static/cache/'
cache_dir = uvcdat_live_root + 'exploratory_analysis/static/exploratory_analysis/cache/tree/'

#path for front end to access cache (can't be a local path)
#old front_end_cache_dir = '../../../static/cache/'
#front_end_cache_dir = '../../../static/exploratory_analysis/cache/tree/uu1/json/tropics_warming_th_q_co2/'

#directory holding netcdf datasets
#<<<<<<< HEAD
#default_sample_data_dir = '/Users/i7j/climatedata/tropics_warming_th_q/' #tropics_warming_th_q_clm2'
default_sample_data_dir = '/Users/8xo/djangoapp_data'
#=======

#default_sample_data_dir = '/Users/i7j/climatedata/' #tropics_warming_th_q_clm2'

#>>>>>>> 4fa58d76f5f248e6cc2fafa6ee472a001c786db2

default_tree_sample_data_dir = default_sample_data_dir
default_map_sample_data_dir = default_sample_data_dir + 'tropics_warming_th_q'

#img_cache_path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/'
img_cache_path = uvcdat_live_root + 'exploratory_analysis/static/exploratory_analysis/cache/'

#timeseries_cache_path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache'
timeseries_cache_path = uvcdat_live_root +'exploratory_analysis/static/exploratory_analysis/cache'

#generated_img_path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/treeex/'
generated_img_path = uvcdat_live_root + 'exploratory_analysis/static/exploratory_analysis/img/treeex/'
